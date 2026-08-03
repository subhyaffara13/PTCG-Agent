import json
from pathlib import Path


def format_status_report(report_file: Path) -> str:
    report = json.loads(report_file.read_text(encoding="utf-8"))
    iter_id = report.get("iteration", "unknown")
    raw_scores = report.get("raw_scores", {})
    version_scores = report.get("version_scores", {})
    best_ver = version_scores.get("best_version", "unknown")
    best_score = version_scores.get(best_ver, 0.0)
    return (
        f"**🏆 PTCG Agent Current Status**\n"
        f"• **Current Iteration:** {iter_id}\n"
        f"• **Peak Baseline Local Score:** `{best_score}` (Version: `{best_ver}`)\n"
        f"• **Reasoning Test Score:** `{raw_scores.get('reasoning_test', 0.0)}`\n"
        f"• **Deck Test Score:** `{raw_scores.get('deck_test', 0.0)}`\n"
        f"• **Variance Baseline Score:** `{raw_scores.get('variance_baseline', 0.0)}`"
    )

