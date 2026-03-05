# Multi-Agent Architecture — JumpIQ

Proposed design: **Super Agent** + **Pattern Agents**.

---

## Overview

```
Super Agent
     ↓
Pattern Agents (each checks one kind of pattern)
     ↓
Classifier / Orchestrator
     ↓
If anomaly → investigate (trace back reason)
```

---

## Pattern Agents

| Agent             | Job                          |
|-------------------|------------------------------|
| **Trend Agent**   | Detects growth or decline    |
| **Outlier Agent**| Detects abnormal spikes/drops |
| **Seasonality Agent** | Detects recurring cycles |
| **Market Agent**  | Checks competitor / market trends |

Each agent:

- Receives (relevant) data from Super Agent
- Runs its specific algorithms
- Returns a result (e.g. “trend up”, “outlier at month X”, “seasonal spike”)

---

## Example Flow

1. **Super Agent** receives dealership (or aggregate) data.
2. **Trend Agent** → e.g. “Upward trend, slope +X.”
3. **Outlier Agent** → e.g. “Outlier at Month 4.”
4. **Seasonality Agent** → e.g. “No unexpected seasonality.”
5. **Classifier** combines results and decides:
   - Normal
   - Anomaly → trigger investigation
   - Opportunity / Risk (from rules + patterns)
6. If **anomaly**, system investigates (trace back reason using tools).

---

## Tools Agents Can Use

- **Database** — query existing dealership metrics, history
- **Web search** — market trends, news
- **MCP** — external tool integrations
- **DMS** — dealer management system data

Agents use these to **explain** (e.g. “Revenue dropped because inventory low and competitor price drop”).

---

## Why Interpretable Models

Requirement: **Explain** why a number changed (real event vs seasonal vs data bug vs model).

So:

- Prefer **interpretable models** (regression, rules, classical time series).
- Avoid **black-box** neural networks for core pattern detection.
- Agents should return human-readable reasons, not only scores.

---

## Phase 1 vs Agents

Phase 1 focus: **Understand algorithms deeply** (trend, seasonality, outlier, time series).  
Once that is solid, design and implement the multi-agent layer on top of the same algorithms.
