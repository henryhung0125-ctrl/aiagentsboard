"""Extra pages: AI Coding Agent Setup Pack (sales + hidden download), free checklist, which-agent picker, and Probably Stolen calculator."""
import os, json, shutil
from which_agent import picker_body
DL = "/dl/C0EXYCG89EaeAcvytSaNYKjS/"
BUY = "https://buy.stripe.com/14AbJ1ccI83l8ky8ZseIw04"
TIP = "https://buy.stripe.com/4gMdR990w97p0S6a3weIw03"
ZIP = "AI-Coding-Agent-Setup-Pack.zip"
MAIL = "sitop@mail.grokbot.com"

def pack_body(zh, P):
    L = lambda z, e: z if zh else e
    inc = [("context", L("可直接放進專案的 <code>AGENTS.md</code>、<code>CLAUDE.md</code> 與 <code>.cursor/rules/*.mdc</code> 範本，涵蓋三種常見技術棧：網頁應用（TypeScript/Next.js）、Python 服務/函式庫、資料分析（Python/SQL/notebook）。", "Drop-in <code>AGENTS.md</code>, <code>CLAUDE.md</code> and <code>.cursor/rules/*.mdc</code> templates for three common stacks: web app (TypeScript/Next.js), Python service/library, and data/analytics (Python/SQL/notebooks).")),
           ("prompts", L("6 個提示詞範本：規劃、重構、除錯、撰寫測試、程式碼審查、交接筆記，每個都附填好的範例。", "6 prompt templates: planning, refactoring, debugging, writing tests, code review and handoff notes, each with a filled-in example.")),
           ("workflows", L("工作流程指南：先規劃再執行、安全的 git 習慣（分支、worktree、禁止 force-push）、子代理與平行代理、上下文管理。", "Workflow guides: plan-then-execute, safe git habits (branches, worktrees, no force-push), subagents and parallel agents, context hygiene.")),
           ("checklists", L("3 份檢查清單：專案初始設定、每次任務前、合併前。", "3 checklists: repo setup, before each task, before merging.")),
           ("examples", L("完整實例：從規劃、分步實作到獨立審查的一次真實流程，以及一份填寫完成的 AGENTS.md。", "Worked examples: a full plan → step-by-step diff → independent review session, plus a filled-in AGENTS.md."))]
    lis = "".join(f"<li><b>{k}</b> — {v}</li>" for k, v in inc)
    why = L("<ul><li><b>指令勝過敘述</b>：每份範本都寫出確切的指令（例如 <code>pnpm test -- path</code>），代理照做更可靠。</li><li><b>驗證是任務的一部分</b>：每個提示詞都以「證明它能用」結尾。</li><li><b>明確的禁止清單</b>：不亂加依賴、不改 lockfile、不刪測試、不 force-push。</li><li><b>單一事實來源</b>：AGENTS.md 為主，CLAUDE.md 與 Cursor 規則只引用它，不必維護三份。</li></ul>",
            "<ul><li><b>Commands over prose</b>: every template states exact commands (e.g. <code>pnpm test -- path</code>), which agents follow far more reliably.</li><li><b>Verification built in</b>: every prompt ends with a \"prove it\" step.</li><li><b>Explicit do-not lists</b>: no surprise dependencies, lockfile edits, deleted tests or force-pushes.</li><li><b>One source of truth</b>: AGENTS.md holds the rules; CLAUDE.md and Cursor rules point to it, so you maintain one file, not three.</li></ul>")
    sample = """# Prompt: Debug from evidence
1. Reproduce the bug first and show me the output.
2. List 2-4 hypotheses ranked by likelihood, with evidence.
3. Test the top hypothesis with the cheapest check. No speculative fixes.
4. Write a failing regression test, then the minimal fix.
Do not: wrap it in try/except, add retries/sleeps as a fix."""
    return (f'<h1>AI Coding Agent Setup Pack</h1><p class="sub">{L("給 Claude Code、Cursor 與 Codex 使用者的實用設定包：範本、提示詞、工作流程與檢查清單。", "A practical setup kit for Claude Code, Cursor and Codex users: templates, prompts, workflows and checklists.")}</p>'
            + f'<p class="sub">{L("還不確定？先拿", "Not sure yet? Start with the")} <a href="{P("/free-checklist/")}">{L("免費設定檢查清單", "free setup checklist")}</a>{L("。", ".")}</p>'
            f'<div class="card"><div class="price">$19</div><p>{L("一次付費，立即下載 zip（46 個檔案）。僅接受信用卡。", "One-time payment, instant zip download (46 files). Card payments only.")}</p><a class="btn" href="{BUY}">{L("購買並下載", "Buy &amp; download")}</a></div>'
            f'<div class="card"><h2>{L("內容", "What&#39;s inside")}</h2><ul>{lis}</ul></div>'
            f'<div class="card"><h2>{L("為什麼比免費範本好用", "Why it beats the free repos")}</h2>{why}</div>'
            f'<div class="card"><h2>{L("試閱", "Sample")}</h2><pre style="white-space:pre-wrap">{sample}</pre></div>'
            f'<div class="card"><h2>{L("退款", "Refunds")}</h2><p>{L(f"購買後 7 天內，來信 <a href=mailto:{MAIL}>{MAIL}</a> 即可全額退款，不問理由。", f"Full refund within 7 days of purchase, no questions asked: email <a href=mailto:{MAIL}>{MAIL}</a>.")}</p>'
            f'<p class="sub">{L("免責聲明：本產品為非官方產品，與 Anthropic、OpenAI、Anysphere（Cursor）或任何工具廠商均無關聯，亦未獲其認可或贊助。產品名稱僅用於說明相容性。範本請依你的專案自行調整與審查。", "Disclaimer: this is an unofficial product, not affiliated with, endorsed by or sponsored by Anthropic, OpenAI, Anysphere (Cursor) or any tool vendor. Product names are used only to describe compatibility. Review and adapt the templates to your own project.")}</p></div>')

