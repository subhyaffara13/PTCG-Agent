import sys, os, time, subprocess, json
from pathlib import Path

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

ENABLE_DISTRIBUTED = False  # Toggle this to activate distributed mode

def main():
    print("--> Orchestration Agent started...")
    
    # Select which scripts to run depending on distributed mode status
    if ENABLE_DISTRIBUTED:
        scripts = [
            "scratch/distributed_master.py",
            "scratch/distributed_learner.py"
        ]
        print("Distributed training mode is ENABLED. Remote workers should connect to this node.")
    else:
        scripts = [
            "scratch/run_deck_optimizer_loop.py",
            "scratch/run_ppo_trainer_loop.py",
            "scratch/run_training_batches.py"
        ]
        print("Local training mode is ENABLED.")

    processes = []
    for script in scripts:
        try:
            p = subprocess.Popen([sys.executable, script])
            processes.append(p)
        except Exception as e:
            print(f"Failed to start {script}: {e}")

    try:
        from factory.teams.analytics_team import AnalyticsTeam
        analytics = AnalyticsTeam()
        iteration = 0
        while True:
            # Monitor sub-process health
            for i, p in enumerate(processes):
                if p.poll() is not None:
                    print(f"Sub-task {scripts[i]} stopped. Restarting...")
                    try:
                        processes[i] = subprocess.Popen([sys.executable, scripts[i]])
                    except Exception as e:
                        print(f"Failed to restart {scripts[i]}: {e}")

            print(f"\n--- [Orchestration] Checking standing & starting batch ---")
            try:
                subprocess.run([sys.executable, "scratch/check_submissions.py"], check=True)
                subprocess.run([sys.executable, "scratch/run_leaderboard_loop.py"], check=True)
            except Exception as e:
                print(f"Error checking online standings: {e}")

            if iteration % 5 == 0:
                try:
                    result_file = Path("logs/iteration_result.json")
                    if result_file.exists():
                        res_data = json.loads(result_file.read_text(encoding="utf-8"))
                        analytics.run_analysis(iteration_id=iteration, log_dir="logs", iteration_result=res_data, decks={"player_a": [], "player_b": []})
                        print("Analytics heavy check finished successfully.")
                except Exception as e:
                    print(f"Analytics Team execution failed: {e}")

            iteration += 1
            time.sleep(3600)
    finally:
        print("Cleaning up sub-tasks...")
        for p in processes:
            try:
                p.terminate()
                p.wait(timeout=5)
            except Exception:
                try: p.kill()
                except Exception: pass

if __name__ == "__main__":
    main()
