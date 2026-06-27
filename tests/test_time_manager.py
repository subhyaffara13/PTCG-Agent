"""
tests/test_time_manager.py

Unit tests for agents/time_manager.py.
"""

import os
import json
import pytest
from pathlib import Path
from agents.time_manager import TimeManager
from router.bus import TimePacket

def test_time_manager_thresholds(tmp_path):
    tm = TimeManager(log_dir=str(tmp_path))
    
    # 1. Normal state (200 elapsed → 400 remaining > 60)
    p1 = TimePacket(time_elapsed=200.0, time_limit=600.0)
    r1 = tm.receive(p1)
    assert r1["status"] == "normal"
    assert r1["action_override"] is None
    assert r1["urgent"] is False

    # 2. Warning state (550 elapsed → 50 remaining > 2)
    p2 = TimePacket(time_elapsed=550.0, time_limit=600.0)
    r2 = tm.receive(p2)
    assert r2["status"] == "warning"
    assert r2["action_override"] is None
    assert r2["urgent"] is True

    # 3. Timeout state (599 elapsed → 1 remaining ≤ 2)
    p3 = TimePacket(time_elapsed=599.0, time_limit=600.0, legal_actions=["retreat:0"])
    r3 = tm.receive(p3)
    assert r3["status"] == "timeout"
    assert r3["action_override"] == "retreat:0"
    assert r3["urgent"] is True

    # 4. Timeout without legal_actions
    p4 = TimePacket(time_elapsed=610.0, time_limit=600.0)
    r4 = tm.receive(p4)
    assert r4["status"] == "timeout"
    assert r4["action_override"] == "pass"
    
    # 5. Invalid / negative time
    p5 = TimePacket(time_elapsed=-10.0, time_limit=600.0)
    r5 = tm.receive(p5)
    assert r5["status"] == "normal"
    tm.flush_logs()
    assert (tmp_path / "reasoning_log.json").exists()

