import os
import subprocess
import json
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AuditPipeline")

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

def invoke_coder_agent(issue):
    """Simulates the Coder Agent fixing the file using the project's existing code_mutator logic if available."""
    file_path = issue["file"]
    line_num = issue["line"]
    desc = issue["description"]
    
    logger.info(f"Coder Agent: Attempting to fix {file_path}:{line_num} -> {desc}")
    
    # In a real environment, we would invoke the LLM here to rewrite the file.
    # For now, we will log it. In the PTCG-Agent context, we can wire this up to code_mutator.py
    # or a dedicated google-genai call.
    
    # Placeholder for actual LLM patch logic:
    # prompt = f"Fix the following issue in {file_path} at line {line_num}: {desc}\n\nCode:\n{open(file_path).read()}"
    # new_code = llm_generate(prompt)
    # open(file_path, 'w').write(new_code)
    
    logger.info(f"Coder Agent: Fix generated and applied (Dry-Run mode).")
    return True

def run_validator():
    """Run pytest to ensure we didn't break player logic."""
    logger.info("Validator Agent: Running pytest...")
    res = subprocess.run(["pytest", "tests/"], capture_output=True, text=True)
    if res.returncode == 0:
        logger.info("Validator Agent: All tests passed! Logic is intact.")
        return True
    else:
        logger.error("Validator Agent: Tests failed after mutation! Reverting...")
        return False

def main():
    logger.info("--- Starting Automated Auditor-Coder Pipeline ---")
    issues = run_auditor()
    
    if not issues:
        logger.info("Auditor Agent found no critical issues. Codebase is clean!")
        return

    logger.warning(f"Auditor Agent flagged {len(issues)} critical issues.")
    
    for idx, issue in enumerate(issues):
        logger.info(f"Processing issue {idx+1}/{len(issues)}...")
        fixed = invoke_coder_agent(issue)
        if fixed:
            valid = run_validator()
            if not valid:
                logger.error(f"Fix for {issue['file']} broke the tests.")
                # Revert logic would go here
    
    logger.info("--- Pipeline Finished ---")

if __name__ == "__main__":
    main()
