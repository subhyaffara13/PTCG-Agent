import time

def _check_submission_budget():
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        logger.warning("Kaggle API not available. Skipping auto-submit.")
        return None, None
    api = None; subs = None
    for attempt in range(3):
        try:
            api = KaggleApi()
            api.authenticate()
            subs = api.competition_submissions("pokemon-tcg-ai-battle")
            break
        except Exception as e:
            if attempt == 2:
                logger.error(f"Kaggle auth/query failed after 3 attempts: {e}")
                return None, None
            logger.warning(f"Kaggle query failed (attempt {attempt+1}), retrying in {2**attempt}s...: {e}")
            time.sleep(2**attempt)
    return api, subs

