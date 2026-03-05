# JumpIQ — Start to End Roadmap (Saare Phases)

Yeh document **pure journey** ko define karta hai: Phase 1 se leke **evolving intelligence engine** tak. Har phase mein kya **padhna**, **seekhna**, **implement** karna hai, aur kya **explain** karna hai — sab yahin hai.

**Goal (end state):** Evolving intelligence engine jo:
- Anomalies detect kare  
- Causes explain kare  
- Naye patterns seekh sake  
- Naye rules bana sake  

---

## Overview — Saare Phases Ek Nazar Mein

| Phase | Focus | Output |
|-------|--------|--------|
| **1** | Algorithms samajhna (pattern → algorithm → result → explain) | Deep understanding, daily reports |
| **2** | Data pipeline: Raw + Cleaning + Validation | Clean, validated data ready for models |
| **3** | Models + Derived values (scores) | Trend/seasonality/outlier + Valuation/Momentum scores |
| **4** | Rules + Database + UI feed | Rule engine, stored results, UI ke liye data |
| **5** | Multi-agent layer (Pattern Agents + Super Agent) | Anomaly detect + investigate + explain |
| **6** | Evolving system | New patterns, new rules, continuous improvement |

---

## Phase 1 — Algorithms Deep Understanding *(current)*

**Kya karna hai:** Code pe jump mat karo; pehle **pattern → algorithm → result → explanation** samjho.

### Padhna (R&D)
- Trend: slope, moving average, linear regression (time series)
- Seasonality: seasonal decomposition, Prophet, ARIMA
- Outliers: Z-score, IQR, Isolation Forest (aur kab fail hota hai)
- Time series basics: trend, seasonality, cycle, noise

### Seekhna
- Algorithm **andar se** kaise kaam karta hai (formula, logic)
- Kab fail hota hai (e.g. small data, non-stationary)
- Har concept: **“Yeh dealership revenue/valuation pe kaise apply hota hai?”**

### Implement
- Small notebooks/scripts: slope, moving avg, Z-score, IQR, decomposition (exploration folder)
- **Pehle understand, phir code** — checklist follow karo (EXPLORATION-PRINCIPLES.md)

### Explain
- Daily report: aaj kya padha + **dealership revenue pe kaise apply**
- Senior ko bata sako: “Trend is slope; we need it for Champions vs Stragglers because…”

**Done when:** Har pattern (trend, seasonality, outlier) ke liye tum explain kar sako — kaise kaam karta hai, kab use karna hai, JumpIQ mein kahan use hoga.

**Doc:** [PHASE1-STUDY.md](PHASE1-STUDY.md), [EXPLORATION-PRINCIPLES.md](EXPLORATION-PRINCIPLES.md)

---

## Phase 2 — Data Pipeline: Raw Data + Cleaning + Validation

**Kya karna hai:** Pipeline ka **pehla hissa** — raw data aane do, clean karo, validate karo. Model pe **sirf clean data** chadega.

### Padhna (R&D)
- Data quality: missing values, duplicates, wrong types, outliers (data bug vs real)
- Imputation: mean, median, last-known, forward-fill, time-based average
- Validation: range checks, consistency (e.g. revenue ≥ 0), schema validation
- ETL basics: extract (DMS, APIs), transform (clean), load (staging/DB)

### Seekhna
- Kab impute karna hai, kab row skip/flag karna hai
- “Never trust raw data blindly” — validation rules kaise design karein
- Time-series specific: missing month kaise handle karein (e.g. avg last 3 months)

### Implement
- Raw data ingest (sample/CSV ya mock API se start)
- Cleaning module: missing, duplicates, basic outliers (e.g. IQR for “sanity”)
- Validation layer: pass/fail + reason (e.g. “Jan revenue null → imputed with avg(Dec, Nov, Oct)”)
- Log/audit: kya change hua, kyu — explainability ke liye

### Explain
- “Ye record clean kyu hai / kyu reject hai” — human-readable reason
- Pipeline diagram pe bata sako: Raw → Cleaning → Validate → output clean dataset

**Done when:** Reliable clean + validated dataset mil raha hai; tum bata sakte ho kis row pe kya cleaning/validation lagi.

