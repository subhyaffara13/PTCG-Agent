import os
import re
import json
import csv
from pathlib import Path

def read_clean_source(path):
    content = Path(path).read_text(encoding="utf-8")
    lines = []
    for line in content.splitlines():
        # Match local imports and skip them
        if re.match(r"^\s*(from|import)\s+(cb_agents|agents|router)\b", line):
            continue
        if "__future__" in line:
            continue
        lines.append(line)
    return "\n".join(lines)

def bundle():
    print("Bundling agent into a single file...")
    
    # 1. Read JSON config files
    skills_dir = Path("skills")
    
    delegation_map = {}
    delegation_path = skills_dir / "delegation_map.json"
    if delegation_path.exists():
        delegation_map = json.loads(delegation_path.read_text(encoding="utf-8")).get("delegation", {})
        
    priority_rules = {}
    priority_path = skills_dir / "priority_rules.json"
    if priority_path.exists():
        priority_rules = json.loads(priority_path.read_text(encoding="utf-8"))
        
    strategy_profiles = {}
    strategy_path = skills_dir / "strategy_profiles.json"
    if strategy_path.exists():
        strategy_profiles = json.loads(strategy_path.read_text(encoding="utf-8"))
        
    deck_archetypes = {}
    archetypes_path = skills_dir / "deck_archetypes.json"
    if archetypes_path.exists():
        deck_archetypes = json.loads(archetypes_path.read_text(encoding="utf-8"))
        
    # 2. Read deck EV scores and deck list from staging/deck_new.csv
    deck_ev = {}
    deck_list = []
    deck_path = Path("staging/deck_new.csv")
    if not deck_path.exists():
        deck_path = Path("submission/deck.csv")
    if deck_path.exists():
        with open(deck_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("card_name", "").strip()
                if name:
                    deck_ev[name] = float(row.get("ev_score", 0.0))
                card_id_str = row.get("card_id", "").strip()
                count_str = row.get("count", "").strip()
                if card_id_str and count_str:
                    deck_list.extend([int(card_id_str)] * int(count_str))
                    
    print(f"Loaded {len(deck_ev)} card EV scores")
    if len(deck_list) == 60:
        default_deck_str = repr(deck_list)
    else:
        print(f"Warning: Loaded deck has {len(deck_list)} cards, falling back to default 60-card deck.")
        default_deck_str = "[\n    3, 3, 3, 3, 3, 3, 3, 5, 6, 6,\n    11, 19, 19, 65, 66, 304, 305, 676, 676, 676,\n    676, 677, 678, 722, 723, 741, 742, 743, 878, 879,\n    1079, 1081, 1086, 1086, 1086, 1086, 1102, 1115, 1121, 1122,\n    1141, 1142, 1145, 1152, 1152, 1152, 1152, 1171, 1182, 1182,\n    1182, 1192, 1219, 1225, 1227, 1227, 1227, 1227, 1231, 1255\n]"

    # 3. Read Python sources
    base_agent = read_clean_source("agents/base_agent.py")
    registry = read_clean_source("agents/registry.py")
    bus = read_clean_source("router/bus.py")
    hand_analyst = read_clean_source("agents/hand_analyst.py")
    turn_planner = read_clean_source("agents/turn_planner.py")
    strategy_agent = read_clean_source("agents/strategy_agent.py")
    opponent_model = read_clean_source("agents/opponent_model.py")
    time_manager = read_clean_source("agents/time_manager.py")
    orchestrator = read_clean_source("agents/orchestrator.py")
    main_py = read_clean_source("submission/main_template.py")

    # 4. Patch class methods to read from inline dicts instead of files
    
    # HandAnalyst patch:
    # Rewrite _load_skill:
    old_load_skill = """    def _load_skill(self) -> dict[str, dict[str, Any]]:
        raw   = json.loads(_SKILL_PATH.read_text(encoding="utf-8"))
        index = {}
        for entry in raw.get("cards", []):
            name = entry.get("card_name", "").strip()
            if name:
                index[name] = entry
        return index"""
        
    new_load_skill = """    def _load_skill(self) -> dict[str, dict[str, Any]]:
        index = {}
        for name, ev in DECK_EV_SCORES.items():
            index[name] = {"card_name": name, "ev_score": ev}
        return index"""
    
    hand_analyst = hand_analyst.replace(old_load_skill, new_load_skill)

    # TurnPlanner patch:
    old_load_rules = """    def _load_priority_rules(self) -> dict:
        path = self.skills_dir / "priority_rules.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read priority_rules.json: {e}")
        return {"rules": []}"""
        
    new_load_rules = """    def _load_priority_rules(self) -> dict:
        return PRIORITY_RULES"""
        
    turn_planner = turn_planner.replace(old_load_rules, new_load_rules)

    # StrategyAgent patch:
    old_load_profiles = """    def _load_strategy_profiles(self) -> dict:
        path = self.skills_dir / "strategy_profiles.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read strategy_profiles.json: {e}")
        return {"profiles": {}}"""
        
    new_load_profiles = """    def _load_strategy_profiles(self) -> dict:
        return STRATEGY_PROFILES"""
        
    strategy_agent = strategy_agent.replace(old_load_profiles, new_load_profiles)

    # OpponentModel patch:
    old_load_archetypes = """    def _load_deck_archetypes(self) -> dict:
        path = self.skills_dir / "deck_archetypes.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("archetypes", {})
            except Exception as e:
                logger.error(f"Failed to read deck_archetypes.json: {e}")
        return {}"""
        
    new_load_archetypes = """    def _load_deck_archetypes(self) -> dict:
        return DECK_ARCHETYPES.get("archetypes", {})"""
        
    opponent_model = opponent_model.replace(old_load_archetypes, new_load_archetypes)

    # Orchestrator patch:
    old_load_delegation = """    def _load_delegation_map(self) -> dict:
        path = self.skills_dir / "delegation_map.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("delegation", {})
            except Exception as e:
                logger.error(f"Failed to read delegation_map.json: {e}")
        # Default fallback map matching skills/delegation_map.json
        return {
            "turn_start": "hand_analyst",
            "after_hand_analysis": "turn_planner",
            "on_trigger": "strategy_agent",
            "on_opponent_play": "opponent_model",
            "before_turn_planner": "lethal_calculator",
            "always": "time_manager"
        }"""
        
    new_load_delegation = """    def _load_delegation_map(self) -> dict:
        return DELEGATION_MAP"""
        
    orchestrator = orchestrator.replace(old_load_delegation, new_load_delegation)

    # Find the definitions of get_val, _log_action_exception and agent in main_py
    # We will split them to place 'agent' at the absolute bottom of the file
    get_val_idx = main_py.find("def get_val")
    agent_idx = main_py.find("def agent")
    log_exc_idx = main_py.find("def _log_action_exception")
    
    # Extract each block
    get_val_code = main_py[get_val_idx:agent_idx]
    
    # We want to trace the end of agent function to extract it cleanly
    # Since agent goes until def _log_action_exception, let's extract it
    agent_code = main_py[agent_idx:log_exc_idx]
    log_exc_code = main_py[log_exc_idx:]
    
    # 5. Generate final content with 'agent' function at the very end
    output = f"""from __future__ import annotations
# Single-file self-contained Pokemon TCG Kaggle Submission Agent
# Generated automatically by build_single_file.py

import json
import logging
import time
import sys
import csv
import datetime
from pathlib import Path
from typing import Any, Dict, List, Set, Callable
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ==========================================
# CONSTANTS & EMBEDDED CONFIGURATIONS
# ==========================================

DELEGATION_MAP = {json.dumps(delegation_map, indent=2)}

PRIORITY_RULES = {json.dumps(priority_rules, indent=2)}

STRATEGY_PROFILES = {json.dumps(strategy_profiles, indent=2)}

DECK_ARCHETYPES = {json.dumps(deck_archetypes, indent=2)}

DECK_EV_SCORES = {json.dumps(deck_ev, indent=2)}

DEFAULT_DECK = {default_deck_str}

# ==========================================
# BASE AGENT
# ==========================================
{base_agent}

# ==========================================
# ROUTER / BUS
# ==========================================
{bus}

# ==========================================
# SUB-AGENTS
# ==========================================
{registry}

{hand_analyst}

{turn_planner}

{strategy_agent}

{opponent_model}

{time_manager}

# ==========================================
# ORCHESTRATOR
# ==========================================
{orchestrator}

# ==========================================
# MAIN AGENT INTERFACE
# ==========================================
# GLOBAL SETUP (runs once on load)
try:
    orchestrator = Orchestrator()
    orchestrator.start_game()
except Exception as global_err:
    logger.error(f"Global orchestrator initialization failed: {{global_err}}")
    orchestrator = None

{get_val_code}

{log_exc_code}

{agent_code}
"""

    # Write the compiled file to submission_single.py
    Path("submission/submission_single.py").write_text(output, encoding="utf-8")
    print(f"Generated submission_single.py successfully ({len(output):,} bytes)")

if __name__ == "__main__":
    bundle()
