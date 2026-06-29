import json, logging
from pathlib import Path
logger = logging.getLogger(__name__)


def check_file_limits():
    print("\n--- LINE LIMITS AUDIT (Max 100 Lines) ---")
    exceeded = False
    refactor_queue = []
    queue_path = Path("logs/refactor_queue.json")
    if queue_path.exists():
        try:
            refactor_queue = json.loads(queue_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    for p in Path(".").glob("**/*.py"):
        if any(x in p.parts for x in (".pytest_cache", "__pycache__", ".git", ".agents", "distributed", "visualizer", "skills")):
            continue
        try:
            lines = len(p.read_text(encoding="utf-8").splitlines())
            if lines > 100:
                print(f"  CRITICAL WARNING: {p} exceeds 100 lines ({lines} lines)!")
                exceeded = True
                if str(p) not in refactor_queue:
                    refactor_queue.append(str(p))
            else:
                pass
        except Exception:
            pass

    if refactor_queue:
        queue_path.write_text(json.dumps(refactor_queue, indent=2), encoding="utf-8")

    if not exceeded:
        print("All code files comply with the 100-line count limits.")


def download_and_analyze_my_replays(api, sub_id):
    from factory.kaggle_scraper import KaggleScraper
    from factory.anti_pattern_extractor import AntiPatternExtractor
    from factory.do_pattern_extractor import DoPatternExtractor
    print(f"\n--- SCRAPING REPLAYS FOR ONLINE SUBMISSION {sub_id} ---")
    scraper = KaggleScraper(output_dir="logs/kaggle_replays")
    do_ext = DoPatternExtractor(skills_dir="skills")
    anti_ext = AntiPatternExtractor(logs_dir="logs", skills_dir="skills")
    try:
        episodes = api.competition_list_episodes(sub_id)
    except Exception as err:
        print(f"  Failed to retrieve episodes: {err}"); return
    if not episodes:
        print("  No episodes found for this submission yet."); return
    my_losses, opp_wins = [], []
    for ep in list(episodes)[:10]:
        ep_id, agents = getattr(ep, 'id', None), getattr(ep, 'agents', [])
        if not ep_id or len(agents) < 2: continue
        r0, r1 = getattr(agents[0], 'reward', 0), getattr(agents[1], 'reward', 0)
        t0 = str(getattr(agents[0], 'team_id', getattr(agents[0], 'teamId', '')))
        t1 = str(getattr(agents[1], 'team_id', getattr(agents[1], 'teamId', '')))
        if r0 < 0 and r1 > 0:
            my_losses.append((ep_id, t0)); opp_wins.append((ep_id, t1))
        elif r1 < 0 and r0 > 0:
            my_losses.append((ep_id, t1)); opp_wins.append((ep_id, t0))
    print(f"  Identified {len(my_losses)} online losses. Downloading and analyzing...")
    downloaded = []
    for ep_id, my_team in my_losses[:3]:
        try:
            p = scraper.download_episode_replay(ep_id)
            if p: downloaded.append((Path(p), my_team))
        except Exception as e:
            logger.warning("Failed to download episode %s: %s", ep_id, e)
    meta = {"anti_patterns": [], "do_patterns": []}
    for p, my_team in downloaded:
        try:
            anti = anti_ext.analyze_losing_replays([p], my_team)
            if anti: meta["anti_patterns"].extend(anti)
        except Exception as e:
            print(f"  Error extracting anti-patterns: {e}")
    for (ep_id, opp_team), (p, _) in zip(opp_wins[:len(downloaded)], downloaded):
        try:
            pts = do_ext.analyze_winning_replays([p], opp_team)
            if pts: meta["do_patterns"].extend(pts)
        except Exception as e:
            print(f"  Error extracting opponent win pattern: {e}")
    print("  Learned behavior patterns from online matches updated successfully.")
    return meta


def check_online_submissions():
    print("\n--- ONLINE KAGGLE SUBMISSIONS STANDINGS ---")
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi(); api.authenticate()
        subs = api.competition_submissions("pokemon-tcg-ai-battle")
        if not subs: print("  No submissions found."); return
        for s in list(subs)[:5]:
            score = getattr(s, 'public_score', getattr(s, 'publicScore', 'N/A'))
            status = getattr(s, 'status', 'N/A')
            date = getattr(s, 'date', 'N/A')
            desc = getattr(s, 'description', '')
            print(f"  ID: {s.ref} | Date: {date} | Status: {status} | Score: {score} | Desc: {desc[:50]}")
        meta = download_and_analyze_my_replays(api, int(subs[0].ref))
        if not meta: return
        print("  Triggering Architecture and Development Teams with Kaggle Meta-Summary...")
        from factory.teams.development_team import DevelopmentTeam
        from factory.teams.architecture_team import ArchitectureTeam
        DevelopmentTeam().run_kaggle_development(meta)
        ArchitectureTeam().execute_adjustments(meta)
        Path("logs/hourly_meta_audit.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"  Failed to check online standings: {e}")
