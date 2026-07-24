import pytest
from cb_agents.card_registry import CardRegistry
from cb_agents.heuristic_pipeline_eval import score_action, score_state
from cb_agents.turn_planner_sort import sort_actions_heuristically
from cb_agents.value_network import NeuralValueNetwork
from cb_agents.sequencing_engine import SequencingEngine
from cb_agents.turn_planner_resolve import resolve_action

def test_card_registry_behavioral_parsing():
    registry = CardRegistry()
    # Check that attributes exist on CardRegistry
    assert hasattr(registry, "target_setup_duration")
    assert hasattr(registry, "target_bench_density")
    assert hasattr(registry, "target_deck_stats")
    assert hasattr(registry, "behavior_donts_rules")

def test_profile_orders_are_distinct():
    game_state = {"my_deck_count": 60, "my_bench": [1]}
    candidates = [
        "attack:Attack1",
        "bench:1",
        "attach_energy:4:1",
        "play_trainer:Lillie's Determination",
        "retreat:1",
        "pass"
    ]
    
    order_setup = sort_actions_heuristically(candidates, "setup", game_state)
    order_aggro = sort_actions_heuristically(candidates, "aggro_push", game_state)
    order_stall = sort_actions_heuristically(candidates, "stall", game_state)
    order_closing = sort_actions_heuristically(candidates, "closing", game_state)
    
    # Assert that distinct profiles produce distinct action rankings
    assert order_closing[0] == "attack:Attack1"
    assert order_stall[0] == "retreat:1" or order_stall[-1] == "attack:Attack1"
    assert order_setup != order_closing

def test_value_network_clipping_allows_negative_heuristics():
    nn = NeuralValueNetwork()
    # Mock game state with dangerous low deck where Lillie's Determination gets severe penalty
    game_state = {"my_deck_count": 2, "my_bench": [1], "my_hand": [1227]}
    val = nn.evaluate(game_state, action="play_trainer:Lillie's Determination")
    
    # The value should be below -1.0 due to -10.0 penalty, not clamped to -1.0
    assert val < -1.0

def test_sequencing_engine_candidate_filtering():
    candidates = [
        "play_trainer:Ultra Ball",      # search phase
        "play_trainer:Professor's Research", # draw phase
        "bench:1",                      # board phase
        "attack:Punch",                 # attack phase
        "pass"                          # attack phase
    ]
    
    seq_engine = SequencingEngine()
    groups = seq_engine.group_actions(candidates)
    assert "search" in groups
    assert "play_trainer:Ultra Ball" in groups["search"]
