import csv
from pathlib import Path

def main():
    csv_path = Path("skills/card_pool_raw.csv")
    if not csv_path.exists():
        print("CSV not found")
        return
        
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row.get("Card ID", "").strip()
            if cid in ("957", "979", "210"):
                print(f"Card {cid}: {row.get('Card Name')} | Type: {repr(row.get('Type'))}")

if __name__ == "__main__":
    main()
