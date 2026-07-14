import json
import sys
from kaggle.api.kaggle_api_extended import KaggleApi

sys.path.insert(0, "C:/Users/subhy/.gemini/antigravity/scratch/ptcg-agent")

api = KaggleApi()
api.authenticate()
subs = api.competition_submissions("pokemon-tcg-ai-battle")
subs.sort(key=lambda s: s.date, reverse=True)

for i, s in enumerate(subs[:5]):
    ref = getattr(s, 'ref', None)
    status = getattr(s, 'status', None)
    desc = getattr(s, 'description', None)
    score = getattr(s, 'publicScore', getattr(s, 'public_score', None))
    print(f"[{i}] Ref: {ref} | Status: {status} | Score: {score} | Date: {s.date} | Desc: {desc}")
