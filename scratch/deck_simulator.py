import random
import os
import torch
from scratch.deck_synergy import evaluate_deck_synergy

_numba_multivariate_setup_prob = None

# Initialize PPO ActorCritic model globally if weights exist
PPO_MODEL = None
ALIGNER = None

try:
    if os.path.exists("models/ppo_actor_critic.pt"):
        from factory.ppo_trainer_network import ActorCritic
        from factory.data_alignment import DataAligner
        ALIGNER = DataAligner()
        PPO_MODEL = ActorCritic(input_dim=213, hidden_dim=256, action_dim=3000)
        PPO_MODEL.load_state_dict(torch.load("models/ppo_actor_critic.pt", map_location="cpu"))
        PPO_MODEL.eval()
except Exception as ppo_err:
    pass

def get_ppo_setup_value(cand: list, details: dict, num_trials: int = 5) -> float:
    if PPO_MODEL is None or ALIGNER is None:
        return 0.0
    basics = [c for c in cand if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"]
    if not basics:
        return -1.5  # Heavy penalty for no basic pokemon
        
    total_val = 0.0
    valid_trials = 0
    for _ in range(num_trials):
        deck_copy = list(cand)
        random.shuffle(deck_copy)
        hand = [deck_copy.pop() for _ in range(min(len(deck_copy), 7))]
        
        hand_basics = [c for c in hand if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"]
        mulligans = 0
        while not hand_basics and mulligans < 5:
            mulligans += 1
            deck_copy = list(cand)
            random.shuffle(deck_copy)
            hand = [deck_copy.pop() for _ in range(min(len(deck_copy), 7))]
            hand_basics = [c for c in hand if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"]
            
        if not hand_basics:
            continue
            
        active = hand_basics[0]
        hand.remove(active)
        bench = [c for c in hand if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"][:5]
        for b in bench:
            hand.remove(b)
            
        raw_state = {
            "hand": [c["card_id"] for c in hand],
            "active": active["card_id"],
            "bench": [c["card_id"] for c in bench],
            "prize": [1]*6,
            "opponent_visible": [],
            "turn": 1,
            "is_first_player": 1,
        }
        
        try:
            norm_state = ALIGNER.normalize_state(raw_state)
            stacked_state = norm_state * 3  # Stack size = 3 (STATE_DIM = 213)
            state_tensor = torch.tensor(stacked_state, dtype=torch.float32).unsqueeze(0)
            with torch.no_grad():
                _, val_tensor = PPO_MODEL(state_tensor)
                total_val += val_tensor.item()
                valid_trials += 1
        except Exception:
            pass
            
    return (total_val / valid_trials) if valid_trials > 0 else 0.0

def multivariate_setup_prob(basics: int, energies: int, consistency: int) -> float:
    if _numba_multivariate_setup_prob is not None:
        return _numba_multivariate_setup_prob(basics, energies, consistency)
    if basics <= 0 or energies <= 0 or consistency <= 0:
        return 0.0
    success = 0
    deck = [1]*basics + [2]*energies + [3]*consistency + [0]*(60 - basics - energies - consistency)
    for _ in range(300):
        hand = random.sample(deck, min(60, 7))
        if 1 in hand and 2 in hand and 3 in hand:
            success += 1
    return success / 300.0

def simulate_goldfish_playout(deck: list, details: dict) -> float:
    deck_copy = list(deck); random.shuffle(deck_copy)
    hand = [deck_copy.pop() for _ in range(min(len(deck_copy), 7))]
    basics = [c for c in hand if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"]
    if not basics:
        return 0.0
    active = basics[0]; hand.remove(active)
    bench, attached, setup_turn = [], 0, 99
    for turn in range(1, 5):
        if deck_copy:
            hand.append(deck_copy.pop())
        if len(hand) <= 3 and any("research" in c.get("card_name", "").lower() or "iono" in c.get("card_name", "").lower() for c in hand):
            hand = [deck_copy.pop() for _ in range(min(len(deck_copy), 7)) if deck_copy]
        eg = next((c for c in hand if c.get("card_type") == "Energy"), None)
        if eg:
            attached += 1; hand.remove(eg)
        buddy = next((c for c in hand if "poffin" in c.get("card_name", "").lower()), None)
        if buddy and len(bench) < 5:
            hand.remove(buddy)
            b_pokemon = next((c for c in deck_copy if c.get("card_type") == "Pokemon" and details.get(str(c["card_id"]), {}).get("stage") == "Basic"), None)
            if b_pokemon:
                deck_copy.remove(b_pokemon); bench.append(b_pokemon)
        rc = next((c for c in hand if "candy" in c.get("card_name", "").lower()), None)
        s2 = next((c for c in hand if details.get(str(c["card_id"]), {}).get("stage") == "Stage 2"), None)
        if rc and s2:
            prev = details.get(str(s2["card_id"]), {}).get("previous_stage", "")
            on_board = active if active.get("card_name") == prev else next((x for x in bench if x.get("card_name") == prev), None)
            if on_board:
                hand.remove(rc); hand.remove(s2)
                if on_board == active:
                    active = s2
                else:
                    bench.remove(on_board); bench.append(s2)
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
    
    # Enforce copy limits
    from collections import Counter
    from scratch.deck_genetics import get_card_copy_limit
    counts = Counter(str(c["card_id"]) for c in cand)
    violations = 0
    for cid, cnt in counts.items():
        card = next((c for c in cand if str(c["card_id"]) == cid), None)
        if card:
            limit = get_card_copy_limit(card)
            if cnt > limit:
                violations += (cnt - limit)
    
    base_score = fit + multivariate_setup_prob(n_basics, n_energies, n_trainers) * 150.0 + evaluate_deck_synergy(cand, details) + simulate_goldfish_playout(cand, details)
    ppo_score = get_ppo_setup_value(cand, details)
    
    # Scale PPO score (which ranges from -1.5 to 1.0) to have a meaningful impact on fitness
    final_score = base_score + ppo_score * 120.0
    if violations > 0:
        final_score -= violations * 100000.0
    return final_score

