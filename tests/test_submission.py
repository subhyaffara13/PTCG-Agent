"""
tests/test_submission.py

Unit tests for submission/main.py.
"""

import os
import json
import pytest
import sys
from pathlib import Path
submission_dir = str(Path(__file__).parent.parent / "submission")
if submission_dir not in sys.path:
    sys.path.insert(0, submission_dir)
from main import agent

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
    assert action[0] in obs.legal_actions

def test_realistic_submission_agent_orchestration():
    # When select is a real turn choice, it should run orchestrator and return selected option indices
    obs = RealisticMockObservation()
    action = agent(obs)
    
    # Assert return value is a list of indices representing the selected option(s)
    assert isinstance(action, list)
    for idx in action:
        assert 0 <= idx < len(obs.select.option)


def test_submission_py_compatibility():
    # Verify that all Python files inside the submission/ directory are Python 3.11 compatible (no PEP 701 nested quotes in f-strings)
    sub_dir = Path(__file__).parent.parent / "submission"
    if sub_dir.exists():
        import ast
        for py_file in sub_dir.rglob("*.py"):
            content = py_file.read_text(encoding="utf-8")
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.JoinedStr):
                    for val in node.values:
                        if isinstance(val, ast.FormattedValue):
                            expr_str = ast.unparse(val.value)
                            assert "'" not in expr_str and '"' not in expr_str, f"PEP 701 f-string compatibility error in {py_file.name}: f-string expression contains quotes: {{{expr_str}}}"
