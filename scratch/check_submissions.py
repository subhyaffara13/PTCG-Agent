import os
from dotenv import load_dotenv
load_dotenv()

from kaggle.api.kaggle_api_extended import KaggleApi

def main():
    import time
    for attempt in range(3):
        try:
            api = KaggleApi()
            api.authenticate()
            break
        except Exception as e:
            if attempt == 2: raise
            time.sleep(2**attempt)
    subs = api.competition_submissions("pokemon-tcg-ai-battle")
    print(f"Found {len(subs)} submissions.")
    for s in subs:
        print(f"ID: {s.ref}, Status: {s.status}, Date: {s.date}, Score: {s.public_score}, Desc: {s.description[:120] if s.description else ''}")

if __name__ == "__main__":
    main()
