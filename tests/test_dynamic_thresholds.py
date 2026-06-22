"""
tests/test_dynamic_thresholds.py

Dynamic threshold and behavior alteration tests.
"""

import os
import json
import pytest
from pathlib import Path
from agents.hand_analyst import HandAnalyst
from agents.strategy_agent import StrategyAgent
from router.bus import HandAnalystPacket, StrategyPacket
from agents.context import SharedContext

def test_dynamic_threshold_loading(tmp_path):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    
    # 1. Write initial card scoring and strategy thresholds
    cards_file = skills_dir / "card_scoring.json"
    cards_file.write_text(json.dumps({
        "cards": [
            {"card_id": "1", "card_name": "Pikachu", "card_type": "Pokemon", "ev_score": 0.8, "combo_tags": ["Basic"]},
            {"card_id": "2", "card_name": "Supporter", "card_type": "Trainer", "ev_score": 0.6, "combo_tags": ["Supporter"]},
            {"card_id": "3", "card_name": "Energy", "card_type": "Energy", "ev_score": 0.5, "combo_tags": []}
        ]
    }), encoding="utf-8")

    thresholds_file = skills_dir / "strategy_thresholds.json"
    initial_thresholds = {
        "hand_analyst": {
            "combo_multipliers": {
                "search_and_bench": 0.1,
                "discard_and_draw": 0.15,
                "discard_search_energy": 0.25,
                "rare_candy_stage2": 0.35
            },
            "penalties": {
                "supporter_oversaturation_threshold": 2,
                "supporter_oversaturation_factor": 0.1,
                "brick_factor": 0.15
            },
            "bonuses": {
                "evolution_match_factor": 0.20,
                "early_basic": 0.15,
                "early_supporter": 0.1,
                "mid_energy": 0.15,
                "mid_evolution": 0.1,
                "late_attacker": 0.15,
                "late_high_ev_threshold": 0.6,
                "late_high_ev_bonus": 0.1
            },
            "priority_profiles": {
                "closing": { "opponent_prizes_max": 2 },
                "aggro_push": { "hand_score_min": 0.35 },
                "setup": { "hand_score_max": 0.3 },
                "disruption": { "control_count_min": 2, "opponent_prizes_max": 3 },
                "stall": { "deck_remaining_max": 15 }
            }
        },
        "strategy_agent": {
            "trigger_rules": {
                "prize_gap_threshold": 2,
                "opponent_confidence_threshold": 0.75,
                "turn_milestones": [3, 6, 9, 12, 15],
                "bench_count_min": 3,
                "bench_opponent_prizes_min": 3,
                "prized_attacker_threshold": 0.75
            },
            "strategy_selection": {
                "prized_attacker_extreme_threshold": 0.99,
                "opponent_prizes_low": 2,
                "desperation_my_prizes_min": 5,
                "desperation_opponent_prizes_max": 3,
                "my_active_hp_critical": 30
            }
        }
    }
    thresholds_file.write_text(json.dumps(initial_thresholds), encoding="utf-8")

    # Clear SharedContext caches to ensure we start clean
    SharedContext._caches.clear()

    # Instantiate HandAnalyst and StrategyAgent
    analyst = HandAnalyst(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    agent = StrategyAgent(log_dir=str(tmp_path), skills_dir=str(skills_dir))

    # Evaluate initial behavior
    packet_ha = HandAnalystPacket(hand=["1", "2", "3"], deck_remaining=30)
    res_ha_1 = analyst.receive(packet_ha)
    
    packet_sa = StrategyPacket(trigger="turn_start", board_summary={
        "my_prizes_remaining": 5,
        "opponent_prizes_remaining": 3, # gap = 2
        "opponent_archetype_confidence": 0.1,
        "priority_profile": "aggro_push",
        "turn_number": 2
    })
    res_sa_1 = agent.receive(packet_sa)
    
    # Under initial configuration:
    # - prize_gap_threshold is 2, so gap of 2 triggers evaluation
    assert res_sa_1["triggered"] is True

    # Now write MODIFIED thresholds to strategy_thresholds.json on disk
    modified_thresholds = {
        "hand_analyst": {
            "combo_multipliers": {
                "search_and_bench": 5.0, # changed from 0.1 to 5.0
                "discard_and_draw": 0.15,
                "discard_search_energy": 0.25,
                "rare_candy_stage2": 0.35
            },
            "penalties": {
                "supporter_oversaturation_threshold": 2,
                "supporter_oversaturation_factor": 0.1,
                "brick_factor": 0.15
            },
            "bonuses": {
                "evolution_match_factor": 0.20,
                "early_basic": 0.15,
                "early_supporter": 0.1,
                "mid_energy": 0.15,
                "mid_evolution": 0.1,
                "late_attacker": 0.15,
                "late_high_ev_threshold": 0.6,
                "late_high_ev_bonus": 0.1
            },
            "priority_profiles": {
                "closing": { "opponent_prizes_max": 2 },
                "aggro_push": { "hand_score_min": 0.35 },
                "setup": { "hand_score_max": 0.3 },
                "disruption": { "control_count_min": 2, "opponent_prizes_max": 3 },
                "stall": { "deck_remaining_max": 15 }
            }
        },
        "strategy_agent": {
            "trigger_rules": {
                "prize_gap_threshold": 5, # changed from 2 to 5
                "opponent_confidence_threshold": 0.75,
                "turn_milestones": [3, 6, 9, 12, 15],
                "bench_count_min": 3,
                "bench_opponent_prizes_min": 3,
                "prized_attacker_threshold": 0.75
            },
            "strategy_selection": {
                "prized_attacker_extreme_threshold": 0.99,
                "opponent_prizes_low": 2,
                "desperation_my_prizes_min": 5,
                "desperation_opponent_prizes_max": 3,
                "my_active_hp_critical": 30
            }
        }
    }
    thresholds_file.write_text(json.dumps(modified_thresholds), encoding="utf-8")

    # Evaluate behavior of EXISTING instances
    res_ha_2 = analyst.receive(packet_ha)
    res_sa_2 = agent.receive(packet_sa)

    # Let's check if the existing instances picked up the change
    # If they did NOT pick up the change, res_sa_2["triggered"] will still be True (since prize_gap_threshold is still cached as 2, and gap is 2)
    # If they DID pick up the change, res_sa_2["triggered"] would be False (since prize_gap_threshold is now 5, and gap is 2 < 5)
    print("Existing StrategyAgent triggered after modification:", res_sa_2["triggered"])
    print("Existing HandAnalyst score after modification:", res_ha_2["hand_score"])
    
    # Evaluate behavior of NEW instances in the same process
    new_analyst = HandAnalyst(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    new_agent = StrategyAgent(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    
    res_ha_3 = new_analyst.receive(packet_ha)
    res_sa_3 = new_agent.receive(packet_sa)
    
    print("New StrategyAgent triggered after modification:", res_sa_3["triggered"])
    print("New HandAnalyst score after modification:", res_ha_3["hand_score"])

    # Clear SharedContext cache explicitly to verify if that's the only reason they don't reload
    SharedContext._caches.clear()
    
    fresh_analyst = HandAnalyst(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    fresh_agent = StrategyAgent(log_dir=str(tmp_path), skills_dir=str(skills_dir))
    
    res_ha_4 = fresh_analyst.receive(packet_ha)
    res_sa_4 = fresh_agent.receive(packet_sa)
    
    print("Fresh StrategyAgent (cache cleared) triggered:", res_sa_4["triggered"])
    print("Fresh HandAnalyst (cache cleared) score:", res_ha_4["hand_score"])
    
    # Assertions for our findings
    # 1. Existing agent does NOT pick up changes (caching prevents it)
    assert res_sa_2["triggered"] is True  # still uses cached prize_gap_threshold = 2
    
    # 2. New agent created in same process does NOT pick up changes (SharedContext caches LazyDict)
    assert res_sa_3["triggered"] is True  # still uses cached prize_gap_threshold = 2
    
    # 3. Only when SharedContext is cleared does it load new configuration
    assert res_sa_4["triggered"] is False  # prize_gap_threshold is now 5, gap 2 < 5, so does not trigger!
