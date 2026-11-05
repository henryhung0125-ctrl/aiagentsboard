"""Which AI agent should I use? — static EN/ZH chooser.

Blurbs and prices are the 2026-11-03 board lines. Fit tags live in picker.js.
Homepage should place picker_cta() after free_cta()."""
import json, os

ROWS = [
    ("claude-code", "Claude Code",
     "Included in Claude Pro / Max / Team plans", "含於 Claude Pro／Max／Team 方案",
     "Developers and engineering teams who want to hand whole coding tasks to an AI.", "想把整段程式工作交給 AI 的開發者與工程團隊。",
     "Describe what you want and it plans, writes code, runs tests and opens pull requests; it can work on several tasks at once and runs in auto mode by default.", "描述你要什麼，它會規劃、寫程式、跑測試並開 Pull Request；可同時處理多個任務，預設以自動模式長時間工作。"),
    ("codex", "OpenAI Codex",
     "Included in ChatGPT plans · Plus $20", "含於 ChatGPT 方案 · Plus $20",
     "Engineers on a ChatGPT plan who need bugs fixed, refactors and new features.", "使用 ChatGPT、需要處理除錯、重構與新功能的工程師。",
     "OpenAI's coding agent runs many agents in parallel, verifies work with computer and browser tools, keeps going in the cloud after you close your laptop, and reviews pull requests.", "OpenAI 的程式 Agent，可平行跑多個 Agent，用電腦與瀏覽器工具驗證成果；關上筆電後仍在雲端繼續，也會自動審查 PR。"),
    ("docker-agent", "Docker Agent",
     "Free · open source (Apache-2.0)", "免費 · 開源（Apache-2.0）",
     "Developers and Docker users who want to assemble AI agent teams without code.", "想不寫程式就組出 AI Agent 團隊的開發者與 Docker 使用者。",
     "Docker's CLI plugin: define agents in YAML, give them tools (including MCP servers) and let teams of specialized agents delegate tasks automatically; works with many model providers.", "Docker 官方 CLI 外掛：用 YAML 定義 Agent、給它工具（含 MCP），讓多個專門 Agent 自動分工合作；支援多家模型供應商。"),
    ("talorys", "Talorys",
     "Free · open source (MIT) · runs on your Cloudflare account", "免費 · 開源（MIT）· 跑在你自己的 Cloudflare 帳號",
     "People who want a private AI assistant whose data stays in their own cloud.", "想要一個資料只在自己雲端的私人 AI 助理的人。",
     "A personal AI agent that runs entirely in your own Cloudflare account: it chats, remembers what matters, manages tasks, notes and projects, and runs reminders and routines on a schedule.", "完全跑在你自己 Cloudflare 帳號裡的個人 AI Agent：聊天、記住重要的事、管理任務、筆記與專案，並依排程執行提醒與例行工作。"),
    ("omnara", "Omnara",
     "Free to self-host (Apache-2.0) · Omnara Cloud: see site", "自架免費（Apache-2.0）· Omnara Cloud 見官網",
     "Teams who want a self-hosted managed-agent platform instead of Claude Managed Agents.", "想自架「託管 Agent」平台、替代 Claude Managed Agents 的團隊。",
     "An open-source managed agent platform: run AI agents on any model and any machine through an API, with tools, secrets, permissions and streaming built in.", "開源的託管 Agent 平台：用 API 在任何模型、任何機器上執行 AI Agent，內建工具、密鑰、權限與串流。"),
    ("dsh-superagent", "dsh-superagent",
     "Free · open source (MIT)", "免費 · 開源（MIT）",
     "Teams researching autonomous coding agents (the README says it is a research prototype, not an official product).", "想研究自主程式 Agent 的團隊（README 明說是研究原型、非正式產品）。",
     "A proactive coding agent for one GitHub repo: it listens to GitHub (optionally Feishu), takes work from allowed people, works in its own session and replies in the original thread, e.g. with a PR; a web panel shows what needs a person.", "針對一個 GitHub 倉庫的主動式程式 Agent：監聽 GitHub（可選飛書），有權限的人交辦工作後，它在自己的工作階段處理，並在原對話回覆（例如開 PR）；網頁面板顯示需要人處理的事項。"),
    ("manus", "Manus",
     "See site", "見官網",
     "People and companies who want a general-purpose AI agent to carry out whole tasks.", "想讓通用 AI Agent 代辦整件工作的個人與企業。",
     "A general-purpose AI agent that carries out the tasks you describe; news reports say Manus raised over $500 million this month and partnered with OPPO to bring its agent to smartphones.", "通用型 AI Agent 公司 Manus 的產品，依你的描述自行執行任務；據新聞報導，本月完成逾 5 億美元融資，並與 OPPO 合作把 Agent 帶進手機。"),
    ("jev", "Jev Ultrafast",
     "Free · open source (MIT)", "免費 · 開源（MIT）",
     "Developers who want to automate websites with code.", "想用程式自動操作網頁的開發者。",
     "Give it a goal and the agent picks actions (click, type, select, scroll) from a table of page elements; the README cites a Google Flights search done in 7.1 seconds.", "給一個目標，Agent 從頁面元素表選擇點擊、輸入、選取、捲動等動作完成任務；README 稱 Google Flights 查詢 7.1 秒完成。"),
    ("zcode", "ZCode",
     "Free · open source (Apache-2.0)", "免費 · 開源（Apache-2.0）",
     "Developers who want an AI coding workbench (README mainly in Simplified Chinese).", "需要 AI 寫程式工作台的開發者（README 以簡體中文為主）。",
     "An AI coding workbench with a desktop app, browser UI and terminal agent; the repo holds the client, backend and agent CLI source.", "AI 程式設計工作台，提供桌面應用、瀏覽器介面與終端 Agent；本倉庫含客戶端、後端與 Agent CLI 原始碼。"),
    ("mika", "Mika",
     "Free · open source (Apache-2.0)", "免費 · 開源（Apache-2.0）",
     "Android 11+ phone users.", "Android 11 以上的手機使用者。",
     "A phone AI assistant: say what you need and it operates apps and the web on a hidden background screen until done, while you keep using your phone.", "手機上的 AI 助理：說出需求，它在隱藏的背景畫面操作 App 和網頁直到完成，你可以繼續用手機。"),
    ("esp32", "ESP32 iPhone Agent",
     "Free · open source (MIT) · needs an ESP32 board", "免費 · 開源（MIT）· 需一塊 ESP32 開發板",
     "Makers and developers who want an AI to operate a real iPhone.", "想讓 AI 直接操作真實 iPhone 的玩家與開發者。",
     "Lets an AI model use a real iPhone with a $7 ESP32: it sees the screen over AirPlay and taps through USB input, with no computer and no jailbreak.", "用一塊約 7 美元的 ESP32 讓 AI 模型操作真實 iPhone：透過 AirPlay 看畫面、以 USB 輸入裝置點按，不需電腦也不用越獄。"),
    ("andee", "Andee",
     "Source on GitHub · hosted build: free allowance, then paid tokens", "原始碼在 GitHub · 代建版有免費額度，之後購買 tokens",
     "Users who want an AI to use any app on their phone or Mac the way they do.", "想讓 AI 像人一樣用手機或 Mac 上任何 App 的使用者。",
     "An agent for Android and Mac that uses any app like you do, with no root, no custom ROM and no per-app integrations.", "裝在 Android 或 Mac 上的 Agent，像你一樣使用任何 App，不需 root 或客製 ROM，也不需各 App 另外整合。"),
    ("openduet", "OpenDuet",
     "Free · open source (MIT) · needs a free CopilotKit project", "免費 · 開源（MIT）· 需免費 CopilotKit 專案",
     "Teams who want a self-hosted proactive work assistant in Slack or Teams.", "想自架主動型工作助理、在 Slack 或 Teams 使用的團隊。",
     "An open-source proactive agent that starts on your work without being asked and keeps you in the loop; each agent has its own computer and works on web, mobile, Slack or Teams.", "開源的主動型 Agent，不等你開口就開始處理工作並讓你掌握進度；每個 Agent 有自己的電腦，可在網頁、手機、Slack 或 Teams 使用。"),
    ("riverside", "Riverside Agents",
     "Included in every Riverside plan · 14-day free trial", "含於所有 Riverside 方案 · 14 天免費試用",
     "Podcasters, creators and teams who record conversations or talking-head videos.", "錄製 Podcast、訪談或口播影片的創作者與團隊。",
     "Four video-only agents: Producer preps the session, Editor turns raw recordings into an episode, Clipper cuts social clips, Marketer writes captions and schedules posts; nothing is published until you approve.", "四個專做影片的 Agent：Producer 準備錄製、Editor 剪成完整一集、Clipper 剪社群短片、Marketer 寫文案並排程貼文；發佈前需你核准。"),
    ("momentic", "Momentic Mo",
     "Free to start", "可免費開始",
     "Software teams and QA who want bugs caught before release.", "想在上線前抓出 bug 的軟體團隊與 QA。",
     "Mo is an AI QA engineer that runs autonomous test sessions in the cloud on web or hosted iOS/Android; a separate agent reproduces each bug before Mo reports it.", "Mo 是 AI QA 工程師，在雲端對網頁或 iOS／Android 自主跑測試，另一個 Agent 會重現每個 bug 後才回報；可從 PR 留言啟動。"),
]

