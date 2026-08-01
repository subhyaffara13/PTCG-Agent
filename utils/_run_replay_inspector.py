
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

