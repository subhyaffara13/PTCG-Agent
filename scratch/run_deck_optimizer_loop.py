"""
scratch/run_deck_optimizer_loop.py
Runs the parallel deck optimizer in a continuous background loop, decoupled from training.
Stops if fitness plateaus (no improvement for 5 consecutive runs).

Option 3 Co-Evolution: After each successful deck promotion, triggers a PPO training step
so the policy model is retrained on games played with the newly discovered dominant deck.
"""
import time
import json
import subprocess
import sys
import os
from pathlib import Path

# Make sure the project root is on sys.path so we can import run_guided_helpers
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _root not in sys.path:
    sys.path.insert(0, _root)

CO_EVOLVE_PPO = True   # Set False to disable co-evolution (deck opt only)

def get_best_fitness() -> float:
    p = Path("logs/best_fitness.json")
    if p.exists():
        try: return float(json.loads(p.read_text(encoding="utf-8")).get("best_fitness", -9999.0))
        except Exception: pass
    return -9999.0

def trigger_ppo_update():
    """Co-evolution step: retrain PPO on the latest game logs after a deck promotion."""
    print("CO-EVOLUTION: Triggering PPO update after deck promotion...")
    try:
        from run_guided_helpers import execute_ppo_step, get_last_iteration_id
        # Temporarily disable FAST_SIM_MODE so PPO has access to the full pipeline
        orig = os.environ.get("FAST_SIM_MODE")
        os.environ["FAST_SIM_MODE"] = "false"
        try:
            last_iter = get_last_iteration_id()
            execute_ppo_step(last_iter)
            print(f"CO-EVOLUTION: PPO update complete (iteration {last_iter}).")
        finally:
            if orig is not None:
                os.environ["FAST_SIM_MODE"] = orig
            else:
                os.environ.pop("FAST_SIM_MODE", None)
    except Exception as e:
        print(f"CO-EVOLUTION: PPO update failed (non-fatal): {e}")

def main():
    print("Starting Decoupled Deck Optimizer Loop with Plateau Detection...")
    last_mod = 0.0
    telemetry_path = Path("logs/kaggle_summary/scraped_decks.json")

    consec_no_imp = 0
    global_best = get_best_fitness()

    while True:
        current_mod = telemetry_path.stat().st_mtime if telemetry_path.exists() else 0.0
        if current_mod != last_mod:
            print(f"New telemetry detected! Running supercharged genetic search...")
            try:
                subprocess.run("python scratch/deck_optimizer.py", shell=True, check=True)
                last_mod = current_mod

                # Check for improvement
                new_fit = get_best_fitness()
                if new_fit > global_best + 0.1:
                    print(f"Improvement found! Fitness increased from {global_best:.2f} to {new_fit:.2f}")
                    global_best = new_fit
                    consec_no_imp = 0
                    # Co-evolution: retrain PPO policy on new deck's games
                    if CO_EVOLVE_PPO:
                        trigger_ppo_update()
                else:
                    consec_no_imp += 1
                    print(f"No significant improvement. Fitness: {new_fit:.2f} (Global Best: {global_best:.2f}). Consec runs: {consec_no_imp}/5")

                if consec_no_imp >= 5:
                    print("PLATEAU DETECTED: No improvement for 5 consecutive runs. Triggering plateau fix...")
                    backup_path = Path("cb_agents/deck_new_backup.csv")
                    current_deck = Path("cb_agents/deck_new.csv")
                    if current_deck.exists():
                        if backup_path.exists(): backup_path.unlink()
                        current_deck.rename(backup_path)
                    print("Diversity Injection: Erasing seed deck to restart search from Kaggle winning templates.")
                    subprocess.run("python scratch/deck_optimizer.py", shell=True, check=True)
                    new_fit = get_best_fitness()
                    if new_fit > global_best:
                        print(f"Plateau successfully broken! New fitness: {new_fit:.2f} > {global_best:.2f}")
                        global_best = new_fit
                        # Co-evolution after plateau break too
                        if CO_EVOLVE_PPO:
                            trigger_ppo_update()
                    else:
                        print("Plateau fix did not exceed previous best. Restoring backup deck.")
                        if backup_path.exists():
                            if current_deck.exists(): current_deck.unlink()
                            backup_path.rename(current_deck)
                    consec_no_imp = 0
            except subprocess.CalledProcessError as e:
                print(f"Deck optimizer execution failed: {e}")
        time.sleep(15)

if __name__ == "__main__":
    main()