def dl_body(zh):
    L = lambda z, e: z if zh else e
    return (f'<h1>{L("感謝購買！", "Thank you for your purchase!")}</h1><div class="card"><p><a class="btn" href="{ZIP}" download>{L("下載 AI Coding Agent Setup Pack（zip）", "Download AI Coding Agent Setup Pack (zip)")}</a></p>'
            f'<p>{L("建議先閱讀 README.md 的「10 分鐘快速開始」。請收藏本頁以便日後重新下載，並請勿公開分享此連結。", "Start with the 10-minute quick start in README.md. Bookmark this page to re-download later, and please don&#39;t share the link publicly.")}</p>'
            f'<p>{L(f"下載有問題或需要退款（7 天內）：<a href=mailto:{MAIL}>{MAIL}</a>", f"Download problems or refunds (within 7 days): <a href=mailto:{MAIL}>{MAIL}</a>")}</p></div>')

def ps_body(zh, P, items):
    L = lambda z, e: z if zh else e
    s = {"item": L("物品", "Item"), "cat": L("類別", "Category"), "base": L("基礎價", "Base"), "sell": L("建議售價", "Sell price"), "buy": L("進貨成本", "Buy cost"), "profit": L("利潤", "Profit"), "pc": L("每格利潤", "Profit/cell"), "src": L("交叉核對", "Cross-check"),
         "ok": L("兩來源一致", "2 sources agree"), "single": L("單一來源", "single source"), "diff": L("來源不一致", "sources differ"), "cb": L("違禁品", "contraband")}
    opt = lambda v, t, sel="": f'<option value="{v}"{" selected" if sel else ""}>{t}</option>'
    diff = opt(20, L("Price Gouge（+20%）", "Price Gouge (+20%)")) + opt(15, L("Mark Up（+15%）", "Mark Up (+15%)"), 1) + opt(0, L("Thin Margins（0%）", "Thin Margins (0%)")) + opt(0, "Red Ink (0%)")
    cb = opt(0, L("無", "None")) + opt(35, L("低（+35%）", "Low (+35%)")) + opt(70, L("中（+70%）", "Mid (+70%)")) + opt(100, L("高（+100%）", "High (+100%)")) + opt(150, L("極高（+150%）", "Critical (+150%)")) + opt(17, L("一級管制，持許可證（+17%）", "Class I restricted w/ permit (+17%)")) + opt(35, L("二級管制，持許可證（+35%）", "Class II restricted w/ permit (+35%)")) + opt(50, L("三級管制，持許可證（+50%）", "Class III restricted w/ permit (+50%)"))
    heat = opt(0, L("一般進貨（原價）", "Normal (base value)")) + opt(-10, L("贓物，熱度 ≤25（−10%）", "Stolen, heat ≤25 (−10%)")) + opt(-15, L("贓物，熱度 ≤50（−15%）", "Stolen, heat ≤50 (−15%)")) + opt(-20, L("贓物，熱度 ≤75（−20%）", "Stolen, heat ≤75 (−20%)")) + opt(-25, L("贓物，熱度 >75（−25%）", "Stolen, heat >75 (−25%)"))
    extra = [(15, L("小費（Pourboire）", "Tips (Pourboire)")), (15, L("觀光客稅", "Tourist tax")), (15, L("多樣買家加成", "Variety buyer")), (10, L("販賣機加成", "Vending machine")), (-5, L("糟糕談判者（特長）", "Awful Negotiator perk"))]
    ex = "".join(f'<label style="margin-right:1em"><input type="checkbox" class="ex" value="{v}"> {t} ({v:+d}%)</label>' for v, t in extra)
    J = json.dumps({"items": items, "s": s}, ensure_ascii=False).replace("</", "<\\/")
    return f'''<style>#ps input[type=checkbox]{{width:auto!important;display:inline;margin:0 .3em 0 0}}#ps label{{display:inline-block;margin:.3em 1em .3em 0}}#ps select,#ps input[type=number]{{width:auto}}</style><div id="ps"><h1>{L("Probably Stolen 售價與利潤計算機（非官方）", "Probably Stolen Price &amp; Profit Calculator (Unofficial)")}</h1>
<p class="sub">{L("選擇物品，輸入狀態、難度與違禁等級，算出建議售價，並查看所有物品的利潤排行。適用 2026-10-28 上架 Steam 的 1.0 版。", "Pick an item, set condition, difficulty and contraband level, and get the suggested sale price, plus a sortable profit ranking of every item. For the 1.0 Steam release (2026-10-28).")}</p>
<div class="card"><label>{s["item"]} <input id="q" list="il" placeholder="{L("輸入物品名稱", "Type an item name")}" style="width:100%;max-width:420px"></label><datalist id="il"></datalist>
<p><label>{L("狀態調整 %（−100 到 +200，100% 完好 = 0）", "Condition adjustment % (−100 to +200; pristine = 0)")} <input id="cond" type="number" min="-100" max="200" value="0" style="width:6em"></label>
<label>{L("難度", "Difficulty")} <select id="diff">{diff}</select></label>
<label>{L("違禁 / 管制等級", "Contraband / restricted level")} <select id="cb">{cb}</select></label>
<label>{L("進貨方式", "Bought as")} <select id="heat">{heat}</select></label></p>
<p>{ex}</p>
<div id="out" class="price" aria-live="polite"></div><p id="outd" class="sub"></p></div>
<div class="card"><h2>{L("利潤排行", "Profit ranking")}</h2><p class="sub">{L("使用上方的狀態、難度、進貨方式與加成設定。違禁等級只套用在被標為違禁品的物品上。點欄位標題排序。", "Uses the condition, difficulty, purchase and bonus settings above. The contraband level is applied only to items flagged as contraband. Click a column header to sort.")}</p>
<label><input id="onlycb" type="checkbox"> {L("只顯示違禁品", "Contraband only")}</label> <input id="f" placeholder="{L("篩選…", "Filter…")}">
<div style="overflow-x:auto"><table id="t" style="width:100%;border-collapse:collapse"><thead><tr></tr></thead><tbody></tbody></table></div></div>
<div class="card"><h2>{L("計算方式與資料來源", "How it&#39;s calculated &amp; sources")}</h2>
<p>{L("售價 = 四捨五入（基礎價 × (1 + 狀態%)）→ 再 × (1 + 零售加價% + 違禁加價% + 其他加成%)，每一步取整（剛好 .5 時取偶數），且不低於 0。進貨成本 = 基礎價經狀態調整後，再套用贓物熱度折扣。利潤 = 售價 − 進貨成本；每格利潤 = 利潤 ÷ 物品佔用格數。", "Sell price = round(base × (1 + condition%)), then × (1 + retail markup% + contraband% + other bonuses%), rounding each step to whole credits (exact halves to even), never below 0. Buy cost = condition-adjusted base with the stolen-goods heat discount. Profit = sell − buy cost; profit/cell = profit ÷ inventory cells.")}</p>
<p>{L("資料由我們自行整理並交叉核對：基礎價、類別、違禁標記與格數取自 AllThings.How 的 356 件物品清單（2026-10-28/29），並與 probablystolenguide.com 的 1.0 目錄（2026-11-02）逐項比對；價格規則（零售加價、違禁四級加價、許可證、熱度折扣、加成）比對 wikily.gg、probably-stolen.nicokobo.com 與 AllThings.How。已知差異：一個來源寫極高違禁品預設為 +200%，其他來源為 +150%，本工具採 +150%。各物品的違禁等級沒有公開對照，請依遊戲內交易平板顯示自行選擇。", "Data compiled and cross-checked by us: base values, categories, contraband flags and grid sizes from the AllThings.How 356-item list (2026-10-28/29), checked item by item against the probablystolenguide.com 1.0 catalogue (2026-11-02); pricing rules (retail markup, four contraband tiers, permits, heat discounts, bonuses) checked across wikily.gg, probably-stolen.nicokobo.com and AllThings.How. Known conflict: one source lists critical contraband at +200% default, others at +150%; this tool uses +150%. Per-item contraband tiers are not published, so pick the tier your trade tablet shows.")}</p>
<p class="sub">{L("非官方粉絲工具，與 Questing Goose Studio、tinyBuild 或 Valve 無關，未使用任何遊戲美術或標誌。遊戲更新可能改變數值，請以遊戲內為準。", "Unofficial fan tool, not affiliated with Questing Goose Studio, tinyBuild or Valve. No game art or logos are used. Patches may change values; the in-game trade tablet is authoritative.")}</p>
<p><a class="btn tip" href="{TIP}">{L("☕ 好用的話請我喝咖啡", "☕ Tip if this helped")}</a> <a class="btn" href="{P("/")}">{L("看本週 AI Agent 工具排行", "See this week&#39;s AI Agents ranking")}</a></p></div>
<script>const D={J};
(function(){{const S=D.s,I=D.items,$=id=>document.getElementById(id);
const r=x=>{{const f=Math.floor(x),d=x-f;let v=Math.abs(d-0.5)<1e-9?(f%2===0?f:f+1):Math.round(x);return Math.max(0,v)}};
$('il').innerHTML=I.map(i=>'<option value="'+i.n.replace(/"/g,'&quot;')+'">').join('');
const st=()=>{{let c=Math.max(-100,Math.min(200,+$('cond').value||0)),m=+$('diff').value,ex=[...document.querySelectorAll('.ex:checked')].reduce((a,e)=>a+ +e.value,0);return{{c,m,cb:+$('cb').value,h:+$('heat').value,ex}}}};
const calc=(i,o,useCb)=>{{const b=r(i.v*(1+o.c/100)),sell=r(b*(1+(o.m+(useCb?o.cb:0)+o.ex)/100)),buy=r(b*(1+o.h/100));return{{sell,buy,p:sell-buy,pc:(sell-buy)/i.cells}}}};
const cols=[['n',S.item],['c',S.cat],['v',S.base],['sell',S.sell],['buy',S.buy],['p',S.profit],['pc',S.pc],['x',S.src]];let sk='p',sd=-1;
document.querySelector('#t thead tr').innerHTML=cols.map(c=>'<th data-k="'+c[0]+'" style="cursor:pointer;text-align:left;padding:4px">'+c[1]+'</th>').join('');
document.querySelectorAll('#t th').forEach(th=>th.onclick=()=>{{const k=th.dataset.k;sd=sk===k?-sd:(k==='n'||k==='c'||k==='x'?1:-1);sk=k;draw()}});
function draw(){{const o=st(),q=$('q').value.trim().toLowerCase(),it=I.find(i=>i.n.toLowerCase()===q);
if(it){{const x=calc(it,o,true);$('out').textContent=x.sell+' cr';$('outd').textContent=S.base+' '+it.v+' · '+S.buy+' '+x.buy+' · '+S.profit+' '+x.p+' · '+it.c+(it.cb?' · '+S.cb:'')+' · '+S[it.x]+(it.x==='diff'?' ('+it.alt+')':'')}}else{{$('out').textContent='';$('outd').textContent=''}}
const f=$('f').value.toLowerCase(),oc=$('onlycb').checked;
let rows=I.filter(i=>(!oc||i.cb)&&(!f||i.n.toLowerCase().includes(f)||i.c.toLowerCase().includes(f))).map(i=>Object.assign({{}},i,calc(i,o,i.cb)));
rows.sort((a,b)=>(a[sk]>b[sk]?1:a[sk]<b[sk]?-1:0)*sd);
document.querySelector('#t tbody').innerHTML=rows.map(i=>'<tr style="border-top:1px solid #8883"><td style="padding:4px">'+i.n+(i.cb?' ⚠':'')+'</td><td>'+i.c+'</td><td>'+i.v+'</td><td><b>'+i.sell+'</b></td><td>'+i.buy+'</td><td>'+i.p+'</td><td>'+i.pc.toFixed(1)+'</td><td>'+S[i.x]+'</td></tr>').join('')}}
document.querySelectorAll('input,select').forEach(e=>e.addEventListener('input',draw));draw()}})();</script></div>'''