def picker_cta(zh, P):
    if zh:
        return (f'<div class="card"><h2>我該用哪個 AI Agent？</h2>'
                f'<p>回答 3 個小問題，從本週排行幫你挑出 3 個工具。</p>'
                f'<a class="btn" href="{P("/which-agent/")}">幫我挑選</a></div>')
    return (f'<div class="card"><h2>Which AI agent should I use?</h2>'
            f'<p>Answer 3 short questions and get 3 picks from this week&#39;s board.</p>'
            f'<a class="btn" href="{P("/which-agent/")}">Help me choose</a></div>')

def picker_body(zh, P):
    L = lambda z, e: z if zh else e
    home = P("/")
    if not home.endswith("/"):
        home += "/"
    agents = {}
    for i, n, pe, pz, we, wz, de, dz in ROWS:
        agents[i] = {"n": n, "price": pz if zh else pe, "who": wz if zh else we, "what": dz if zh else de}
    data = {
        "q1": L("你想用它做什麼？", "What do you want to use it for?"),
        "q2": L("預算多少？", "What's your budget?"),
        "q3": L("你會寫程式嗎？", "Do you know how to code?"),
        "uses": [
            {"id": "code", "t": L("寫程式、交付功能", "Write and ship code")},
            {"id": "device", "t": L("幫我操作網頁或手機", "Use websites or my phone")},
            {"id": "tasks", "t": L("處理一般工作與提醒", "General tasks and reminders")},
            {"id": "video", "t": L("剪影片或 Podcast", "Video or podcasts")},
            {"id": "qa", "t": L("測試軟體", "Test my software")},
            {"id": "host", "t": L("自己架 Agent", "Run my own agents")},
        ],
        "budgets": [
            {"id": "free", "t": L("只要免費", "Free only")},
            {"id": "sub", "t": L("一個月約 20 美元可以", "About $20 a month is fine")},
            {"id": "any", "t": L("值得的話我願意付費", "I'll pay if it's worth it")},
        ],
        "codes": [
            {"id": "yes", "t": L("會", "Yes")},
            {"id": "some", "t": L("會一點", "A little")},
            {"id": "no", "t": L("不會", "No")},
        ],
        "step": L("第 %n 題，共 3 題", "Question %n of 3"),
        "next": L("下一題", "Next"),
        "back": L("上一題", "Back"),
        "see": L("看 3 個建議", "See my 3 picks"),
        "noteAll": L("本週排行裡有 3 個工具符合你的三個答案。", "Three tools on this week's board match your answers."),
        "noteNone": L("本週排行裡沒有工具同時符合三個答案，以下是最接近的。", "Nothing on this week's board matches all three answers. These are the closest."),
        "noteOne": L("本週排行裡只有 1 個工具同時符合三個答案，另外的建議是最接近的。", "Only 1 tool on this week's board matches all three answers. The other picks are the closest."),
        "noteSome": L("本週排行裡只有 %n 個工具同時符合三個答案，其餘是最接近的。", "Only %n tools on this week's board match all three answers. The other picks are the closest."),
        "why": {
            "fit": L("符合你要做的事、預算，以及你想自己動手的程度。", "Matches the job, the budget, and how hands-on you want to be."),
            "price": L("工作內容符合，但價格高於你選的預算。", "Fits the job, but it costs more than the budget you picked."),
            "skill": L("工作內容符合。本週排行把這項列給需要自己設定或審查結果的人。", "Fits the job. This week's board lists it for people who set it up or review the work."),
            "both": L("工作內容符合，但價格較高，也需要更多設定。", "Fits the job, but it costs more than you picked and expects more setup."),
            "close": L("不是完全符合。這是本週排行裡最接近的相關工具。", "Not an exact match. It is the closest related tool on this week's board."),
            "other": L("不是直接對應。本週排行裡很少有工具同時符合每個答案。", "Not a direct match. Few tools on this week's board fit every answer."),
        },
        "rank": L("本週排行 #%n", "Ranked #%n this week"),
        "who": L("適合誰：", "Who it's for:"),
        "what": L("能做什麼：", "What it does:"),
        "onBoard": L("看排行榜上的介紹", "See it on the board"),
        "again": L("重新選擇", "Start over"),
        "board": home,
        "agents": agents,
    }
    blob = json.dumps(data, ensure_ascii=False).replace("<", "\\u003c")
    check, pack = P("/free-checklist/"), P("/setup-pack/")
    if zh:
        noscript = ('這個挑選器需要 JavaScript。本週排行裡最前面的程式 Agent 是 '
                    '<a href="https://www.anthropic.com/claude-code">Claude Code</a>、'
                    '<a href="https://openai.com/codex/">OpenAI Codex</a> 與 '
                    '<a href="https://github.com/deepseek-ai/dsh-superagent-prototype">dsh-superagent</a>。')
    else:
        noscript = ('This chooser needs JavaScript. The top coding agents on the board are '
                    '<a href="https://www.anthropic.com/claude-code">Claude Code</a>, '
                    '<a href="https://openai.com/codex/">OpenAI Codex</a> and '
                    '<a href="https://github.com/deepseek-ai/dsh-superagent-prototype">dsh-superagent</a>.')
    return f'''<h1>{L("我該用哪個 AI Agent？", "Which AI agent should I use?")}</h1>
<p class="sub">{L("三個小問題，從本週排行挑出 3 個工具。", "Three short questions. Three picks from this week's board.")}</p>
<p class="sub">{L("建議來自 2026-11-03 本期排行的 15 個工具。分數代表熱度，不代表品質。", "Picks come from the 15 tools on the 2026-11-03 board. The ranking measures attention, not quality.")}</p>
<p>{L("若要設定程式 Agent，可先看", "Setting up a coding agent? Start with the ")}<a href="{check}">{L("免費檢查清單", "free checklist")}</a>{L("，或看 ", " or the ")}<a href="{pack}">{L("$19 設定包", "$19 setup pack")}</a>{L("。", ".")}</p>
<div id="quiz" class="card"><p class="steps" id="pstep"></p><h2 id="pq"></h2><div class="qopts" id="popts" role="group" aria-labelledby="pq"></div><div class="qnav"><button type="button" class="linkish" id="pback" hidden></button><button type="button" class="btn" id="pnext" disabled></button></div></div>
<div id="presult" hidden><p class="sub" id="pnote"></p><div id="pcards"></div>
<div class="card"><h2>{L("接著可以把程式 Agent 設定好", "Set up a coding agent")}</h2><p>{L("免費檢查清單有 20 個重點，給 Claude Code、Cursor 或 Codex 使用。$19 設定包再加上範本、提示詞與工作流程。", "The free checklist is 20 checks for Claude Code, Cursor or Codex. The $19 setup pack adds templates, prompts and workflows.")}</p><p><a class="btn" href="{check}">{L("免費檢查清單", "Free checklist")}</a> <a class="btn" href="{pack}">{L("設定包 $19", "Setup pack — $19")}</a></p></div>
<p><button type="button" class="linkish" id="pagain">{L("重新選擇", "Start over")}</button></p></div>
<noscript><div class="card"><p>{noscript}</p><p><a class="btn" href="{check}">{L("免費檢查清單", "Free checklist")}</a> <a class="btn" href="{pack}">{L("設定包 $19", "Setup pack — $19")}</a></p></div></noscript>
<script>window.PICKER_DATA={blob};</script>
<script src="/picker.js"></script>'''