**Doc:** [PIPELINE.md](PIPELINE.md) — Step 1 & 2

---

## Phase 3 — Models + Derived Values (Scores)

**Kya karna hai:** Clean data pe **models** chalao (trend, seasonality, outlier); phir **derived values** (scores) nikalo.

### Padhna (R&D)
- Phase 1 ke algorithms ko **production-style** use (configurable, interpretable output)
- Derived metrics: Valuation Score, Profitability Score, Momentum Score, Market Health Score — yeh kaise define hain (business se align)
- Combining model outputs into one score (e.g. weighted formula, rules)

### Seekhna
- Model output ko **explain** kaise karein (e.g. “Momentum score 0.8 because trend slope positive and no outlier”)
- Kab trend/seasonality/outlier result conflict kare (e.g. spike = seasonal vs outlier) — resolution logic

### Implement
- Model layer: trend detection, seasonality detection, outlier detection (Phase 1 algorithms use karke)
- Derived-values layer: inputs = raw + model outputs → Valuation/Momentum/Profitability/Market Health scores
- Har score ke liye **explanation** (short text ya structured reason) — e.g. “Momentum = 0.8: upward trend, no anomaly”

### Explain
- “Is dealership ka Momentum score 0.8 kyu hai?” — components (trend, outlier, etc.) se answer
- “Ye spike outlier hai ya seasonal?” — algorithm + rule se explain

**Done when:** Clean data in → models run → scores + explanations out; sab interpretable.

**Doc:** [PIPELINE.md](PIPELINE.md) — Step 3 & 4, [PATTERN-DETECTION.md](PATTERN-DETECTION.md)

---

## Phase 4 — Rules + Database + UI Feed

**Kya karna hai:** **Rule engine** (e.g. revenue growth > 20% + market stable → Opportunity), results **database** mein store karo, **UI** ke liye ready data feed.

### Padhna (R&D)
- Rule engines: condition → action (e.g. if-then, threshold-based)
- Schema design: cleaned data, model outputs, scores, rule outcomes, timestamps — kaise store karein (query fast, audit easy)
- APIs for UI: what UI needs (time range, dealership, quadrants, anomaly list with reasons)

### Seekhna
- Rules ko kaise **version** karein (badalne par purana behavior explain ho)
- Database se “why did this dealership become Opportunity this month?” — trace back

### Implement
- Rule engine: input = scores + optional model flags → output = classification (Champion/Straggler/Opportunity/etc.) + reason
- Database: tables for cleaned data, model results, scores, rule results (with timestamp, dealership_id, etc.)
- UI feed: API ya view jo UI ko trend, quadrants, anomalies + explanations de

### Explain
- “Is dealership ko Opportunity kyu mark kiya?” — rule + underlying scores se answer
- “Is month revenue drop kyu dikha?” — DB se trace: raw → clean → model → score → rule

**Done when:** Rule output consistent hai, DB mein sab traceable hai, UI ko sahi data mil raha hai.

**Doc:** [PIPELINE.md](PIPELINE.md) — Step 5, 6, 7

---

## Phase 5 — Multi-Agent Layer (Detect + Investigate + Explain)

**Kya karna hai:** **Pattern Agents** (Trend, Outlier, Seasonality, Market) + **Super Agent** — anomaly detect karo, **investigate** karo (data validity → seasonal → competitor → group), **explain** karo.

### Padhna (R&D)
- Agent design: single responsibility (har agent ek pattern), orchestration (Super Agent)
- Investigation flow: CID-style — step-by-step reason trace (EXPLORATION-PRINCIPLES.md)
- Tools: Database query, web search, MCP, DMS — kab kaunsa use karna hai

### Seekhna
- Agents ka output **interpretable** kaise rakhein (natural language ya structured reason)
- Conflict resolution: multiple agents different bolein to Super Agent kaise decide kare

### Implement
- Trend Agent, Outlier Agent, Seasonality Agent, Market Agent — har ek Phase 3 ke models use kare, result + reason return kare
- Super Agent: agents ko call kare, results combine kare, classify kare (normal / anomaly / opportunity)
- Investigation module: anomaly pe trigger → data validity check → seasonal check → competitor/market check → final explanation (e.g. “Revenue dropped because inventory low + competitor price drop”)
- Tools integration: DB search, (optional) web/MCP/DMS for investigation

