"""
tests/test_lethal_calculator.py
"""

import pytest
from agents.lethal_calculator import LethalCalculator
from router.bus import LethalPacket
import os

def test_lethal_calculator_finds_lethal(tmp_path):
    calculator = LethalCalculator(log_dir=str(tmp_path))
    
    packet = LethalPacket(
        my_active_damage=120,
        opponent_active_hp=100,
        legal_attacks=["Thunderbolt"]
    )
    
    result = calculator.receive(packet)
    assert result["action_override"] == "attack:Thunderbolt"
    assert "LethalCalculator found lethal" in result["reasoning_chain"]

def test_lethal_calculator_no_lethal(tmp_path):
    calculator = LethalCalculator(log_dir=str(tmp_path))
    
    packet = LethalPacket(
        my_active_damage=50,
        opponent_active_hp=100,
        legal_attacks=["Quick Attack"]
    )
    
    result = calculator.receive(packet)
    assert result["action_override"] is None

def test_lethal_calculator_no_attack_available(tmp_path):
    calculator = LethalCalculator(log_dir=str(tmp_path))
    
    packet = LethalPacket(
        my_active_damage=120,
        opponent_active_hp=100,
        legal_attacks=[]
    )
    
    result = calculator.receive(packet)
    assert result["action_override"] is None
