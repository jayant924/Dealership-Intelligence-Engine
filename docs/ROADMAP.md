# JumpIQ — Start to End Roadmap (All Phases)

This document defines the complete journey: from Phase 1 straight through to the evolving intelligence engine. It dictates exactly what to study, learn, implement, and explain at every phase.

**Goal (end state):** Evolving intelligence engine that:
- Detects anomalies
- Explains causes 
- Learns new patterns  
- Generates new rules  

---

## Overview — All Phases at a Glance

| Phase | Focus | Output |
|-------|--------|--------|
| **1** | Understanding algorithms (pattern → algorithm → result → explain) | Deep understanding, daily reports |
| **2** | Data pipeline: Raw Data + Cleaning + Validation | Clean, validated data ready for models |
| **3** | Models + Derived values (scores) | Trend/seasonality/outlier + Valuation/Momentum scores |
| **4** | Rules + Database + UI feed | Rule engine, stored results, UI ke liye data |
| **5** | Multi-agent layer (Pattern Agents + Super Agent) | Anomaly detect + investigate + explain |
| **6** | Evolving system | New patterns, new rules, continuous improvement |

---

## 🚨 Urgent Sprint: Friday Demo PoC (Current Focus)

**Goal:** Compress key learnings from Phase 1, Phase 3, and Phase 5 to deliver a working Proof of Concept (PoC) demo by Friday.

*   **What we need for Friday:**
    1.  **Concept Explanation:** Be able to clearly explain the target algorithms (Trend, Z-Score/Outlier, Seasonality).
    2.  **Implementation Approach:** Explain how a Multi-Agent architecture (Super Agent + Pattern Agents) applies to these algorithms in JumpIQ.
    3.  **Working Demo:** A script running mock time-series sales data against the algorithms and generating an "Anomaly Report."
    4.  **Next Steps:** Presentation on how this PoC evolves into the production Intelligence Engine.

*After the Friday Demo, we will return to the structured Phase 2 (Data Pipeline) and stabilize the system end-to-end.*

---

## Phase 1 — Algorithms Deep Understanding *(current)*

**Objective:** Do not jump straight to code. First, understand the flow: pattern -> algorithm -> result -> explanation.

### Research & Study (R&D)
*See deep-dive documentation in the `/docs/` folder.*
- **Trend:** [Algorithm Guide](algorithms/trend_detection.md) | [Learning Notes](learning/TREND_AND_SEASONALITY.md) (slope, moving average)
- **Seasonality:** [Algorithm Guide](algorithms/seasonality_detection.md) | [Learning Notes](learning/TREND_AND_SEASONALITY.md) (decomposition, Prophet)
- **Outliers:** [Learning Notes](learning/ANOMALY_DETECTION.md) (Z-score, IQR)
- **Exploration Scripts:** [exploration/script/](../exploration/script/) (trend_detection.py, seasonality_detection.py)
- **Working PoC Dashboard:** [exploration/web app/](../exploration/web%20app/) (FastAPI + Angular)

### Understanding & Learning
- How the algorithm works internally (formulas, mathematical logic).
- When it fails (e.g., small datasets, non-stationary data).
- For every concept: “How does this apply to dealership revenue and valuation?”.

### Implementation
- Small notebooks/scripts: slope, moving avg, Z-score, IQR, decomposition.
- Understand first, then code. Follow the principles in EXPLORATION-PRINCIPLES.md.

### Explanation
- Daily report: what was studied today + how it applies to dealership revenue.
- Be able to explain clearly: “Trend is slope; we need it for Champions vs Stragglers because…”

**Done when:** You can explain every pattern (trend, seasonality, outlier) — how it works, when to use it, and where it fits in JumpIQ.

**Doc:** [PHASE1-STUDY.md](PHASE1-STUDY.md), [EXPLORATION-PRINCIPLES.md](EXPLORATION-PRINCIPLES.md)

---

## Phase 2 — Data Pipeline: Raw Data + Cleaning + Validation

**Objective:** The first section of the pipeline — ingest raw data, clean it, and validate it. Models run strictly on clean data.

