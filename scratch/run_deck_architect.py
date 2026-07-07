import sys
import os
from pathlib import Path

if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())

from factory.deck_architect import DeckArchitect
from factory.deck_loader import DeckLoader

def main():
    print("Initializing DeckArchitect...")
    architect = DeckArchitect()
    
    print("Building a new aggro deck...")
    res = architect.build({"next_eval_context": "aggro"})
    print("Result:", res)
    
    deck_path = Path("staging/deck_new.csv")
    if not deck_path.exists():
        print("Error: staging/deck_new.csv was not generated!")
        return
        
    print("\nGenerated Deck:")
    lines = deck_path.read_text(encoding="utf-8").splitlines()
    header = lines[0].split(",")
    
    pkmn = []
    trainers = []
    energies = []
    
    import csv
    with open(deck_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cname = row["card_name"]
            ctype = row["card_type"]
            count = int(row["count"])
            if ctype == "Pokemon":
                pkmn.append((cname, count))
            elif ctype == "Trainer":
                trainers.append((cname, count))
            elif ctype == "Energy":
                energies.append((cname, count))
                
    total_pkmn = sum(c for _, c in pkmn)
    total_trainers = sum(c for _, c in trainers)
    total_energies = sum(c for _, c in energies)
    
    print(f"Total Pokemon: {total_pkmn}")
    for name, c in pkmn:
        print(f"  - {name} (x{c})")
        
    print(f"Total Trainers: {total_trainers}")
    for name, c in trainers:
        print(f"  - {name} (x{c})")
        
    print(f"Total Energies: {total_energies}")
    for name, c in energies:
        print(f"  - {name} (x{c})")
        
    print(f"\nTotal Deck Size: {total_pkmn + total_trainers + total_energies}")

if __name__ == "__main__":
    main()
