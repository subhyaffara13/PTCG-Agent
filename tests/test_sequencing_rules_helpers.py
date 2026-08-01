import json

from utils.setup_skills_dir import setup_skills_dir

PRIORITY_RULES_EMPTY = {"rules": []}
STRATEGY_PROFILES_EMPTY = {"profiles": {"setup": {"actions": ["PASS"]}, "hand_dead": {"actions": ["PASS"]}, "aggro_push": {"actions": ["PASS"]}}}

CHARGED_ACTIVE = {
    "id": 722,
    "energies": [3, 3, 3]
}
