import os
import sys
import shutil
import subprocess
import time
import logging
import re
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - BugHunter - %(levelname)s - %(message)s")
logger = logging.getLogger("bug_hunter")

def extract_crash_info(log_path: Path):
    """Scans the crash log for the most recent unhandled exception."""
    if not log_path.exists():
        return None, None
        
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        if not content.strip():
            return None, None
            
        # Split by crash report header
        reports = content.split("--- CRASH REPORT AT")
        if len(reports) < 2:
            return None, None
            
        latest_report = reports[-1]
        
        # Find the last file in the stack trace that belongs to our codebase
        # Looking for lines like: File "C:\...\cb_agents\something.py", line 42, in ...
        file_pattern = r'File\s+"([^"]+)",\s+line\s+\d+,'
        matches = list(re.finditer(file_pattern, latest_report))
        
        target_file = None
        for match in reversed(matches):
            filepath = match.group(1)
            # Only patch files we own
            if "cb_agents" in filepath or "factory" in filepath:
                # Get relative path
                try:
                    target_file = filepath.split("ptcg-agent")[1].lstrip("\\/")
                except IndexError:
                    if "cb_agents" in filepath:
                        target_file = "cb_agents/" + filepath.split("cb_agents")[-1].lstrip("\\/")
                    elif "factory" in filepath:
                        target_file = "factory/" + filepath.split("factory")[-1].lstrip("\\/")
                break
                
        return target_file, latest_report.strip()
    except Exception as e:
        logger.error(f"Failed to parse crash log: {e}")
        return None, None

def clear_crash_log(log_path: Path):
    """Clears the log so we don't fix the same bug twice in a loop."""
    try:
        if log_path.exists():
            log_path.write_text("", encoding="utf-8")
    except Exception:
        pass

def hunt_bugs():
    main_dir = Path(__file__).resolve().parent.parent
    crash_log = main_dir / "logs" / "crash_report.log"
    
    target_file, crash_trace = extract_crash_info(crash_log)
    
    if not target_file:
        logger.info("No actionable crashes found in logs. System looks healthy.")
        return
        
    logger.warning(f"CRASH DETECTED! Culprit file identified: {target_file}")
    
    # 1. Setup sandbox
    sandbox_dir = main_dir.parent / (main_dir.name + "_bughunter_workspace")
    logger.info(f"Setting up isolated bug-hunter workspace at {sandbox_dir}...")
    
    if sandbox_dir.exists():
        shutil.rmtree(sandbox_dir, ignore_errors=True)
    
    def ignore_patterns(path, names):
        return [n for n in names if n in ("logs", "models", ".git", ".env", "temp", "__pycache__", ".venv")]

    shutil.copytree(main_dir, sandbox_dir, ignore=ignore_patterns)
    
    try:
        # Import mutator from sandbox to avoid locking main files
        import sys as _sys
        sys_path_backup = list(_sys.path)
        _sys.path.insert(0, str(sandbox_dir))
        
        from cb_agents.code_mutator import request_code_mutation_from_llm  # type: ignore
        
        sandbox_target = sandbox_dir / target_file
        if not sandbox_target.exists():
            logger.error(f"Target file {target_file} not found in sandbox.")
            return
            
        logger.info("Requesting LLM patch for the crashed file...")
        
        prompt = f"""
        The system crashed with the following unhandled exception:
        {crash_trace}
        
        This stack trace points to {target_file} as the culprit. 
        Please provide a completely fixed, robust rewrite of {target_file} that resolves this crash.
        Ensure it handles None-types, missing dict keys, or edge cases gracefully.
        """
        
        mutated_code = request_code_mutation_from_llm(sandbox_target, prompt)
        
        if not mutated_code:
            logger.error("LLM failed to provide a patch.")
            return
            
        logger.info("Applying patch to sandbox...")
        sandbox_target.write_text(mutated_code, encoding="utf-8")
        
        logger.info("Running pytest guardrails...")
        test_res = subprocess.run(["pytest"], cwd=sandbox_dir, capture_output=True, text=True)
        
        if test_res.returncode == 0:
            logger.info("Pytest passed! The patch did not break the test suite.")
            main_target = main_dir / target_file
            
            logger.info(f"Porting fixed {target_file} back to main workspace...")
            shutil.copy2(sandbox_target, main_target)
            
            # Clear crash log so we don't get stuck in a loop
            clear_crash_log(crash_log)
            logger.info("Bug successfully squashed!")
        else:
            logger.warning("The LLM patch failed the test suite! Rejecting mutation.")
            logger.warning(f"Pytest Output: {test_res.stdout[-500:]}")
            
    except Exception as e:
        logger.error(f"Bug hunting failed: {e}")
    finally:
        import sys
        if str(sandbox_dir) in sys.path:
            sys.path.remove(str(sandbox_dir))
        logger.info("Cleaning up isolated workspace...")
        shutil.rmtree(sandbox_dir, ignore_errors=True)

if __name__ == "__main__":
    logger.info("Starting Autonomous Bug Hunter Worker...")
    while True:
        hunt_bugs()
        logger.info("Sleeping for 30 minutes before next sweep...")
        time.sleep(1800)
