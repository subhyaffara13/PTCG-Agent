import ast
import json
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

def log_error_to_decisions(decisions_file: Path, reason: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n## BUILDER AGENT ERROR — {timestamp}\n**Error:** {reason}\n---\n"
    try:
        with open(decisions_file, "a", encoding="utf-8") as f: f.write(entry)
    except Exception as e:
        logger.error(f"Failed to append error to decisions.md: {e}")

def log_decision(decisions_file: Path, iteration: int, target: str, change_type: str, 
                 weak_metric: str, description: str, lines: list):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = (
        f"\n## Builder Agent — Iteration {iteration} — {timestamp}\n"
        f"**Target:** {target}\n**Change type:** {change_type}\n"
        f"**Weak metric:** {weak_metric}\n**Change:** {description}\n"
        f"**Lines modified:** {lines}\n---\n"
    )
    try:
        with open(decisions_file, "a", encoding="utf-8") as f: f.write(entry)
    except Exception as e:
        logger.error(f"Failed to append builder log to decisions.md: {e}")

def modify_json(content: str, change_type: str) -> tuple[str, list[int], str]:
    data = json.loads(content)
    if change_type == "reasoning_logic" and "thresholds" in data:
        data["thresholds"]["logic_margin"] = data["thresholds"].get("logic_margin", 0.5) + 0.05
        desc = "Increased logic_margin threshold by 0.05"
    elif change_type == "priority_rules" and "attack_priority" in data:
        data["attack_priority"]["base_value"] = data["attack_priority"].get("base_value", 10) + 1
        desc = "Increased base attack_priority threshold value by 1"
    else:
        data["last_metric_tweak"] = change_type
        desc = f"Tweaked last_metric_tweak config to {change_type}"
    return json.dumps(data, indent=2), [1], desc

def modify_python(content: str, change_type: str) -> tuple[str, list[int], str]:
    # verify AST correctness
    ast.parse(content)
    lines = content.splitlines()
    modified = False
    lines_modified = []
    
    for idx, line in enumerate(lines):
        if "threshold" in line.lower() and "=" in line and not modified:
            parts = line.split("=")
            try:
                val = float(parts[1].strip())
                lines[idx] = f"{parts[0]}= {val + 0.1}"
                lines_modified.append(idx + 1)
                desc = f"Incremented logic threshold parameter on line {idx + 1}"
                modified = True
            except ValueError:
                pass
    
    if not modified:
        lines.append(f"\n# BuilderAgent: Adjusted {change_type} threshold parameters")
        lines_modified = [len(lines)]
        desc = f"Appended {change_type} adjustment marker to bottom of file"
        
    return "\n".join(lines), lines_modified, desc
