"""
scratch/deck_optimizer_helpers.py
Hypergeometric math, synergy checks, goldfish playout simulator, and deck builder.
"""
import math
import random

try:
    import numba
    import numpy as np
    @numba.jit(nopython=True, cache=True)
    def _numba_multivariate_setup_prob(basics: int, energies: int, consistency: int) -> float:
        if basics <= 0 or energies <= 0 or consistency <= 0: return 0.0
        success = 0
        deck = np.zeros(60, dtype=np.int32)
        deck[:basics] = 1
        deck[basics:basics+energies] = 2
        deck[basics+energies:basics+energies+consistency] = 3
        for _ in range(300):
            indices = np.random.choice(60, size=7, replace=False)
            has_basic = has_energy = has_consistency = False
            for idx in indices:
                val = deck[idx]
                if val == 1: has_basic = True
                elif val == 2: has_energy = True
                elif val == 3: has_consistency = True
            if has_basic and has_energy and has_consistency: success += 1
        return success / 300.0
except ImportError:
    _numba_multivariate_setup_prob = None

def multivariate_setup_prob(basics: int, energies: int, consistency: int) -> float:
    if _numba_multivariate_setup_prob is not None:
        return _numba_multivariate_setup_prob(basics, energies, consistency)
    if basics <= 0 or energies <= 0 or consistency <= 0: return 0.0
    success = 0
    deck = [1]*basics + [2]*energies + [3]*consistency + [0]*(60 - basics - energies - consistency)
    for _ in range(300):
        hand = random.sample(deck, min(60, 7))
        if 1 in hand and 2 in hand and 3 in hand: success += 1
    return success / 300.0

def evaluate_deck_synergy(deck: list, details: dict) -> float:
    penalty = 0.0
    p_types = {details.get(str(c["card_id"]), {}).get("element_type", "") for c in deck if c.get("card_type") == "Pokemon"}
    p_types.discard("")
    e_names = {c.get("card_name", "").lower() for c in deck if c.get("card_type") == "Energy"}
    t_map = {"{R}": "fire", "{W}": "water", "{G}": "grass", "{L}": "lightning", "{F}": "fighting", "{P}": "psychic", "{D}": "darkness", "{M}": "metal"}
    for pt in p_types:
        exp = t_map.get(pt, "none")
        if exp != "none" and not any(exp in en for en in e_names): penalty += 50.0
    s2 = sum(1 for c in deck if details.get(str(c["card_id"]), {}).get("stage") == "Stage 2")
    rc = sum(1 for c in deck if c.get("card_name", "").lower() == "rare candy")
    if s2 > rc: penalty += 15.0 * (s2 - rc)
    return penalty

def simulate_goldfish_playout(deck: list, details: dict) -> float:
    deck_copy = list(deck); random.shuffle(deck_copy)
    hand = [deck_copy.pop() for _ in range(min(len(deck_copy), 7))]
    basics = [c for c in hand if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"]
    if not basics: return 0.0
    active = basics[0]; hand.remove(active)
    bench, attached, setup_turn = [], 0, 99
    
    for turn in range(1, 5):
        if deck_copy: hand.append(deck_copy.pop())
        if len(hand) <= 3 and any("research" in c.get("card_name", "").lower() or "iono" in c.get("card_name", "").lower() for c in hand):
            hand = [deck_copy.pop() for _ in range(min(len(deck_copy), 7)) if deck_copy]
        eg = next((c for c in hand if c.get("card_type") == "Energy"), None)
        if eg: attached += 1; hand.remove(eg)
        buddy = next((c for c in hand if "poffin" in c.get("card_name", "").lower()), None)
        if buddy and len(bench) < 5:
            hand.remove(buddy)
            b_pokemon = next((c for c in deck_copy if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"), None)
            if b_pokemon: deck_copy.remove(b_pokemon); bench.append(b_pokemon)
        rc = next((c for c in hand if "candy" in c.get("card_name", "").lower()), None)
        s2 = next((c for c in hand if details.get(str(c["card_id"]), {}).get("stage") == "Stage 2"), None)
        if rc and s2:
            prev = details.get(str(s2["card_id"]), {}).get("previous_stage", "")
            on_board = active if active.get("card_name") == prev else next((x for x in bench if x.get("card_name") == prev), None)
            if on_board:
                hand.remove(rc); hand.remove(s2)
                if on_board == active: active = s2
                else: bench.remove(on_board); bench.append(s2)
        s1 = next((c for c in hand if details.get(str(c["card_id"]), {}).get("stage") == "Stage 1"), None)
        if s1:
            prev = details.get(str(s1["card_id"]), {}).get("previous_stage", "")
            if active.get("card_name") == prev:
                active = s1; hand.remove(s1)
            elif any(x.get("card_name") == prev for x in bench):
                tgt = next(x for x in bench if x.get("card_name") == prev)
                bench.remove(tgt); bench.append(s1); hand.remove(s1)
        if attached >= 3 or (attached >= 2 and active.get("card_name", "").endswith("ex")):
            setup_turn = min(setup_turn, turn)
    return max(0.0, 100.0 - setup_turn * 20.0)

def evaluate_single_candidate(args) -> float:
    cand, scores, details = args
    n_basics = sum(1 for c in cand if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic")
    n_energies = sum(1 for c in cand if c.get("card_type") == "Energy")
    n_trainers = sum(1 for c in cand if c.get("card_type") == "Trainer")
    fit = sum(scores.get(str(c["card_id"]), 0.0) for c in cand)
    return fit + multivariate_setup_prob(n_basics, n_energies, n_trainers) * 150.0 - evaluate_deck_synergy(cand, details) + simulate_goldfish_playout(cand, details)

def make_deck(lines, trainers, energies, basics, pool, details) -> list:
    deck, copies = [], {}
    def add(c, count):
        cid = str(c["card_id"])
        limit = 99 if c.get("card_type") == "Energy" and "Basic" in c.get("card_name", "") else 4
        for _ in range(count):
            if len(deck) < 60 and copies.get(cid, 0) < limit:
                deck.append(c); copies[cid] = copies.get(cid, 0) + 1
    for p in lines:
        add(p, 3)
        prev = details.get(str(p["card_id"]), {}).get("previous_stage")
        if prev:
            p_basic = next((x for x in pool if x.get("card_name", "").lower() == prev.lower()), None)
            if p_basic: add(p_basic, 4)
    for t, tc in trainers.items():
        match_t = next((x for x in pool if x.get("card_name", "").lower() == t.lower()), None)
        if match_t: add(match_t, tc)
    for e in energies: add(e, 4)
    while len(deck) < 60: deck.append(random.choice(basics or pool))
    return deck[:60]
