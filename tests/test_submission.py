"""
tests/test_submission.py

Unit tests for submission/main.py.
"""

import os
import json
import pytest
from pathlib import Path
from submission.main import agent

class MockObservation:
    def __init__(self):
        self.hand = ["1"]
        self.deck_count = 45
        self.prizes = 6
        self.active = "Pikachu"
        self.bench = []
        self.opponent_active = "Charmander"
        self.opponent_bench_count = 0
        self.opponent_prizes = 6
        self.opponent_discard = []
        self.opponent_revealed = []
        self.opponent_last_play = False
        self.turn = 1
        self.legal_actions = ["pass", "attack:Thunderbolt"]

def test_submission_agent_returns_legal_action():
    obs = MockObservation()
    
    # Run agent act iteration
    action = agent(obs)
    
    # Assert action is from the legal list
    assert action in obs.legal_actions
