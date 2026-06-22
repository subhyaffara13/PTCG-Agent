"""
scratch/hourly_audit.py
Performs hourly audit of leaderboard, match history, and file line counts.
"""
import sys
import os
import subprocess
from pathlib import Path

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

def run_cmd(cmd: str):
    print(f"Executing: {cmd}")
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if res.stdout: print(res.stdout[-800:])
    if res.stderr: print(res.stderr[-800:])

def check_file_limits():
    print("\n--- LINE LIMITS AUDIT (Max 150 Lines) ---")
    limit_exceeded = False
    for p in Path(".").glob("**/*.py"):
        if any(x in p.parts for x in (".pytest_cache", "__pycache__", ".git", ".agents", "distributed", "visualizer")):
            continue
        try:
            lines = len(p.read_text(encoding="utf-8").splitlines())
            if lines > 150:
                print(f"  CRITICAL WARNING: {p} exceeds 150 lines ({lines} lines)!")
                limit_exceeded = True
            else:
                print(f"  {p}: {lines} lines")
        except Exception:
            pass
    if not limit_exceeded:
        print("All code files comply with the line count limits.")

def download_and_analyze_my_replays(api, sub_id):
    from factory.kaggle_scraper import KaggleScraper
    from factory.anti_pattern_extractor import AntiPatternExtractor
    from factory.do_pattern_extractor import DoPatternExtractor
    
    print(f"\n--- SCRAPING REPLAYS FOR ONLINE SUBMISSION {sub_id} ---")
    scraper = KaggleScraper(output_dir="logs/kaggle_replays")
    do_extractor = DoPatternExtractor(skills_dir="skills")
    anti_extractor = AntiPatternExtractor(logs_dir="logs", skills_dir="skills")
    
    try:
        episodes = api.competition_list_episodes(sub_id)
    except Exception as err:
        print(f"  Failed to retrieve episodes: {err}")
        return
        
    if not episodes:
        print("  No episodes found for this submission yet.")
        return
        
    my_losses, opponent_wins = [], []
    for ep in list(episodes)[:10]:
        ep_id = getattr(ep, 'id', None)
        agents = getattr(ep, 'agents', [])
        if not ep_id or len(agents) < 2:
            continue
            
        r0 = getattr(agents[0], 'reward', 0)
        r1 = getattr(agents[1], 'reward', 0)
        t0 = str(getattr(agents[0], 'team_id', getattr(agents[0], 'teamId', '')))
        t1 = str(getattr(agents[1], 'team_id', getattr(agents[1], 'teamId', '')))
        
        # If one agent lost and the other won:
        if r0 < 0 and r1 > 0:
            my_losses.append((ep_id, t0))
            opponent_wins.append((ep_id, t1))
        elif r1 < 0 and r0 > 0:
            my_losses.append((ep_id, t1))
            opponent_wins.append((ep_id, t0))
            
    print(f"  Identified {len(my_losses)} online losses. Downloading and analyzing...")
    downloaded_paths = []
    for ep_id, my_team in my_losses[:3]:
        p = scraper.download_episode_replay(ep_id)
        if p: downloaded_paths.append((Path(p), my_team))
        
    for p, my_team in downloaded_paths:
        try:
            anti_extractor.analyze_losing_replays([p], my_team)
        except Exception as e:
            print(f"  Error extracting anti-patterns: {e}")
            
    for (ep_id, opp_team), (p, _) in zip(opponent_wins[:len(downloaded_paths)], downloaded_paths):
        try:
            do_extractor.analyze_winning_replays([p], opp_team)
        except Exception as e:
            print(f"  Error extracting opponent win pattern: {e}")
            
    print("  Learned behavior patterns from online matches updated successfully.")

def check_online_submissions():
    print("\n--- ONLINE KAGGLE SUBMISSIONS STANDINGS ---")
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        subs = api.competition_submissions("pokemon-tcg-ai-battle")
        if subs:
            for s in list(subs)[:5]:
                score = getattr(s, 'public_score', getattr(s, 'publicScore', 'N/A'))
                status = getattr(s, 'status', 'N/A')
                date = getattr(s, 'date', 'N/A')
                desc = getattr(s, 'description', '')
                print(f"  ID: {s.ref} | Date: {date} | Status: {status} | Score: {score} | Desc: {desc[:50]}")
            
            # Learn from online matches of the latest submission
            latest_id = int(subs[0].ref)
            download_and_analyze_my_replays(api, latest_id)
        else:
            print("  No submissions found.")
    except Exception as e:
        print(f"  Failed to check online standings: {e}")

def main():
    print("==================================================")
    print("HOURLY AUDIT REPORT")
    print("==================================================")
    
    # 1. Run leaderboard check
    run_cmd("python scratch/run_leaderboard_loop.py")
    
    # 2. Check online submission standings & replays
    check_online_submissions()
    
    # 3. Check match history & win rates
    iter_file = Path("logs/iteration_result.json")
    if iter_file.exists():
        try:
            import json
            data = json.loads(iter_file.read_text(encoding="utf-8"))
            print(f"\n--- MATCH HISTORY (Iteration {data.get('iteration')}) ---")
            for k, g in data.get("games", {}).items():
                print(f"  {k}: Winner = {g.get('winner')}, Turns = {g.get('turns_taken')}")
        except Exception as e:
            print(f"Failed to read iteration result: {e}")
            
    # 4. Check line count standards
    check_file_limits()
    
    # 5. Rebuild submission package
    run_cmd("python build_submission.py")
    print("==================================================")

if __name__ == "__main__":
    main()
