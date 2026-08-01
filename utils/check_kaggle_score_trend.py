
def check_kaggle_score_trend():
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        api = KaggleApi()
        api.authenticate()
        subs = api.competition_submissions("pokemon-tcg-ai-battle")
        if not subs:
            return {'divergence_detected': False}
        recent_subs = [s for s in subs if getattr(s, 'publicScore', None) is not None][:5]
        if len(recent_subs) < 3:
            return {'divergence_detected': False}
        scores = [float(s.publicScore) for s in recent_subs]
        if scores[0] < scores[1] and scores[1] < scores[2]:
            return {'divergence_detected': True, 'trend': 'declining', 'scores': scores}
        return {'divergence_detected': False}
    except Exception:
        return {'divergence_detected': False}

