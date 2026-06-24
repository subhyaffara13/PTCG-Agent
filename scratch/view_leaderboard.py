from kaggle.api.kaggle_api_extended import KaggleApi

def main():
    api = KaggleApi()
    api.authenticate()
    lb = api.competition_leaderboard_view('pokemon-tcg-ai-battle')
    print("TOP 15 LEADERBOARD:")
    for i, entry in enumerate(lb[:15]):
        tname = getattr(entry, "teamName", getattr(entry, "team_name", "Unknown"))
        safe_name = tname.encode('ascii', 'ignore').decode('ascii').strip()
        if not safe_name:
            safe_name = "[Unicode Team Name]"
        score = getattr(entry, "score", "N/A")
        print(f"{i+1}. Team: {safe_name}, Score: {score}")

if __name__ == "__main__":
    main()
