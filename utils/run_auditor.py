import json
import os
import subprocess

def run_auditor():
    """Run bandit and flake8 to find issues."""
    logger.info("Auditor Agent: Running static analysis...")
    issues = []

    # 1. Run Bandit
    try:
        subprocess.run(
            ["bandit", "-r", "cb_agents", "factory", "router", "distributed", "-f", "json", "-o", "pipeline_bandit.json"],
            capture_output=True, text=True
        )
        if os.path.exists("pipeline_bandit.json"):
            with open("pipeline_bandit.json", "r") as f:
                data = json.load(f)
                for res in data.get("results", []):
                    if res["issue_severity"] in ["HIGH", "MEDIUM"]:
                        issues.append({
                            "file": res["filename"],
                            "line": res["line_number"],
                            "description": f"Bandit {res['test_id']}: {res['issue_text']}"
                        })
    except Exception as e:
        logger.error(f"Bandit failed: {e}")

    # 2. Run Flake8
    try:
        res = subprocess.run(
            ["flake8", "cb_agents", "factory", "router", "distributed"],
            capture_output=True, text=True
        )
        for line in res.stdout.splitlines():
            if " F" in line or " E9" in line: # Critical logic errors
                parts = line.split(":", 3)
                if len(parts) >= 4:
                    issues.append({
                        "file": parts[0],
                        "line": parts[1],
                        "description": f"Flake8: {parts[3].strip()}"
                    })
    except Exception as e:
        logger.error(f"Flake8 failed: {e}")

    return issues

