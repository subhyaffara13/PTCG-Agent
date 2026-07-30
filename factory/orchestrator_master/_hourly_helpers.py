def _run_kaggle_check():
    import logging
    logger = logging.getLogger("orchestration_agent")
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi(); api.authenticate()
        subs = api.competition_submissions("pokemon-tcg-ai-battle")
        if subs:
            subs.sort(key=lambda s: s.date, reverse=True)
            latest_sub = subs[0]
            sub_id = getattr(latest_sub, 'ref', None)
            if not sub_id:
                for attr in ['id', 'submission_id', 'submissionId', 'key']:
                    if hasattr(latest_sub, attr): sub_id = getattr(latest_sub, attr); break
            if sub_id:
                logger.info(f"Triggering AnalyticsTeam replay audit for Kaggle submission {sub_id}...")
                from factory.teams.analytics_team import AnalyticsTeam
                AnalyticsTeam().run_kaggle_analysis(sub_id)
            else: logger.warning("Could not find submission ID for latest submission.")
    except Exception as e: logger.error(f"Error running AnalyticsTeam Kaggle self-healing audit: {e}")
    return sub_id if 'sub_id' in dir() else None

def _run_replay_inspector(sub_id):
    import logging
    logger = logging.getLogger("orchestration_agent")
    try:
        from factory.deep_replay_inspector import DeepReplayInspector
        inspector = DeepReplayInspector()
        if sub_id:
            logger.info(f"Triggering DeepReplayInspector for latest losses in submission {sub_id}...")
            inspector.inspect_latest_losses(submission_id=sub_id)
    except ImportError: pass
    except Exception as e: logger.error(f"Error running DeepReplayInspector: {e}")
