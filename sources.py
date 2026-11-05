#!/usr/bin/env python3
"""Multi-source candidate gathering and scoring. Free, no-account endpoints only:
GitHub Search API, Hacker News (Algolia API), Product Hunt (public Atom feed), Hugging Face (public API),
Reddit (public .json, falls back to .rss), tech news RSS (TechCrunch, The Verge, Ars Technica).
Every function returns plain dicts with a `url` so each signal can be traced back to its source."""
import json, re, time, math, datetime, urllib.request, urllib.parse, urllib.error, xml.etree.ElementTree as ET, sys
UA = "Mozilla/5.0 (compatible; aiagentsboard-bot/1.0; +https://aiagentsboard.com/about/)"
SUBS = ["AI_Agents", "AgentsOfAI", "LocalLLaMA", "ChatGPT", "ClaudeAI"]
NEWS = {"TechCrunch": "https://techcrunch.com/category/artificial-intelligence/feed/",
        "The Verge": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "Ars Technica": "https://feeds.arstechnica.com/arstechnica/technology-lab"}
# Reputable outlets counted for the news signal (matched against the <source> of Google News RSS results).
REPUTABLE = ["TechCrunch", "The Verge", "Reuters", "Bloomberg", "WIRED", "Wired", "Ars Technica", "VentureBeat", "CNBC", "Business Insider",
             "The Information", "ZDNET", "ZDNet", "Engadget", "Forbes", "Financial Times", "The Wall Street Journal", "The New York Times", "Axios",
             "SiliconANGLE", "The Decoder", "Tom's Hardware", "InfoWorld", "The Register", "The Next Web", "Nikkei Asia", "MIT Technology Review", "GeekWire", "Fortune"]
PH_FEED = "https://www.producthunt.com/feed?category=artificial-intelligence"
# Weights of the combined score (max 100 + breadth bonus). Shown on the methodology line.
WEIGHTS = {"github": 25, "hn": 20, "producthunt": 15, "huggingface": 10, "reddit": 15, "news": 15}
BREADTH = 5   # points per additional source an agent appears in (max 4 extra sources counted)
LABEL = {"github": "GitHub", "hn": "Hacker News", "producthunt": "Product Hunt", "huggingface": "Hugging Face", "reddit": "Reddit", "news": "News"}

def fetch(url, accept=None, tries=3):
    for a in range(tries):
        h = {"User-Agent": UA}
        if accept: h["Accept"] = accept
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and a < tries - 1 and ("github" in url or (e.code == 429 and "reddit" in url)):
                time.sleep(30 * (a + 1)); continue
            print(f"  {e.code} {url}", file=sys.stderr); return None
        except Exception as e:
            print(f"  error {url}: {e}", file=sys.stderr); time.sleep(3)
    return None

def jget(url, **k):
    t = fetch(url, **k)
    try: return json.loads(t) if t else None
    except ValueError: return None

def _feed(url):
    t = fetch(url)
    if not t: return []
    try: root = ET.fromstring(t.encode())
    except ET.ParseError: return []
    out = []
    for it in root.iter():
        tag = it.tag.split("}")[-1]
        if tag not in ("item", "entry"): continue
        g = lambda n: next((c for c in it if c.tag.split("}")[-1] == n), None)
        ti, ln, dt = g("title"), g("link"), g("pubDate") or g("published") or g("updated")
        link = (ln.get("href") or ln.text) if ln is not None else ""
        body = g("description") or g("content") or g("summary")
        out.append({"title": (ti.text or "").strip() if ti is not None else "", "url": (link or "").strip(),
                    "date": (dt.text or "")[:25] if dt is not None else "", "text": re.sub("<[^>]+>", " ", (body.text or "") if body is not None else "")[:600]})
    return out

