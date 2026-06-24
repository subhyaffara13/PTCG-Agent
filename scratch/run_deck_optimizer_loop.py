"""
scratch/run_deck_optimizer_loop.py
Runs the parallel deck optimizer in a continuous background loop, decoupled from training.
Stops if fitness plateaus (no improvement for 5 consecutive runs).
"""
import time
import json
import subprocess
from pathlib import Path

def get_best_fitness() -> float:
    p = Path("logs/best_fitness.json")
    if p.exists():
        try: return float(json.loads(p.read_text(encoding="utf-8")).get("best_fitness", -9999.0))
        except Exception: pass
    return -9999.0

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
                
                # Check for plateau
                new_fit = get_best_fitness()
                if new_fit > global_best + 0.1:
                    print(f"Improvement found! Fitness increased from {global_best:.2f} to {new_fit:.2f}")
                    global_best = new_fit
                    consec_no_imp = 0
                else:
                    consec_no_imp += 1
                    print(f"No significant improvement. Fitness: {new_fit:.2f} (Global Best: {global_best:.2f}). Consec runs: {consec_no_imp}/5")
                    
                if consec_no_imp >= 5:
                    print("PLATEAU DETECTED: No improvement for 5 consecutive runs. Triggering plateau fix...")
                    backup_path = Path("agents/deck_new_backup.csv")
                    current_deck = Path("agents/deck_new.csv")
                    if current_deck.exists():
                        if backup_path.exists(): backup_path.unlink()
                        current_deck.rename(backup_path)
                    print("Diversity Injection: Erasing seed deck to restart search from Kaggle winning templates.")
                    subprocess.run("python scratch/deck_optimizer.py", shell=True, check=True)
                    new_fit = get_best_fitness()
                    if new_fit > global_best:
                        print(f"Plateau successfully broken! New fitness: {new_fit:.2f} > {global_best:.2f}")
                        global_best = new_fit
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
