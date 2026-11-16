/* Which-agent picker. Agent ids, ranks, URLs and fit tags match the 2026-11-16 board.
   Localized names and blurbs are supplied by the page as window.PICKER_DATA. */
(function () {
  var AGENTS = [
    {id: "claude-code", rank: 1, href: "https://www.anthropic.com/claude-code", uses: ["code"], cost: "sub", skill: "yes"},
    {id: "codex", rank: 3, href: "https://openai.com/codex/", uses: ["code"], cost: "sub", skill: "yes"},
    {id: "docker-agent", rank: 15, href: "https://github.com/docker/docker-agent", uses: ["host"], cost: "free", skill: "some"},
    {id: "talorys", rank: 19, href: "https://github.com/rociiu/talorys", uses: ["tasks"], cost: "free", skill: "some"},
    {id: "omnara", rank: 4, href: "https://github.com/omnara-ai/omnara", uses: ["host"], cost: "free", skill: "yes"},
    {id: "dsh-superagent", rank: 5, href: "https://github.com/deepseek-ai/dsh-superagent-prototype", uses: ["code"], cost: "free", skill: "yes"},
    {id: "manus", rank: 22, href: "https://manus.im/", uses: ["tasks"], cost: "paid", skill: "no"},
    {id: "jev", rank: 9, href: "https://github.com/browser-use/jev-ultrafast", uses: ["device"], cost: "free", skill: "yes"},
    {id: "zcode", rank: 11, href: "https://github.com/zai-org/ZCode", uses: ["code"], cost: "free", skill: "yes"},
    {id: "mika", rank: 10, href: "https://github.com/wangzan101/Mika", uses: ["device"], cost: "free", skill: "some"},
    {id: "esp32", rank: 14, href: "https://github.com/onehumanbeing/esp32-iphone-agent", uses: ["device"], cost: "free", skill: "yes"},
    {id: "andee", rank: 13, href: "https://github.com/kuafuai/andee", uses: ["device"], cost: "freemium", skill: "no"},
    {id: "openduet", rank: 17, href: "https://github.com/CopilotKit/OpenDuet", uses: ["tasks"], cost: "free", skill: "yes"},
    {id: "riverside", rank: 18, href: "https://riverside.com/", uses: ["video"], cost: "sub", skill: "no"},
    {id: "momentic", rank: 20, href: "https://momentic.ai/", uses: ["qa"], cost: "freemium", skill: "yes"}
  ];
  var COST = {free: {free: 1, freemium: 1}, sub: {free: 1, freemium: 1, sub: 1}, any: {free: 1, freemium: 1, sub: 1, paid: 1}};
  var SKILL = {no: {no: 1}, some: {no: 1, some: 1}, yes: {no: 1, some: 1, yes: 1}};
  var RELATED = {code: {qa: 1, host: 1}, qa: {code: 1}, host: {code: 1}, device: {tasks: 1}, tasks: {device: 1}, video: {}};

  function flags(a, ans) {
    var use = false, rel = false, i;
    for (i = 0; i < a.uses.length; i++) {
      if (a.uses[i] === ans.use) use = true;
      if (RELATED[ans.use] && RELATED[ans.use][a.uses[i]]) rel = true;
    }
    return {
      use: use,
      rel: rel && !use,
      cost: !!(COST[ans.budget] && COST[ans.budget][a.cost]),
      skill: !!(SKILL[ans.code] && SKILL[ans.code][a.skill])
    };
  }

  function tier(f) {
    if (f.use && f.cost && f.skill) return 0;
    if (f.use && f.skill) return 1;
    if (f.use && f.cost) return 2;
    if (f.use) return 3;
    if (f.rel && f.cost && f.skill) return 4;
    if (f.rel && f.skill) return 5;
    if (f.rel && f.cost) return 6;
    if (f.rel) return 7;
    if (f.cost && f.skill) return 8;
    if (f.skill) return 9;
    return 10;
  }

  function recommend(ans) {
    var scored = AGENTS.map(function (a) {
      var f = flags(a, ans);
      return {a: a, f: f, t: tier(f)};
    });
    scored.sort(function (x, y) { return x.t - y.t || x.a.rank - y.a.rank; });
    var exact = 0, i;
    for (i = 0; i < scored.length; i++) if (scored[i].t === 0) exact++;
    return {picks: scored.slice(0, 3), exact: exact};
  }

  function why(f, copy) {
    if (f.use && f.cost && f.skill) return copy.fit;
    if (f.use && !f.cost && !f.skill) return copy.both;
    if (f.use && !f.cost) return copy.price;
    if (f.use && !f.skill) return copy.skill;
    if (f.rel) return copy.close;
    return copy.other;
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function labeled(label, text) {
    var p = el("p");
    var b = el("b", null, label);
    p.appendChild(b);
    p.appendChild(document.createTextNode(" " + text));
    return p;
  }

  function mount(data) {
    var quiz = document.getElementById("quiz");
    var result = document.getElementById("presult");
    if (!quiz || !data) return;
    var steps = [
      {k: "use", q: data.q1, opts: data.uses},
      {k: "budget", q: data.q2, opts: data.budgets},
      {k: "code", q: data.q3, opts: data.codes}
    ];
    var ans = {}, i = 0;
    var stepEl = document.getElementById("pstep");
    var qEl = document.getElementById("pq");
    var optsEl = document.getElementById("popts");
    var next = document.getElementById("pnext");
    var back = document.getElementById("pback");

    function render() {
      var s = steps[i], o;
      stepEl.textContent = data.step.replace("%n", String(i + 1));
      qEl.textContent = s.q;
      optsEl.innerHTML = "";
      for (o = 0; o < s.opts.length; o++) {
        (function (opt) {
          var b = el("button", "qopt", opt.t);
          b.type = "button";
          b.setAttribute("aria-pressed", ans[s.k] === opt.id ? "true" : "false");
          b.addEventListener("click", function () { ans[s.k] = opt.id; render(); });
          optsEl.appendChild(b);
        })(s.opts[o]);
      }
      next.disabled = !ans[s.k];
      next.textContent = i === 2 ? data.see : data.next;
      back.hidden = i === 0;
      back.textContent = data.back;
    }

    function show() {
      var rec = recommend(ans);
      var note = document.getElementById("pnote");
      var cards = document.getElementById("pcards");
      var p, info, art, body, h, meta, link;
      quiz.hidden = true;
      result.hidden = false;
      if (rec.exact >= 3) note.textContent = data.noteAll;
      else if (rec.exact === 0) note.textContent = data.noteNone;
      else if (rec.exact === 1) note.textContent = data.noteOne;
      else note.textContent = data.noteSome.replace("%n", String(rec.exact));
      cards.innerHTML = "";
      for (p = 0; p < rec.picks.length; p++) {
        info = data.agents[rec.picks[p].a.id];
        if (!info) continue;
        art = el("article", "card rank");
        art.appendChild(el("div", "n", String(p + 1)));
        body = el("div");
        h = el("h2", "tool");
        link = el("a", null, info.n);
        link.href = rec.picks[p].a.href;
        link.rel = "noopener";
        h.appendChild(link);
        body.appendChild(h);
        meta = el("p", "meta", data.rank.replace("%n", String(rec.picks[p].a.rank)) + " · " + info.price);
        body.appendChild(meta);
        body.appendChild(el("p", null, why(rec.picks[p].f, data.why)));
        body.appendChild(labeled(data.who, info.who));
        body.appendChild(labeled(data.what, info.what));
        link = el("a", null, data.onBoard);
        link.href = data.board + "#t" + rec.picks[p].a.rank;
        body.appendChild(el("p")).appendChild(link);
        art.appendChild(body);
        cards.appendChild(art);
      }
      result.scrollIntoView({behavior: "smooth", block: "start"});
    }

    next.addEventListener("click", function () {
      if (!ans[steps[i].k]) return;
      if (i < 2) { i++; render(); }
      else show();
    });
    back.addEventListener("click", function () { if (i > 0) { i--; render(); } });
    document.getElementById("pagain").addEventListener("click", function () {
      ans = {}; i = 0; result.hidden = true; quiz.hidden = false; render();
      quiz.scrollIntoView({behavior: "smooth", block: "start"});
    });
    render();
  }

  if (typeof document !== "undefined") {
    document.addEventListener("DOMContentLoaded", function () { mount(window.PICKER_DATA); });
  }
  if (typeof module !== "undefined" && module.exports) {
    module.exports = {recommend: recommend, AGENTS: AGENTS};
  }
})();