### Explain
- “System ne anomaly kyu bola?” — which agent(s) flagged, what reason
- “Revenue drop ka cause kya nikala?” — investigation steps + final explanation

**Done when:** Anomaly aate hi system investigate karke human-readable reason de raha hai.

**Doc:** [AGENTS.md](AGENTS.md), [EXPLORATION-PRINCIPLES.md](EXPLORATION-PRINCIPLES.md) — §7, §8

---

## Phase 6 — Evolving System (Learn New Patterns, New Rules)

**Kya karna hai:** System **evolving** ho — naye patterns add ho sakein, naye rules ban sakein, explanations improve hon, feedback se learn ho.

### Padhna (R&D)
- How other “intelligence” systems evolve (e.g. Stripe fraud — new rules, new signals over time)
- Feedback loops: user/senior corrects explanation → use that to tune rules or add patterns
- Rule/pattern versioning and A/B or gradual rollout

### Seekhna
- Naya pattern (e.g. “festival impact”) kaise add karein — new agent ya existing agent extend
- Naya rule kaise add karein without purana break karein — config-driven rules, audit log

### Implement
- **Config-driven rules:** rules DB/config file se; naya rule add = config update + deploy, no hardcode
- **Pattern registry:** list of patterns + which agent handles; naya pattern = naya agent ya existing agent extend
- **Feedback capture:** user “correct explanation” / “wrong classification” — store for R&D
- **Audit + versioning:** rule change, model change — kya badla, kab, kyu (explain)

### Explain
- “Naya rule kyu add kiya?” — business reason + example cases
- “Is pattern ko system ne kaise seekha/add kiya?” — documentation ya runbook

**Done when:** Naye patterns aur rules add kar sakte ho without full rewrite; explanations improve over time with feedback.

**Doc:** README — “evolving intelligence engine”; yeh phase ka detail future mein expand ho sakta hai

---

## Summary — Har Phase Mein Kya

| Phase | Padhna | Seekhna | Implement | Explain |
|-------|--------|---------|------------|---------|
| **1** | Trend, seasonality, outlier, time series | Formula, kab fail, JumpIQ link | Notebooks (after understand) | Daily report + “dealership pe kaise” |
| **2** | Data quality, imputation, validation, ETL | Kab impute/flag, never trust raw | Ingest + clean + validate | “Ye row clean/reject kyu” |
| **3** | Models production-style, score definitions | Explain score, resolve conflicts | Models + derived scores + reasons | “Score 0.8 kyu”, “spike seasonal/outlier kyu” |
| **4** | Rule engine, DB schema, UI APIs | Rule versioning, trace “why” | Rules + DB + UI feed | “Opportunity kyu”, “drop trace” |
| **5** | Agent design, investigation flow, tools | Interpretable output, conflict resolve | Agents + Super Agent + investigation | “Anomaly kyu”, “cause kya” |
| **6** | Evolving systems, feedback, versioning | New pattern/rule add safely | Config rules, pattern registry, feedback | “Naya rule/pattern kyu, kaise” |

---

## Order of Work (Start to End)

1. **Phase 1** — Abhi yahi karo; complete karo with daily reports.  
2. **Phase 2** — Jab Phase 1 clear ho, pipeline ka data part (raw + clean + validate).  
3. **Phase 3** — Clean data pe models + scores; explainability har step pe.  
4. **Phase 4** — Rules + DB + UI; full pipeline end-to-end (data → UI).  
5. **Phase 5** — Agent layer; anomaly + investigation + explain.  
6. **Phase 6** — Evolving: new patterns, new rules, feedback.

---

## Important Reminder

- **Phase 1** ke bina Phase 2–6 solid nahi banenge — pehle **understand**, phir implement.  
- Har phase mein **explain** zaroori hai — JumpIQ ko “why” batana hai.  
- Documentation update karte raho: jo naya seekha/implement kiya, short note bana do (same docs ya new R&D notes).  
- Yeh roadmap **living doc** hai — project ke saath refine ho sakta hai (dates, priorities).  

Ab **Phase 1** pe focus karo; baaki phases ka detail jab us phase pe pahuncho tab aur bhar sakte ho.
