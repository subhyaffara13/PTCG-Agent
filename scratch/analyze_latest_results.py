import json
from pathlib import Path

def main():
    p = Path("logs/iteration_result.json")
    if not p.exists():
        print("No iteration results found.")
        return
        
    data = json.loads(p.read_text(encoding="utf-8"))
    print(f"Iteration: {data.get('iteration')}")
    print(f"Timestamp: {data.get('timestamp')}")
    
    games = data.get("games", {})
    
    deck_wins_a = 0
    deck_wins_b = 0
    var_wins_a = 0
    var_wins_b = 0
    
    for label, g in games.items():
        winner = g.get("winner")
        if label.startswith("deck_test"):
            if winner == "player_a": deck_wins_a += 1
            elif winner == "player_b": deck_wins_b += 1
        elif label.startswith("variance_baseline"):
            if winner == "player_a": var_wins_a += 1
            elif winner == "player_b": var_wins_b += 1
            
    print(f"\nDeck Tests (Candidate vs Baseline):")
    print(f"  Candidate Wins (Player B): {deck_wins_b}")
    print(f"  Baseline Wins (Player A): {deck_wins_a}")
    print(f"  Candidate Win Rate: {deck_wins_b / max(1, deck_wins_a + deck_wins_b) * 100:.1f}%")
    
    print(f"\nVariance Baselines (Baseline vs Baseline):")
    print(f"  Baseline A Wins: {var_wins_a}")
    print(f"  Baseline B Wins: {var_wins_b}")
    print(f"  Ratio: {var_wins_a}:{var_wins_b}")

if __name__ == "__main__":
    main()
