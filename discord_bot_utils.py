"""
discord_bot_utils.py
--------------------
Helper functions for discord_bot.py command handlers.
"""

import asyncio
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

def format_decisions(dec_file: Path) -> str:
    content = dec_file.read_text(encoding="utf-8")
    entries = content.split("## Iteration ")
    if len(entries) <= 1:
        return "Decision log is empty."
    last_entries = entries[-3:]
    result_text = "**📝 Recent Decision Log Entries:**\n"
    for item in last_entries:
        result_text += f"\n*Iteration {item.strip()[:1000]}*\n"
    if len(result_text) > 2000:
        result_text = result_text[:1990] + "\n...(truncated)"
    return result_text

def format_log_entries(component: str, path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data:
        return "Logs are empty."
    latest = data[-3:]
    msg = f"**📊 Latest Heuristic Reasoning for `{component}`:**\n"
    for i, entry in enumerate(latest):
        msg += f"\n**Turn {entry.get('turn')} ({entry.get('perspective')}):**\n```json\n"
        cleaned_entry = {k: v for k, v in entry.items() if k not in ("turn", "perspective")}
        msg += json.dumps(cleaned_entry, indent=2)[:500]
        msg += "\n```"
    return msg

async def run_subprocess(ctx, *args, success_msg, failure_header):
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    if process.returncode == 0:
        await ctx.send(success_msg)
    else:
        await ctx.send(f"{failure_header} with exit code {process.returncode}.\nError:\n```\n{stderr.decode(errors='replace')[-1000:]}\n```")

def format_command_output(returncode, stdout, stderr):
    msg = f"**Command Exit Code:** `{returncode}`\n"
    if stdout:
        msg += f"**Output:**\n```\n{stdout.decode(errors='replace')[-1500:]}\n```"
    if stderr:
        msg += f"**Errors:**\n```\n{stderr.decode(errors='replace')[-1500:]}\n```"
    if len(msg) > 2000:
        msg = msg[:1990] + "\n...(truncated)"
    return msg