# ---------- discovery: broad lists of this week's candidates ----------
def discover(date, days=30):
    since = (datetime.date.fromisoformat(date) - datetime.timedelta(days=days))
    ts = int(datetime.datetime.combine(since, datetime.time()).timestamp())
    c = {}
    gh = []
    for q in (f"ai agent created:>{since - datetime.timedelta(days=30)}", f"topic:ai-agents pushed:>{since}"):
        r = jget("https://api.github.com/search/repositories?" + urllib.parse.urlencode({"q": q, "sort": "stars", "order": "desc", "per_page": 30}), accept="application/vnd.github+json")
        gh += [{"title": x["full_name"], "url": x["html_url"], "stars": x["stargazers_count"], "text": x.get("description") or ""} for x in (r or {}).get("items", [])]
        time.sleep(2)
    c["github"] = gh
    hn = []
    for q in ("agent", "AI agent", "autonomous agent", "coding agent"):
        r = jget("https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode({"query": q, "tags": "story", "numericFilters": f"created_at_i>{ts},points>50", "hitsPerPage": 40}))
        hn += [{"title": h["title"], "url": h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}", "hn": f"https://news.ycombinator.com/item?id={h['objectID']}", "points": h.get("points", 0)} for h in (r or {}).get("hits", [])]
    c["hn"] = sorted({h["hn"]: h for h in hn}.values(), key=lambda h: -h["points"])
    c["producthunt"] = _feed(PH_FEED)
    hf = []
    for kind in ("spaces", "models"):
        r = jget(f"https://huggingface.co/api/{kind}?sort=trendingScore&limit=60&full=false") or []
        hf += [{"title": x["id"], "url": f"https://huggingface.co/{'spaces/' if kind=='spaces' else ''}{x['id']}", "likes": x.get("likes", 0), "tags": x.get("tags", [])}
               for x in r if any("agent" in t.lower() for t in x.get("tags", [])) or "agent" in x["id"].lower()]
    c["huggingface"] = hf
    rd = []
    for s in SUBS:
        rd += reddit_list(f"https://www.reddit.com/r/{s}/top", {"t": "week", "limit": 50})
    c["reddit"] = rd
    nw = []
    for src, u in NEWS.items():
        for it in _feed(u):
            if re.search(r"\bagent", it["title"] + " " + it["text"], re.I): nw.append(dict(it, source=src))
    c["news"] = nw
    return c

def reddit_list(base, params):
    """Public .json first (often 403 for datacenter IPs), then the public .rss feed."""
    j = jget(base + ".json?" + urllib.parse.urlencode(params)) if not _RD.get("json_blocked") else None
    if j is None: _RD["json_blocked"] = True
    if j and "data" in j:
        return [{"title": p["data"]["title"], "url": "https://www.reddit.com" + p["data"]["permalink"], "score": p["data"].get("score")} for p in j["data"]["children"]]
    time.sleep(10)  # Reddit rate-limits anonymous feeds hard
    return [{"title": i["title"], "url": i["url"], "score": None} for i in _feed(base + "/.rss?" + urllib.parse.urlencode(params))]
_RD = {}

# ---------- per-agent signals ----------
def _hit(text, terms): return any(re.search(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])", text, re.I) for t in terms)

def signals(agent, date, cache, days=30):
    """agent: {name, terms[], github?, hf?[]}. Returns {source: {"value": number, "evidence": [urls]}} for sources with a hit."""
    terms = agent.get("terms") or [agent["name"]]
    since = datetime.date.fromisoformat(date) - datetime.timedelta(days=days)
    ts = int(datetime.datetime.combine(since, datetime.time()).timestamp())
    out = {}
    if agent.get("github"):
        r = jget(f"https://api.github.com/repos/{agent['github']}", accept="application/vnd.github+json")
        if r and "stargazers_count" in r: out["github"] = {"value": r["stargazers_count"], "evidence": [r["html_url"]]}
    pts, ev = 0, []
    for t in terms:
        r = jget("https://hn.algolia.com/api/v1/search?" + urllib.parse.urlencode({"query": t, "tags": "story", "numericFilters": f"created_at_i>{ts},points>10", "hitsPerPage": 50})) or {}
        for h in r.get("hits", []):
            u = f"https://news.ycombinator.com/item?id={h['objectID']}"
            if u not in ev and _hit(h.get("title", "") + " " + (h.get("url") or ""), [t]): ev.append(u); pts += h.get("points") or 0
    if ev: out["hn"] = {"value": pts, "evidence": ev[:5]}
    ph = [i for i in cache.setdefault("ph", _feed(PH_FEED)) if _hit(i["title"] + " " + i["text"], terms)]
    ph += [{"url": u} for u in agent.get("producthunt", [])]
    ph = list(dict.fromkeys(i["url"] for i in ph))
    if ph: out["producthunt"] = {"value": len(ph), "evidence": ph[:3]}
    hf = [{"url": f"https://huggingface.co/{x}", "id": x} for x in agent.get("hf", [])]
    likes = 0
    for x in hf:
        j = jget("https://huggingface.co/api/" + ("spaces/" + x["id"][7:] if x["id"].startswith("spaces/") else "models/" + x["id"])) or {}
        likes += j.get("likes", 0)
    if hf: out["huggingface"] = {"value": likes, "evidence": [x["url"] for x in hf]}
    if not cache.get("reddit"):  # this week's top posts in each subreddit (one request per sub; search endpoints get rate-limited)
        cache["reddit"] = [p for sub in SUBS for p in reddit_list(f"https://www.reddit.com/r/{sub}/top", {"t": "week", "limit": 100})]
    ev = list(dict.fromkeys(p["url"] for p in cache["reddit"] if _hit(p["title"], terms)))
    n = len(ev)
    if ev: out["reddit"] = {"value": n, "evidence": ev[:5]}
    nw = []
    for t in terms[:2]:  # Google News RSS search (free, no account), last N days, reputable outlets only
        q = f'"{t}" AI agent when:{days}d'
        txt = fetch("https://news.google.com/rss/search?" + urllib.parse.urlencode({"q": q, "hl": "en-US", "gl": "US", "ceid": "US:en"}))
        try: items = list(ET.fromstring(txt.encode()).iter("item")) if txt else []
        except ET.ParseError: items = []
        for it in items:
            src, title = (it.findtext("source") or ""), (it.findtext("title") or "")
            if src in REPUTABLE and _hit(title, [t]): nw.append({"url": it.findtext("link"), "title": title, "source": src})
    nw += [{"url": u} for u in agent.get("news", [])]
    if nw:
        ev = []
        for u in dict.fromkeys(i["url"] for i in nw if i.get("url")):
            if len(ev) >= 4: break
            ev.append(publisher_url(u))
        out["news"] = {"value": len({i["title"] if "title" in i else i["url"] for i in nw}), "evidence": ev,
                       "outlets": sorted({i["source"] for i in nw if "source" in i})}
    return out

def publisher_url(url):
    """Google News /rss/articles/ links are wrappers. Resolve the publisher URL.
    Any other URL is unchanged. If Google does not return one https article URL, keep the wrapper."""
    if not url or "news.google.com" not in url or "/articles/" not in url:
        return url
    try:
        page = fetch(url)
        if not page: return url
        sig = re.search(r'data-n-a-sg="([^"]+)"', page)
        ts = re.search(r'data-n-a-ts="(\d+)"', page)
        if not sig or not ts: return url
        article_id = url.split("/articles/", 1)[1].split("?", 1)[0]
        rpc = json.dumps(["garturlreq",
            [["X", "X", ["X", "X"], None, None, 1, 1, "US:en", None, 1, None, None, None, None, None, 0, 1],
             "X", "X", 1, [1, 1, 1], 1, 1, None, 0, 0, None, 0],
            article_id, int(ts.group(1)), sig.group(1)], separators=(",", ":"))
        freq = json.dumps([[["Fbv4je", rpc, None, "generic"]]], separators=(",", ":"))
        req = urllib.request.Request("https://news.google.com/_/DotsSplashUi/data/batchexecute",
            data=urllib.parse.urlencode({"f.req": freq}).encode(),
            headers={"User-Agent": UA, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "Referer": "https://news.google.com/"})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8", "replace")
        m = re.search(r'garturlres\\",\\"(https://[^\\"\s]+)', body)
        if not m or "news.google.com" in m.group(1): return url
        return m.group(1)
    except Exception as e:
        print(f"  news resolve failed: {e}", file=sys.stderr)
        return url

def score(agents):
    """Combined score: for each source, value -> log scale, divided by the best value among this week's agents,
    times the source weight; plus BREADTH points per extra source. Deterministic and reproducible from the stored values."""
    best = {s: max([math.log1p(a["signals"][s]["value"]) for a in agents if s in a["signals"]] or [1]) or 1 for s in WEIGHTS}
    for a in agents:
        parts = {s: round(WEIGHTS[s] * math.log1p(v["value"]) / best[s], 1) for s, v in a["signals"].items()}
        a["score_parts"] = parts
        a["score"] = round(sum(parts.values()) + BREADTH * min(4, max(0, len(parts) - 1)), 1)
    agents.sort(key=lambda a: -a["score"])
    return agents
