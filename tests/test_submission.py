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

class MockSelectOption:
    def __init__(self, opt_type, name=""):
        self.type = opt_type
        self.name = name

class MockSelect:
    def __init__(self):
        self.option = [MockSelectOption(14, "pass"), MockSelectOption(13, "Thunderbolt")]
        self.maxCount = 1
        self.type = 0
        self.context = 0

class MockCard:
    def __init__(self, card_id):
        self.id = card_id

class MockPlayerState:
    def __init__(self, is_me=True):
        if is_me:
            self.hand = [MockCard(721)]  # Active attacker basic
            self.deckCount = 45
            self.prize = [{}, {}, {}, {}, {}, {}]
            self.active = [{"hp": 100, "name": "Pikachu", "id": 721}]
            self.bench = []
        else:
            self.hand = []
            self.deckCount = 45
            self.prize = [{}, {}, {}, {}, {}, {}]
            self.active = [{"hp": 100, "name": "Charmander", "id": 722}]
            self.bench = []

class MockCurrentState:
    def __init__(self):
        self.yourIndex = 0
        self.players = [MockPlayerState(is_me=True), MockPlayerState(is_me=False)]
        self.turn = 1

class RealisticMockObservation:
    def __init__(self):
        self.select = MockSelect()
        self.current = MockCurrentState()
        self.legal_actions = ["pass", "attack:Thunderbolt"]

def test_submission_agent_legacy_mock_fallback():
    # When select is None, it should hit the legacy fallback and return the first legal action
    obs = MockObservation()
    action = agent(obs)
    assert action in obs.legal_actions

def test_realistic_submission_agent_orchestration():
    # When select is a real turn choice, it should run orchestrator and return selected option indices
    obs = RealisticMockObservation()
    action = agent(obs)
    
    # Assert return value is a list of indices representing the selected option(s)
    assert isinstance(action, list)
    for idx in action:
        assert 0 <= idx < len(obs.select.option)
