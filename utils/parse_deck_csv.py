
def parse_deck_csv(eval_deck):
    deck_path = Path(eval_deck)
    if not deck_path.exists():
        return [1] * 60
    deck_ids = []
    try:
        with open(eval_deck, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if not row or not any(cell.strip() for cell in row):
                    continue
                card_id_str = row[0].strip()
                count = int(row[3])
                card_id = int(card_id_str) if card_id_str.isdigit() else 1
                deck_ids.extend([card_id] * count)
    except Exception as e:
        logger.error(f"Error parsing deck CSV {eval_deck}: {e}")
        deck_ids = [1] * 60
    if len(deck_ids) != 60:
        deck_ids = (deck_ids + [1] * 60)[:60]
    return deck_ids

