
def run_hourly_checks(iteration: int):
    """Runs leaderboard checks and auto-submission logic."""
    logger.info(f"--- [Orchestration] Hourly check #{iteration} ---")
    
    import os
    if not os.path.exists(".env") and not os.path.exists("kaggle.json"):
        logger.error("WARNING: Missing .env or kaggle.json! This worker promoted to Master but lacks Kaggle credentials. Skipping submissions.")
        return

    for script in ["scratch/check_submissions.py", "scratch/run_leaderboard_loop.py"]:
        log_path = script_log_path(script)
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                subprocess.run([sys.executable, script], stdout=f, stderr=f, check=True)
        except Exception as e:
            logger.error(f"Error running {script}: {e}")

    try:
        auto_submit_if_ready()
    except Exception as e:
        logger.error(f"Auto-submission error: {e}")

    # Run Kaggle Replay self-healing check using AnalyticsTeam
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        subs = api.competition_submissions("pokemon-tcg-ai-battle")
        if subs:
            subs.sort(key=lambda s: s.date, reverse=True)
            latest_sub = subs[0]
            sub_id = getattr(latest_sub, 'ref', None)
            if not sub_id:
                for attr in ['id', 'submission_id', 'submissionId', 'key']:
                    if hasattr(latest_sub, attr):
                        sub_id = getattr(latest_sub, attr)
                        break
            if sub_id:
                logger.info(f"Triggering AnalyticsTeam replay audit for Kaggle submission {sub_id}...")
                from factory.teams.analytics_team import AnalyticsTeam
                AnalyticsTeam().run_kaggle_analysis(sub_id)
            else:
                logger.warning("Could not find submission ID for latest submission.")
    except Exception as e:
        logger.error(f"Error running AnalyticsTeam Kaggle self-healing audit: {e}")

    try:
        from factory.deep_replay_inspector import DeepReplayInspector
        inspector = DeepReplayInspector()
        if 'sub_id' in locals() and sub_id:
            logger.info(f"Triggering DeepReplayInspector for latest losses in submission {sub_id}...")
            inspector.inspect_latest_losses(submission_id=sub_id)
    except ImportError:
        pass
    except Exception as e:
        logger.error(f"Error running DeepReplayInspector: {e}")

