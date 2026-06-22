from kaggle.api.kaggle_api_extended import KaggleApi

def main():
    api = KaggleApi()
    api.authenticate()
    
    subs = api.competition_submissions("pokemon-tcg-ai-battle")
    print(f"Found {len(subs)} submissions.")
    for s in subs:
        if str(s.status) == "SubmissionStatus.COMPLETE" or s.status == "complete":
            print(f"ID: {s.ref}, Date: {s.date}, Score: {s.public_score}, Desc: {s.description[:120] if s.description else ''}")

if __name__ == "__main__":
    main()
