
def load_corpus() -> List[List[int]]:
    corpus = []
    try:
        with open("logs/kaggle_summary/scraped_decks.json", "r") as f:
            data = json.load(f)
            if "opp_win_decks" in data:
                corpus.extend(data["opp_win_decks"])
            if "us_win_decks" in data:
                corpus.extend(data["us_win_decks"])
    except FileNotFoundError:
        pass
    
    try:
        with open("logs/iteration_result.json", "r") as f:
            data = json.load(f)
            pass
    except FileNotFoundError:
        pass
        
    return corpus

