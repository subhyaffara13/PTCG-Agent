import csv
import json
from pathlib import Path
from collections import Counter

from factory.deck_loader import DeckLoader
from scratch.deck_clustering import filter_pool_by_archetype
from dataclasses import dataclass
from typing import Dict, List, Set
from scratch.deck_synergy_graph import get_global_synergy_graph

@dataclass
class EmpiricalCore:
    locked_cards: Dict[int, int]
    flex_pool: List[int]
    core_engines: List[Set[int]]
    locked_count: int

def load_optimizer_data(archetype: str = None):
    loader = DeckLoader(Path("skills"))
    pool_cards = loader.load_card_pool()
    details = loader.parse_card_details(pool_cards)
    data = json.loads(Path("logs/kaggle_summary/scraped_decks.json").read_text(encoding="utf-8"))
    w_opp, w_us, l_us = data.get("opp_wins", {}), data.get("us_wins", {}), data.get("us_losses", {})
    winning_decks = data.get("opp_win_decks", []) + data.get("us_win_decks", [])

    opp_types = [details.get(str(cid), {}).get("element_type", "") for dk in data.get("opp_win_decks", []) for cid in dk]
    dominant_type = Counter(x for x in opp_types if x).most_common(1)
    bonus_type = {"{L}": "{F}", "{R}": "{W}", "{W}": "{L}", "{D}": "{F}", "{P}": "{D}", "{G}": "{R}"}.get(dominant_type[0][0]) if dominant_type else None

    winning_freq = Counter(int(cid) for dk in winning_decks for cid in dk)

    # Functional clustering: reduce pool to ~200 cards for the chosen archetype
    if archetype:
        pool_cards = filter_pool_by_archetype(pool_cards, details, archetype)
        print(f"[Setup] Filtered pool to {len(pool_cards)} cards for archetype={archetype}")

    scores = {str(c["card_id"]): float(c.get("ev_score", 0.5)) + 2.0 * w_opp.get(str(c["card_id"]), 0) + 1.0 * w_us.get(str(c["card_id"]), 0) - 1.5 * l_us.get(str(c["card_id"]), 0) + 3.0 * winning_freq.get(int(c["card_id"]), 0) + (15.0 if bonus_type and details.get(str(c["card_id"]), {}).get("element_type") == bonus_type else 0.0) for c in pool_cards}

    id_map = {int(c["card_id"]): c for c in pool_cards if str(c.get("card_id", "")).isdigit()}
    winning_ids = set().union(*winning_decks)
    allowed_types = {details.get(str(cid), {}).get("element_type") for cid in winning_ids if details.get(str(cid), {}).get("element_type")}

    pokemon_pool = sorted([c for c in pool_cards if c.get("card_type") == "Pokemon" and str(details.get(str(c.get("card_id")), {}).get("element_type", "")).startswith("{") and details.get(str(c.get("card_id")), {}).get("element_type") in allowed_types], key=lambda x: scores.get(str(x["card_id"]), 0.0), reverse=True)
    basics = [c for c in pokemon_pool if details.get(str(c["card_id"]), {}).get("stage") == "Basic"]
    trainer_pool = {"ultra ball": 4, "switch": 4, "lillie's determination": 4, "buddy-buddy poffin": 4, "boss's orders": 4, "poke pad": 4, "pokegear 3.0": 4, "hilda": 4}
    energy_pool = [c for c in pool_cards if c.get("card_type") == "Energy"]

    graph = get_global_synergy_graph()
    core_engines = graph.extract_core_engines(threshold=1.0)
    engine_cards = set().union(*core_engines) if core_engines else set()

    locked_cards = {}
    locked_count = 0
    if winning_decks:
        num_winners = len(winning_decks)
        for cid, freq in winning_freq.most_common():
            if int(cid) not in engine_cards:
                continue
            avg_copies = round(freq / num_winners)
            if avg_copies > 0:
                card_dict = id_map.get(int(cid))
                if card_dict:
                    limit = 99 if card_dict.get("card_type") == "Energy" and "Basic" in card_dict.get("card_name", "") else 4
                    copies_to_add = min(avg_copies, limit)
                    if locked_count + copies_to_add <= 40:
                        locked_cards[int(cid)] = copies_to_add
                        locked_count += copies_to_add
                    else:
                        locked_cards[int(cid)] = 40 - locked_count
                        locked_count = 40
                        break

    flex_pool = []
    for c in pool_cards:
        cid = int(c["card_id"])
        if cid in locked_cards:
            continue
        has_synergy = False
        if not locked_cards:
            has_synergy = True
        else:
            for l_cid in locked_cards:
                if graph.get_pmi(cid, l_cid) > 0:
                    has_synergy = True
                    break
        if has_synergy:
            flex_pool.append(cid)

    empirical_core = EmpiricalCore(
        locked_cards=locked_cards,
        flex_pool=flex_pool,
        core_engines=core_engines,
        locked_count=locked_count
    )

    seed_deck = []
    p = Path("cb_agents/deck_new.csv")
    if p.exists():
        for r in list(csv.reader(p.open(encoding="utf-8")))[1:]:
            if r and int(r[0]) in id_map:
                seed_deck.extend([id_map[int(r[0])]] * int(r[3]))

    return {"pool_cards": pool_cards, "details": details, "scores": scores,
            "pokemon_pool": pokemon_pool, "basics": basics, "energy_pool": energy_pool,
            "trainer_pool": trainer_pool, "seed_deck": seed_deck, "empirical_core": empirical_core}
