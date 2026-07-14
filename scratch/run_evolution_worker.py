import os
import shutil
import subprocess
import time
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - EvolutionWorker - %(levelname)s - %(message)s")
logger = logging.getLogger("evolution_worker")

def safe_evolve():
    main_dir = Path(__file__).resolve().parent.parent
    evolve_dir = main_dir.parent / (main_dir.name + "_evolve_workspace")
    
    logger.info(f"Setting up isolated evolution workspace at {evolve_dir}...")
    
    # 1. Copy current codebase to isolated directory (exclude heavy logs/models)
    if evolve_dir.exists():
        shutil.rmtree(evolve_dir, ignore_errors=True)
    
    def ignore_patterns(path, names):
        ignored = []
        for n in names:
            if n in ("logs", "models", ".git", ".env", "temp", "__pycache__", ".venv"):
                ignored.append(n)
        return ignored

    shutil.copytree(main_dir, evolve_dir, ignore=ignore_patterns)
    
    # 2. Run the evolution script inside the isolated workspace
    logger.info("Launching Active Evolution in isolated workspace...")
    evolve_script = evolve_dir / "scratch" / "run_active_evolution.py"
    
    try:
        # We run the script. If it rejects the mutation, it exits with 0 but restores backup.
        # So we just check if the target file was modified compared to main_dir.
        subprocess.run(["python", str(evolve_script)], cwd=evolve_dir, check=True)
        
        # 3. Compare evolved file with main file
        target_file = "cb_agents/turn_planner_sort.py"
        evolved_file = evolve_dir / target_file
        main_file = main_dir / target_file
        
        if evolved_file.exists() and main_file.exists():
            with open(evolved_file, "r", encoding="utf-8") as f1, open(main_file, "r", encoding="utf-8") as f2:
                if f1.read() != f2.read():
                    logger.info("Evolution successful! A superior mutation was found and verified.")
                    logger.info(f"Porting mutated {target_file} back to main workspace...")
                    shutil.copy2(evolved_file, main_file)
                    
                    # 4. Optional: We can signal the Master Orchestrator to restart workers here!
                    # For now, next time a worker spawns, it will read the new file.
                else:
                    logger.info("Evolution cycle completed, but no superior mutation was found. Code remains unchanged.")
                    
    except subprocess.CalledProcessError as e:
        logger.error(f"Evolution script crashed or failed: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during evolution: {e}")
        
    logger.info("Cleaning up isolated workspace...")
    shutil.rmtree(evolve_dir, ignore_errors=True)

if __name__ == "__main__":
    logger.info("Starting Self-Sustaining Evolution Worker...")
    while True:
        safe_evolve()
        logger.info("Sleeping for 1 hour before next evolution cycle...")
        time.sleep(3600)
