# PTCG Agent — Decision Log

---

## 2026-06-18 — Project Initialization

**Context:** Solo project for the Kaggle `pokemon-tcg-ai-battle` competition. Goal is a self-improving multi-agent factory that produces increasingly better Player Agents submitted to the ladder.

**Decisions made today:**

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | **Python 3.13.1** confirmed as runtime | Verified ≥ 3.10 required; 3.13.1 found on system — no version issues |
| 2 | **`kaggle` SDK** as submission interface | Official API for interacting with the competition ladder |
| 3 | **`pytest`** as test framework | Standard, lightweight; fits bottom-up MVP approach |
| 4 | **`json` + `pathlib`** as stdlib only | Both are Python built-ins — no extra install needed |
| 5 | **Git initialized** in `ptcg-agent/` root | Version control from day one; `.gitignore` excludes credentials, caches, logs |
| 6 | **Folder scaffold fixed** at project start | Avoids structural churn later; all layers (agents, factory, router, skills, logs, versions, submission) locked in |

**Architecture philosophy:**
- Build bottom-up: MVP first, then iterate via the factory loop
- All inter-agent communication routed through `router/bus.py`
- Skills (JSON) drive agent behavior — logic stays separate from knowledge
- Every improvement cycle logged in `versions/version_history.json`

---