def _page(zh, body):
    L = lambda z, e: z if zh else e
    title = L("我該用哪個 AI Agent？｜SI 精選", "Which AI agent should I use? | AI Agents Board")
    desc = L("回答 3 個小問題，從本週排行幫你挑出 3 個 AI Agent，並連結免費檢查清單與 $19 設定包。", "Answer 3 short questions and get 3 AI agent picks from this week's board, plus the free setup checklist and the $19 setup pack.")
    path = "/zh/which-agent/" if zh else "/which-agent/"
    other = "/which-agent/" if zh else "/zh/which-agent/"
    canon = "https://aiagentsboard.com" + path
    lang = "zh-Hant" if zh else "en"
    locale = "zh_TW" if zh else "en_US"
    home = "/zh/" if zh else "/"
    nav = (f'<a href="{home}">排行</a><a href="/zh/issues/">往期</a><a href="/zh/submit/">提交</a><a href="/zh/sponsor/">贊助</a><a href="/zh/setup-pack/">設定包</a><a href="/zh/tools/probably-stolen/">工具</a><a href="/zh/about/">關於</a>'
           f'<a class="lang" href="{other}" onclick="localStorage.setItem(\'lang\',\'en\')" hreflang="en">中文 / <b>EN</b></a>') if zh else (
           f'<a href="/">Ranking</a><a href="/issues/">Archive</a><a href="/submit/">Submit</a><a href="/sponsor/">Sponsor</a><a href="/setup-pack/">Setup Pack</a><a href="/tools/probably-stolen/">Tools</a><a href="/about/">About</a>'
           f'<a class="lang" href="{other}" onclick="localStorage.setItem(\'lang\',\'zh\')" hreflang="zh-Hant"><b>中文</b> / EN</a>')
    redir = "" if zh else "<script>try{if(localStorage.getItem('lang')=='zh')location.replace('/zh/which-agent/')}catch(e){}</script>"
    foot = (f"<footer><div class=\"sponsor\">本週贊助位開放中 — <a href='/zh/sponsor/'>贊助我們</a></div><p><a class=\"btn\" href=\"https://aiagentsboard.beehiiv.com/subscribe\" target=\"_blank\" rel=\"noopener\">📬 訂閱電子報</a> <a class=\"btn tip\" href=\"https://buy.stripe.com/4gMdR990w97p0S6a3weIw03\">☕ 請我喝咖啡</a></p><p>聯絡: <a href=\"mailto:sitop@mail.grokbot.com\">sitop@mail.grokbot.com</a> · <a href=\"/zh/privacy/\">隱私權政策</a> · <a href=\"/zh/terms/\">贊助條款</a></p><p>© 2026 SI 精選 AI Agents Board · 贊助內容一律標示</p></footer>"
            if zh else
            "<footer><div class=\"sponsor\">This week's sponsor slot is open — <a href='/sponsor/'>Sponsor us</a></div><p><a class=\"btn\" href=\"https://aiagentsboard.beehiiv.com/subscribe\" target=\"_blank\" rel=\"noopener\">📬 Get the weekly list by email</a> <a class=\"btn tip\" href=\"https://buy.stripe.com/4gMdR990w97p0S6a3weIw03\">☕ Buy us a coffee</a></p><p>Contact: <a href=\"mailto:sitop@mail.grokbot.com\">sitop@mail.grokbot.com</a> · <a href=\"/privacy/\">Privacy</a> · <a href=\"/terms/\">Sponsor terms</a></p><p>© 2026 SI 精選 AI Agents Board · Sponsored content is always labeled</p></footer>")
    updated = L("最後更新: ", "Last updated: ")
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="zh-Hant" href="https://aiagentsboard.com/zh/which-agent/"><link rel="alternate" hreflang="en" href="https://aiagentsboard.com/which-agent/"><link rel="alternate" hreflang="x-default" href="https://aiagentsboard.com/which-agent/">
<meta property="og:type" content="website"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{canon}"><meta property="og:site_name" content="SI 精選 AI Agents Board"><meta property="og:locale" content="{locale}"><meta property="og:image" content="https://aiagentsboard.com/og-image.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="https://aiagentsboard.com/og-image.png"><link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="icon" href="/favicon.png" type="image/png" sizes="64x64">
<link rel="stylesheet" href="/style.css">{redir}</head><body>
<header><a class="logo" href="{home}" aria-label="SI 精選 AI Agents Board"><img src="/logo-mark.svg" width="32" height="32" alt="">SI 精選 <span>AI Agents Board</span></a><nav>{nav}</nav></header>
<main>{body}<p class="meta">{updated}<time datetime="2026-11-05">2026-11-05</time></p></main>{foot}</body></html>
'''

def write_pages(root):
    def P(lang, path):
        return ("/zh" if lang == "zh" else "") + path
    for lang in ("en", "zh"):
        zh = lang == "zh"
        body = picker_body(zh, lambda path, lang=lang: P(lang, path))
        rel = "zh/which-agent/index.html" if zh else "which-agent/index.html"
        dest = os.path.join(root, rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(_page(zh, body))
    en = os.path.join(root, "en/which-agent/index.html")
    os.makedirs(os.path.dirname(en), exist_ok=True)
    with open(en, "w", encoding="utf-8") as f:
        f.write('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Moved</title><link rel="canonical" href="https://aiagentsboard.com/which-agent/"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=/which-agent/"><script>location.replace("/which-agent/"+location.hash)</script></head><body><p>Moved to <a href="/which-agent/">https://aiagentsboard.com/which-agent/</a></p></body></html>\n')

if __name__ == "__main__":
    write_pages(os.path.dirname(os.path.abspath(__file__)))
