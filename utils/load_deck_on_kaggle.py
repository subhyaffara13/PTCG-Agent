
def load_deck_on_kaggle(configuration=None):
    import csv
    import sys
    from pathlib import Path
    
    agent_dir = None
    if isinstance(configuration, dict) and configuration.get("__raw_path__"):
        agent_dir = Path(configuration["__raw_path__"]).parent
    
    if not agent_dir:
        for p in sys.path:
            if p and Path(p).joinpath("deck.csv").exists():
                agent_dir = Path(p)
                break
                
    if not agent_dir:
        curr_dir = Path(__file__).parent.resolve() if "__file__" in globals() and globals()["__file__"] else Path(os.getcwd())
        if curr_dir.joinpath("deck.csv").exists():
            agent_dir = curr_dir
            
    if not agent_dir:
        sys.stderr.write("[deck] Could not determine agent directory to load deck.csv. Using fallback.\n")
        return None
        
    deck_path = agent_dir / "deck.csv"
    sys.stderr.write(f"[deck] Loading deck from: {deck_path}\n")
    if not deck_path.exists():
        sys.stderr.write(f"[deck] deck.csv not found at {deck_path}\n")
        return None
        
    try:
        loaded_deck = []
        with open(deck_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                loaded_deck.extend([int(row["card_id"])] * int(row["count"]))
        if len(loaded_deck) == 60:
            sys.stderr.write(f"[deck] Successfully loaded deck from deck.csv (60 cards)\n")
            return loaded_deck
        else:
            sys.stderr.write(f"[deck] Loaded deck has invalid length: {len(loaded_deck)}\n")
    except Exception as e:
        sys.stderr.write(f"[deck] Error loading deck.csv: {e}\n")
    return None


def load_deck_on_kaggle(configuration=None):
    import csv
    import sys
    from pathlib import Path
    
    agent_dir = None
    if isinstance(configuration, dict) and configuration.get("__raw_path__"):
        agent_dir = Path(configuration["__raw_path__"]).parent
    
    if not agent_dir:
        for p in sys.path:
            if p and Path(p).joinpath("deck.csv").exists():
                agent_dir = Path(p)
                break
                
    if not agent_dir:
        curr_dir = Path(__file__).parent.resolve() if "__file__" in globals() and globals()["__file__"] else Path(os.getcwd())
        if curr_dir.joinpath("deck.csv").exists():
            agent_dir = curr_dir
            
    if not agent_dir:
        sys.stderr.write("[deck] Could not determine agent directory to load deck.csv. Using fallback.\n")
        return None
        
    deck_path = agent_dir / "deck.csv"
    sys.stderr.write(f"[deck] Loading deck from: {deck_path}\n")
    if not deck_path.exists():
        sys.stderr.write(f"[deck] deck.csv not found at {deck_path}\n")
        return None
        
    try:
        loaded_deck = []
        with open(deck_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                loaded_deck.extend([int(row["card_id"])] * int(row["count"]))
        if len(loaded_deck) == 60:
            sys.stderr.write(f"[deck] Successfully loaded deck from deck.csv (60 cards)\n")
            return loaded_deck
        else:
            sys.stderr.write(f"[deck] Loaded deck has invalid length: {len(loaded_deck)}\n")
    except Exception as e:
        sys.stderr.write(f"[deck] Error loading deck.csv: {e}\n")
    return None

