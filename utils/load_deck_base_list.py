
def load_deck_base_list(skills_dir: Path) -> dict:
    """Loads base deck counts from deck_new.csv or deck.csv."""
    for filename in ["cb_agents/deck_new.csv", "deck.csv"]:
        path = Path(filename)
        if not path.exists():
            path = skills_dir.parent / filename
        if path.exists():
            try:
                deck_dict = {}
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        deck_dict[int(row["card_id"])] = int(row["count"])
                return deck_dict
            except Exception as e:
                logger.warning(f"Deck CSV load failed for {path}: {e}")
    return {}


def load_deck_base_list(skills_dir: Path) -> dict:
    """Loads base deck counts from deck_new.csv or deck.csv."""
    for filename in ["cb_agents/deck_new.csv", "deck.csv"]:
        path = Path(filename)
        if not path.exists():
            path = skills_dir.parent / filename
        if path.exists():
            try:
                deck_dict = {}
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        deck_dict[int(row["card_id"])] = int(row["count"])
                return deck_dict
            except Exception as e:
                logger.warning(f"Deck CSV load failed for {path}: {e}")
    return {}


def load_deck_base_list(skills_dir: Path) -> dict:
    """Loads base deck counts from deck_new.csv or deck.csv."""
    for filename in ["cb_agents/deck_new.csv", "deck.csv"]:
        path = Path(filename)
        if not path.exists():
            path = skills_dir.parent / filename
        if path.exists():
            try:
                deck_dict = {}
                with open(path, "r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        deck_dict[int(row["card_id"])] = int(row["count"])
                return deck_dict
            except:
                pass
    return {}