### Research & Study (R&D)
- Data quality: missing values, duplicates, wrong types, outliers (data bug vs real)
- Imputation: mean, median, last-known, forward-fill, time-based average
- Validation: range checks, consistency (e.g. revenue >= 0), schema validation
- ETL basics: extract (DMS, APIs), transform (clean), load (staging/DB)

### Understanding & Learning
- When to impute versus when to skip or flag a row.
- “Never trust raw data blindly” — learn how to design robust validation rules.
- Handling time-series specifics like missing months (e.g., averaging the last 3 months).

### Implementation
- Raw data ingest (sample/CSV ya mock API se start)
- Cleaning module: missing, duplicates, basic outliers (e.g. IQR for “sanity”)
- Validation layer: pass/fail + reason (e.g. “Jan revenue null → imputed with avg(Dec, Nov, Oct)”)
- Log/audit: kya change hua, kyu — explainability ke liye

### Explanation
- Explain “Why is this record clean/rejected?” with a human-readable reason.
- Be able to trace the pipeline flow: Raw -> Cleaning -> Validate -> Cleaned Output.

**Done when:** The dataset is reliably clean and validated, and you can explain exactly which logic processed each row.

**Doc:** [PIPELINE.md](PIPELINE.md) — Step 1 & 2

---

## Phase 3 — Models + Derived Values (Scores)

**Objective:** Run the models on clean data (trend, seasonality, outliers); then extract derived values (scores).

### Research & Study (R&D)
- Implement Phase 1 algorithms in a production style (configurable, interpretable outputs).
- Derived metrics: Valuation Score, Profitability Score, Momentum Score, Market Health Score — how these are defined and aligned with the business.
- Combining model outputs into one score (e.g. weighted formula, rules)

### Understanding & Learning
- How to explain the model output. (e.g. “Momentum score 0.8 because trend slope positive and no outlier”)
- How to resolve conflicts between trend, seasonality, and outlier results.

### Implementation
- Model layer: trend detection, seasonality detection, outlier detection (Phase 1 algorithms use karke)
- Derived-values layer: inputs = raw + model outputs -> Valuation/Momentum/Profitability/Market Health scores
- Provide a short text or structured reason for every score. — e.g. “Momentum = 0.8: upward trend, no anomaly”

### Explanation
- Answer “Why is this dealership’s momentum score 0.8?” by breaking down the components.
- Answer “Is this spike an outlier or seasonal?” using rules and algorithm results.

**Done when:** Clean data yields scores and explanations smoothly and interpretable outputs are generated.

**Doc:** [PIPELINE.md](PIPELINE.md) — Step 3 & 4, [PATTERN-DETECTION.md](PATTERN-DETECTION.md)

---

## Phase 4 — Rules + Database + UI Feed

**Objective:** Implement the rule engine, store results in the database, and feed data to the UI.

### Research & Study (R&D)
- Rule engines: condition -> action (e.g. if-then, threshold-based)
- Schema design: cleaned data, model outputs, scores, rule outcomes, timestamps — how to store items for fast querying and easy auditing.
- APIs for UI: what UI needs (time range, dealership, quadrants, anomaly list with reasons)

### Understanding & Learning
- How to version rules so that legacy behavior remains explainable if changes occur.
- Trace back via the database to answer why a dealership changed quadrant.

### Implementation
- Rule engine: input = scores + optional model flags -> output = classification (Champion/Straggler/Opportunity/etc.) + reason
- Database: tables for cleaned data, model results, scores, rule results (with timestamp, dealership_id, etc.)
- UI feed: API ya view jo UI ko trend, quadrants, anomalies + explanations de

### Explanation
- Explain why a dealership was marked as an opportunity using rules and scores.
- Using the DB to trace exactly why a revenue drop was flagged.

**Done when:** Rule outputs are consistent, traceable in the database, and the UI receives accurate data feeds.

**Doc:** [PIPELINE.md](PIPELINE.md) — Step 5, 6, 7

---

## Phase 5 — Multi-Agent Layer (Detect + Investigate + Explain)

**Objective:** **Pattern Agents** (Trend, Outlier, Seasonality, Market) + **Super Agent** — detect anomalies, investigate them (validity -> seasonal -> competitor -> group), and explain them.

