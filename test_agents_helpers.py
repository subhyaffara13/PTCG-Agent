import sys, json
sys.path.insert(0, ".")

from router.bus import Router
from agents.hand_analyst import HandAnalyst
from agents.turn_planner import TurnPlanner
from agents.time_manager import TimeManager
from agents.strategy_agent import StrategyAgent
from agents.opponent_model import OpponentModel, OpponentModelPacket

SEP = "=" * 60

router = Router()
analyst = HandAnalyst()
planner = TurnPlanner()
tm = TimeManager()
strategy = StrategyAgent()
opponent = OpponentModel()

strategy_tests = [
    ("ko_window",  {},                            "exact key match"),
    ("prize_race", {},                            "exact key match"),
    ("",           {"prizes": 1},                 "board_summary signal (prizes=1 -> endgame_close)"),
    ("bench_low",  {"bench_count": 1},            "exact key + board signal"),
    ("attacking",  {},                            "keyword scan / fallback"),
]

opp_pkt = OpponentModelPacket(
    turn=3,
    newly_played_cards=["Quick Ball", "Nest Ball", "Boss's Orders"],
    revealed_active_pokemon="Pikachu ex",
    revealed_bench_count=3,
    revealed_hand_size=4,
    revealed_prizes_remaining=4,
    revealed_discard=["Lightning Energy"],
    game_phase="early",
)

game_state = {
    "time_elapsed": 210.0,
    "time_limit":   600.0,
    "hand":           ["Charizard ex", "Rare Candy", "Fire Energy", "Boss's Orders"],
    "deck_remaining": 22,
    "trigger":       "ko_window",
    "board_summary": {"prizes": 3, "opponent_prizes": 4, "hand_score": 6.5},
    "revealed_cards":            ["Quick Ball", "Arcanine ex"],
    "turn_number":               5,
    "archetype_confidence":      0.55,
    "opponent_active_pokemon":   "Arcanine ex",
    "opponent_bench_count":      2,
    "opponent_hand_size":        3,
    "opponent_prizes_remaining": 4,
    "opponent_discard":          ["Fire Energy", "Fire Energy"],
    "game_phase":                "mid",
}
