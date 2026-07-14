import sys
import json
from pathlib import Path

# Add project root to sys.path
cwd = str(Path(__file__).parent.parent.resolve())
if cwd not in sys.path:
    sys.path.insert(0, cwd)

from scratch.deck_setup import load_optimizer_data

def main():
    try:
        data_dict = load_optimizer_data()
        empirical_core = data_dict["empirical_core"]
        flex_pool = empirical_core.flex_pool
        print(f"Flex pool size: {len(flex_pool)}")
        
        # Load card names
        from factory.deck_loader import DeckLoader
        loader = DeckLoader(Path("skills"))
        pool = loader.load_card_pool()
        card_names = {int(c["card_id"]): c.get("card_name", f"Card {c['card_id']}") for c in pool if str(c.get("card_id", "")).isdigit()}
        
        # Find which energy cards are in flex_pool
        energies_in_flex = []
        for cid in flex_pool:
            card_name = card_names.get(cid, f"Card {cid}")
            # Check card type
            card_dict = next((c for c in pool if int(c["card_id"]) == cid), None)
            if card_dict and card_dict.get("card_type") == "Energy":
                energies_in_flex.append((cid, card_name))
                
        print("\nEnergy cards present in flex_pool:")
        for cid, name in energies_in_flex:
            print(f"  - {cid}: {name}")
            
    except Exception as e:
        print(f"Error during inspection: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