### Research & Study (R&D)
- Agent design: single responsibility (one agent per pattern), orchestration (Super Agent)
- Investigation flow: CID-style — step-by-step reason trace (EXPLORATION-PRINCIPLES.md)
- Tools: Database query, web search, MCP, DMS — when to use which

### Understanding & Learning
- How to keep agent output highly interpretable using natural language.
- How the Super Agent resolves conflicting results from pattern agents.

### Implementation
- Trend Agent, Outlier Agent, Seasonality Agent, Market Agent — each using Phase 3 models to return results and reasons.
- Super Agent: Call agents, combine results, and classify.
- Investigation module: Trigger on anomaly -> Check data validity -> Check seasonality -> Market checks -> final explanation.
- Tools integration: DB search, (optional) web/MCP/DMS for investigation

### Explanation
- Answer: “Why did the system flag an anomaly?” (Which agents flagged it, and why).
- Answer: “What caused the revenue drop?” by detailing investigation steps.

**Done when:** As soon as an anomaly hits, the system investigates and returns a human-readable reason.

**Doc:** [AGENTS.md](AGENTS.md), [EXPLORATION-PRINCIPLES.md](EXPLORATION-PRINCIPLES.md) — §7, §8

---

## Phase 6 — Evolving System (Learn New Patterns, New Rules)

**Objective:** The system must evolve — able to add new patterns, generate new rules, improve explanations, and learn precisely from feedback.

### Research & Study (R&D)
- How other “intelligence” systems evolve (e.g. Stripe fraud — new rules, new signals over time)
- Feedback loops: The user corrects an explanation -> the system tunes its rules based on that correction.
- Rule/pattern versioning and A/B or gradual rollout

### Understanding & Learning
- How to securely add simple new patterns (e.g., “festival impact”).
- How to safely deploy new rules without breaking legacy logic.

### Implementation
- **Config-driven rules:** Rule retrieval driven from the config database; avoid hardcoding rules into application logic.
- **Pattern registry:** Registry noting which agents handle which patterns.
- **Feedback capture:** Record user corrections for R&D tuning.
- **Audit + versioning:** Who changed what, when, and why.

### Explanation
- “Why was this rule added?” Explained simply with business logic and example edge cases.
- Using the runbook documentation to trace how a system learned a new pattern.

**Done when:** New patterns and rules can be appended without application rewrites, and the feedback loop verifiably improves explanations.

---

## Summary — What to Do in Each Phase

| Phase | Research | Learn | Code | Synthesize |
|-------|--------|---------|------------|---------|
| **1** | Trend, seasonality, outlier, time series | Formulas, limitations, and direct application to JumpIQ. | Notebooks (after understand) | Reports linking algorithms to dealership logic |
| **2** | Data quality, imputation, validation, ETL | Determine imputation/flag conditions. | ETL execution. | Line-by-line justification. |
| **3** | Models production-style, score definitions | Handling calculation conflicts vs intuition. | Model extraction formulas | Justifying individual metrics. |
| **4** | Rule engine, DB schema, UI APIs | Ensuring backward compatibility. | Architecting delivery systems. | Tracing UI state directly back to triggers. |
| **5** | Advanced reasoning loop | Agent interaction safety | Agent system instantiation | Orchestrated anomaly justification |
| **6** | Auto-tuning parameters | Configuration-driven deployments | Feedback routing | Reviewing feedback efficacy. |

---

## Order of Work (Start to End)

1. **Phase 1** — Focus entirely here; generate accurate daily implementation reports.  
2. **Phase 2** — Once Phase 1 mathematics are understood, build out the ETL scripts.  
3. **Phase 3** — Run analysis models against cleaned data; maintain explainable architecture.  
4. **Phase 4** — Feed analytical output into the DB and UI rule engines.  
5. **Phase 5** — Deploy logic via Multi-Agent architectures.  
6. **Phase 6** — Evolving: new patterns, new rules, feedback.

---

## Important Reminder

- Phase 1 is the bedrock for the remainder of the architecture — understand the math before implementing it.  
- Explanation is paramount at every stage. We must teach JumpIQ to answer “why”.  
- Abstract learnings into standalone markdown (like /learning/).  
- The roadmap is a living document and will evolve with the project.  

Hyper-focus on Phase 1 logic for now; future planning details can be formalized when their phases arrive.