def extra_pages(lang_page, P, ROOT, updated):
    items = json.load(open(os.path.join(ROOT, "data/ps_items.json")))
    urls = []
    for lang in ("en", "zh"):
        zh = lang == "zh"; Pl = lambda p: P(lang, p)
        prod = {"@context": "https://schema.org", "@type": "Product", "name": "AI Coding Agent Setup Pack", "description": "Unofficial templates, prompts, workflows and checklists for Claude Code, Cursor and Codex users.", "offers": {"@type": "Offer", "price": "19.00", "priceCurrency": "USD", "url": BUY, "availability": "https://schema.org/InStock"}}
        urls.append((lang_page(lang, "/setup-pack/", "AI Coding Agent 設定包：CLAUDE.md、AGENTS.md、Cursor 規則範本（$19）" if zh else "AI Coding Agent Setup Pack: CLAUDE.md, AGENTS.md & Cursor rules templates ($19)",
                               "給 Claude Code、Cursor 與 Codex 使用者的非官方設定包：三種技術棧範本、6 個提示詞、工作流程與檢查清單。" if zh else "Unofficial setup pack for Claude Code, Cursor and Codex users: templates for 3 stacks, 6 prompt templates, workflow guides and checklists.",
                               pack_body(zh, Pl), [prod], updated), updated))
        urls.append((lang_page(lang, "/free-checklist/", "免費 AI Coding Agent 設定檢查清單｜Claude Code、Cursor、Codex" if zh else "Free AI Coding Agent Setup Checklist | Claude Code, Cursor, Codex",
                               "20 個讓 Claude Code、Cursor 與 Codex 少出錯的設定重點，訂閱電子報免費取得。" if zh else "20 checks that make Claude Code, Cursor and Codex fail less. Free with the newsletter.",
                               free_body(zh, Pl), None, updated), updated))
        urls.append((lang_page(lang, "/which-agent/", "我該用哪個 AI Agent？｜SI 精選" if zh else "Which AI agent should I use? | AI Agents Board",
                               "回答 3 個小問題，從本週排行幫你挑出 3 個 AI Agent，並連結免費檢查清單與 $19 設定包。" if zh else "Answer 3 short questions and get 3 AI agent picks from this week's board, plus the free setup checklist and the $19 setup pack.",
                               picker_body(zh, Pl), None, updated), updated))
        app = {"@context": "https://schema.org", "@type": "WebApplication", "name": "Probably Stolen Price & Profit Calculator (Unofficial)", "applicationCategory": "GameApplication", "operatingSystem": "Web", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}}
        urls.append((lang_page(lang, "/tools/probably-stolen/", "Probably Stolen 售價計算機與利潤排行（非官方）｜物品價格、違禁品加價" if zh else "Probably Stolen Price Calculator & Profit Ranking (Unofficial) | Item Sell Prices",
                               "免費 Probably Stolen 售價計算機：依物品、狀態、難度與違禁等級算出建議售價，並以利潤與每格利潤排行 310 件物品。" if zh else "Free Probably Stolen sell price calculator: get the suggested sale price by item, condition, difficulty and contraband level, and rank 310 items by profit and profit per cell.",
                               ps_body(zh, Pl, items), [app], updated), updated))
        lang_page(lang, DL, "下載｜AI Coding Agent Setup Pack" if zh else "Download | AI Coding Agent Setup Pack", "Download", dl_body(zh), None, None, True)
        shutil.copy("/workspace/pack/" + ZIP, os.path.join(ROOT, Pl(DL).lstrip("/"), ZIP))
    return urls

