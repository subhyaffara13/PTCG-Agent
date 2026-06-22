import pytest
from agents.opponent_model import OpponentModel
from agents.hand_analyst import HandAnalyst
from router.bus import OpponentModelPacket, HandAnalystPacket

def test_opponent_model_archetype_predictor():
    om = OpponentModel(log_dir="logs", skills_dir="skills")
    
    # Mock signature cards for combo (e.g. charizard-ex-obs-125)
    packet = OpponentModelPacket(
        turn=1,
        newly_played_cards=["charizard-ex-obs-125", "pidgeot-ex-obs-164", "rare-candy-sv1-191"],
        revealed_active_pokemon="charmander-obs-023",
        revealed_bench_count=1,
        revealed_hand_size=5,
        revealed_prizes_remaining=6,
        revealed_discard=[],
        game_phase="early"
    )
    
    result = om.receive(packet)
    assert result["inferred_deck_type"] == "combo"
    assert result["archetype_confidence"] > 0.0

def test_hand_analyst_prize_mapper():
    ha = HandAnalyst(log_dir="logs", skills_dir="skills")
    
    # Setup mock deck list
    ha.deck_base_list = {
        721: 4,  # Kyogre
        3: 56    # Energy/Trainers
    }
    
    # Hand + Board + Discard has all 4 Kyogres accounted for
    packet = HandAnalystPacket(
        hand=[721, 721],
        deck_remaining=50,
        discard=[721],
        board=[721]
    )
    
    # Deduce prized probabilities
    ha.receive(packet)
    
    # Read generated logs
    import json
    from pathlib import Path
    log_file = Path("logs/prize_mapper_reasoning.json")
    assert log_file.exists()
    logs = json.loads(log_file.read_text(encoding="utf-8"))
    
    latest_log = logs[-1]
    prized_probs = latest_log["prized_probabilities"]
    
    # Kyogre (721) has all 4 copies revealed, so prized probability must be 0.0
    assert prized_probs["721"] == 0.0