NL = "https://aiagentsboard.beehiiv.com/subscribe"
# Homepage order: free_cta(), then which_agent.picker_cta().
def free_cta(zh, P):
    return (f'<div class="card"><h2>{"免費：AI Coding Agent 設定檢查清單" if zh else "Free: AI coding agent setup checklist"}</h2>'
            f'<p>{"讓專案準備好給 Claude Code、Cursor 或 Codex 使用的 20 個重點。訂閱電子報即可免費取得。" if zh else "20 checks to get a repo ready for Claude Code, Cursor or Codex. Free when you join the newsletter."}</p>'
            f'<a class="btn" href="{P("/free-checklist/")}">{"免費領取檢查清單" if zh else "Get the free checklist"}</a></div>')

def free_body(zh, P):
    L = lambda z, e: z if zh else e
    sec = [(L("一次性：讓專案準備好給 Agent（約 30 分鐘）", "One time: make the repo agent-ready (~30 min)"), [
        L("在專案根目錄放 <code>AGENTS.md</code>，寫上確切的安裝、測試、lint、型別檢查與建置指令", "Put an <code>AGENTS.md</code> at the repo root with the exact install, test, lint, type-check and build commands"),
        L("在乾淨的 checkout 上實際跑過每一條指令", "Run every one of those commands on a clean checkout"),
        L("提供並記錄「只跑單一測試」的指令，讓回饋更快", "Document a single-test command for a fast feedback loop"),
        L("<code>CLAUDE.md</code> 用 <code>@AGENTS.md</code> 引用，不要重複內容", "Have <code>CLAUDE.md</code> import <code>@AGENTS.md</code> instead of duplicating it"),
        L("寫一段「禁止事項」：新增依賴、改 lockfile、migration、密鑰、刪測試、force-push", "Add a \"Do not\" section: new deps, lockfile edits, migrations, secrets, deleting tests, force-push"),
        L("<code>.env.example</code> 列出所有環境變數，真正的 <code>.env</code> 加入 gitignore", "List every env var in <code>.env.example</code>; keep the real <code>.env</code> gitignored"),
        L("用 pre-commit 或 CI 自動跑 lint 與測試，Agent 才不會「忘記」", "Run lint and tests in pre-commit or CI so the agent can't skip them"),
        L("安全指令加入允許清單，危險指令需要手動核准", "Allow-list safe commands; require approval for risky ones")]),
      (L("每次任務前（1 分鐘）", "Before each task (1 minute)"), [
        L("工作區乾淨，開新分支或 worktree", "Clean tree, new branch or worktree"),
        L("把目標寫成可觀察的結果，並說明如何驗證", "Write the goal as an observable outcome, plus how to verify it"),
        L("備好相關路徑、錯誤訊息或 issue 連結", "Have the relevant paths, errors or issue link ready"),
        L("講清楚限制（不加依賴、API 不變等）", "State constraints (no new deps, keep the API stable, etc.)"),
        L("改動超過 3 個檔案或需求不明確時，先規劃再動手", "Touching 3+ files or unclear? Plan first, then execute"),
        L("開新的 session，避免舊上下文干擾", "Start a fresh session so old context doesn't leak in")]),
      (L("合併前", "Before merging"), [
        L("讀完整個 diff，不只看摘要", "Read the whole diff, not just the summary"),
        L("<code>git diff --stat</code> 只出現預期中的檔案", "<code>git diff --stat</code> shows only the files you expected"),
        L("CI 上型別檢查、lint 與完整測試通過，而不是 Agent 說「本機通過」", "Type-check, lint and full tests pass in CI, not just \"locally\" per the agent"),
        L("新行為有測試，沒有測試被刪除、跳過或放寬", "New behavior has tests; none were deleted, skipped or loosened"),
        L("親手跑過一次功能", "Try the feature yourself once"),
        L("沒有密鑰、除錯輸出或被註解掉的程式碼", "No secrets, debug prints or commented-out code")])]
    lists = "".join(f'<h2>{h}</h2><ul style="list-style:none;padding-left:0">' + "".join(f'<li><label><input type="checkbox"> {i}</label></li>' for i in items) + '</ul>' for h, items in sec)
    return f'''<h1>{L("免費 AI Coding Agent 設定檢查清單", "Free AI coding agent setup checklist")}</h1>
<p class="sub">{L("給 Claude Code、Cursor 與 Codex 使用者：20 個讓 Agent 少出錯的重點。", "For Claude Code, Cursor and Codex users: 20 checks that make agents fail less.")}</p>
<div class="card" id="gate"><h2>{L("1. 訂閱電子報", "1. Join the newsletter")}</h2>
<p>{L("每週一封 AI Agent 工具排行，隨時可取消訂閱。按下按鈕會在新分頁開啟 beehiiv 訂閱頁，輸入 email 即可。", "One email a week with the AI agent tools ranking. Unsubscribe anytime. The button opens our beehiiv signup page in a new tab; just enter your email.")}</p>
<p><a class="btn" id="sub" href="{NL}" target="_blank" rel="noopener">{L("📬 免費訂閱並取得清單", "📬 Subscribe free & get the checklist")}</a></p>
<p class="sub"><a href="#" id="skip">{L("已經訂閱了？直接看清單", "Already subscribed? Show the checklist")}</a></p></div>
<div id="list" hidden><div class="card"><p class="sub">{L("2. 你的檢查清單（可直接勾選，或用瀏覽器列印存成 PDF）", "2. Your checklist (tick as you go, or print to PDF)")}</p>{lists}</div>
<div class="card"><h2>{L("想要完整版？", "Want the full kit?")}</h2><p>{L("$19 設定包包含三種技術棧的 AGENTS.md / CLAUDE.md / Cursor 規則範本、6 個提示詞、工作流程指南、完整檢查清單與實例。", "The $19 Setup Pack adds AGENTS.md / CLAUDE.md / Cursor rules templates for 3 stacks, 6 prompt templates, workflow guides, the full checklists and worked examples.")}</p>
<a class="btn" href="{BUY}">{L("購買設定包 $19", "Get the Setup Pack — $19")}</a> <a href="{P("/setup-pack/")}">{L("查看內容", "See what&#39;s inside")}</a></div></div>
<script>(function(){{var s=function(){{document.getElementById('list').hidden=false;try{{localStorage.setItem('fc','1')}}catch(e){{}}}};
document.getElementById('sub').addEventListener('click',function(){{setTimeout(s,800)}});
document.getElementById('skip').addEventListener('click',function(e){{e.preventDefault();s()}});
try{{if(localStorage.getItem('fc'))s()}}catch(e){{}}}})();</script>'''
