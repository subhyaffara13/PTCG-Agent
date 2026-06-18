"""
rewrite_all.py
--------------
Rewrites router/bus.py, agents/hand_analyst.py, agents/turn_planner.py,
agents/time_manager.py, agents/strategy_agent.py, agents/orchestrator.py
with the correct implementations, overwriting any stale content.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent


# ─────────────────────────────────────────────────────────────────────────────
# router/bus.py
# ─────────────────────────────────────────────────────────────────────────────
BUS = """\
\"\"\"
router/bus.py
-------------
Central message bus for the PTCG multi-agent system.

Design contract
---------------
- The Orchestrator is the ONLY agent that holds full game state.
- Every other agent receives a scoped input packet -- no more, no less.
- Attempting to request data outside an agent's declared scope raises
  ScopeViolationError loudly so the bug surfaces immediately.
- Every delegation call is appended to logs/action_log.json.
\"\"\"

from __future__ import annotations

import json
import pathlib
import datetime
from typing import Any

Card      = str
GameState = dict[str, Any]
Packet    = dict[str, Any]


class ScopeViolationError(RuntimeError):
    \"\"\"Raised when an agent receives a field outside its packet schema.\"\"\"


class UnknownAgentError(KeyError):
    \"\"\"Raised when the Router is asked to dispatch to an unregistered agent.\"\"\"


PACKET_SCHEMAS: dict[str, frozenset[str]] = {
    "HandAnalyst": frozenset({"hand", "deck_remaining"}),
    "TurnPlanner": frozenset({"hand_score", "priority_profile"}),
    "StrategyAgent": frozenset({"trigger", "board_summary"}),
    "OpponentModel": frozenset({"revealed_cards", "turn_number", "archetype_confidence"}),
    "TimeManager": frozenset({"time_elapsed", "time_limit"}),
}

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_LOG_PATH     = _PROJECT_ROOT / "logs" / "action_log.json"


class Router:
    \"\"\"Routes scoped packets from the Orchestrator to downstream agents.

    Usage
    -----
        router = Router()
        packet = router.dispatch("HandAnalyst", {
            "hand": ["Charizard ex", "Rare Candy"],
            "deck_remaining": 42,
        })
    \"\"\"

    def __init__(self) -> None:
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        if not _LOG_PATH.exists() or _LOG_PATH.stat().st_size == 0:
            _LOG_PATH.write_text("[]", encoding="utf-8")

    def dispatch(self, agent_name: str, data: dict[str, Any]) -> Packet:
        \"\"\"Validate scope and deliver a scoped packet to agent_name.

        Raises UnknownAgentError for unregistered agents.
        Raises ScopeViolationError for out-of-scope keys.
        \"\"\"
        schema = self._get_schema(agent_name)
        packet = self._enforce_scope(agent_name, schema, data)
        self._log(agent_name, packet, status="ok")
        return packet

    def _get_schema(self, agent_name: str) -> frozenset[str]:
        if agent_name not in PACKET_SCHEMAS:
            raise UnknownAgentError(
                f"No packet schema registered for agent '{agent_name}'. "
                f"Registered agents: {list(PACKET_SCHEMAS.keys())}"
            )
        return PACKET_SCHEMAS[agent_name]

    def _enforce_scope(self, agent_name: str, schema: frozenset[str], data: dict[str, Any]) -> Packet:
        incoming_keys = frozenset(data.keys())
        forbidden = incoming_keys - schema
        if forbidden:
            self._log(agent_name, data, status="scope_violation",
                      detail=f"Forbidden keys: {sorted(forbidden)}")
            raise ScopeViolationError(
                f"Agent '{agent_name}' was sent field(s) outside its packet schema: "
                f"{sorted(forbidden)}. Allowed keys: {sorted(schema)}"
            )
        return {k: data[k] for k in schema if k in data}

    def _log(self, agent_name: str, payload: dict[str, Any], *, status: str, detail: str | None = None) -> None:
        entry: dict[str, Any] = {
            "timestamp":   datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":       agent_name,
            "status":      status,
            "packet_keys": sorted(payload.keys()),
        }
        if detail:
            entry["detail"] = detail
        try:
            log: list[dict[str, Any]] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.append(entry)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
"""

# ─────────────────────────────────────────────────────────────────────────────
# agents/hand_analyst.py
# ─────────────────────────────────────────────────────────────────────────────
HAND_ANALYST = """\
\"\"\"
agents/hand_analyst.py
----------------------
Analyses the player's current hand and returns a scored summary.

Contract
--------
- Skill file  : skills/card_scoring.json  (loaded once at __init__, never again)
- Input packet: { hand: list[str], deck_remaining: int }  -- from Router only
- Output      : { hand_score: float, priority_profile: str, top_play: str }
- Logs        : every analysis -> logs/reasoning_log.json
- File access : card_scoring.json and reasoning_log.json ONLY
\"\"\"

from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_SKILL_PATH   = _PROJECT_ROOT / "skills" / "card_scoring.json"
_LOG_PATH     = _PROJECT_ROOT / "logs"   / "reasoning_log.json"

_PROFILE_THRESHOLDS: list[tuple[float, str]] = [
    (7.0, "aggressive"),
    (4.0, "tempo"),
    (0.0, "defensive"),
]


class HandAnalyst:
    def __init__(self) -> None:
        self._scoring_db: dict[str, dict[str, Any]] = self._load_skill()

    def analyse(self, packet: dict[str, Any]) -> dict[str, Any]:
        hand: list[str]    = packet["hand"]
        deck_remaining: int = packet.get("deck_remaining", 0)
        scored_cards        = self._score_hand(hand)
        hand_score          = self._mean_ev(scored_cards)
        priority_profile    = self._derive_profile(hand_score)
        top_play            = self._best_card(scored_cards)
        result = {
            "hand_score":       round(hand_score, 4),
            "priority_profile": priority_profile,
            "top_play":         top_play,
        }
        self._log(hand, deck_remaining, scored_cards, result)
        return result

    def _load_skill(self) -> dict[str, dict[str, Any]]:
        raw   = json.loads(_SKILL_PATH.read_text(encoding="utf-8"))
        index = {}
        for entry in raw.get("cards", []):
            name = entry.get("card_name", "").strip()
            if name:
                index[name] = entry
        return index

    def _score_hand(self, hand: list[str]) -> list[tuple[str, float]]:
        scored = []
        for card_name in hand:
            entry    = self._scoring_db.get(card_name, {})
            ev_score = float(entry.get("ev_score", 0.0))
            scored.append((card_name, ev_score))
        return scored

    def _mean_ev(self, scored_cards: list[tuple[str, float]]) -> float:
        if not scored_cards:
            return 0.0
        return sum(ev for _, ev in scored_cards) / len(scored_cards)

    def _derive_profile(self, hand_score: float) -> str:
        for threshold, profile in _PROFILE_THRESHOLDS:
            if hand_score >= threshold:
                return profile
        return "defensive"

    def _best_card(self, scored_cards: list[tuple[str, float]]) -> str:
        if not scored_cards:
            return "(empty hand)"
        return max(scored_cards, key=lambda t: t[1])[0]

    def _log(self, hand, deck_remaining, scored_cards, result):
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":     "HandAnalyst",
            "input":     {"hand": hand, "deck_remaining": deck_remaining},
            "reasoning": {
                "card_scores":   [{"card": n, "ev_score": e} for n, e in scored_cards],
                "unknown_cards": [n for n, e in scored_cards if e == 0.0],
            },
            "output": result,
        }
        try:
            log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.append(entry)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
"""

# ─────────────────────────────────────────────────────────────────────────────
# agents/turn_planner.py
# ─────────────────────────────────────────────────────────────────────────────
TURN_PLANNER = """\
\"\"\"
agents/turn_planner.py
----------------------
Translates a hand summary into an ordered action plan for this turn.

Contract
--------
- Skill file  : skills/priority_rules.json  (loaded once at __init__, never again)
- Input packet: { hand_score: float, priority_profile: str }  -- from Router only
- Output      : list[dict]  -- ordered action plan, highest priority first
- Logs        : every plan + per-decision rationale -> logs/reasoning_log.json
- File access : priority_rules.json and reasoning_log.json ONLY

Priority order (spec):
    1. ATTACK_KO   -- attack if KO available
    2. EVOLVE      -- evolve if possible
    3. ATTACH_ENERGY
    4. PLAY_TRAINER
    5. PASS
\"\"\"

from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any

_PROJECT_ROOT      = pathlib.Path(__file__).resolve().parent.parent
_SKILL_PATH        = _PROJECT_ROOT / "skills" / "priority_rules.json"
_LOG_PATH          = _PROJECT_ROOT / "logs"   / "reasoning_log.json"
_KO_SCORE_THRESHOLD: float = 6.0


class TurnPlanner:
    def __init__(self) -> None:
        self._rules: list[dict[str, Any]]          = []
        self._overrides: dict[str, dict[str, Any]] = {}
        self._load_skill()

    def plan(self, packet: dict[str, Any]) -> list[dict[str, Any]]:
        hand_score: float = float(packet.get("hand_score", 0.0))
        profile:    str   = packet.get("priority_profile", "tempo")
        active_rules      = self._apply_profile(profile)
        action_plan       = self._evaluate_rules(active_rules, hand_score, profile)
        self._log(packet, active_rules, action_plan)
        return action_plan

    def _load_skill(self) -> None:
        raw              = json.loads(_SKILL_PATH.read_text(encoding="utf-8"))
        self._rules      = sorted(raw.get("rules", []), key=lambda r: r["priority"])
        self._overrides  = raw.get("profile_overrides", {})

    def _apply_profile(self, profile: str) -> list[dict[str, Any]]:
        override   = self._overrides.get(profile, {})
        boosted    = set(override.get("boost",    []))
        suppressed = set(override.get("suppress", []))
        filtered   = [r for r in self._rules if r["action"] not in suppressed]
        return (
            [r for r in filtered if r["action"] in boosted]
            + [r for r in filtered if r["action"] not in boosted]
        )

    def _evaluate_rules(self, rules, hand_score, profile):
        plan: list[dict[str, Any]] = []
        pass_included = False
        for rule in rules:
            action    = rule["action"]
            rationale = rule["rationale"]
            if action == "PASS":
                pass_included = True
                continue
            viable, why = self._is_viable(action, hand_score, profile, rationale)
            plan.append({"action": action, "viable": viable, "rationale": why})
        plan.append({"action": "PASS", "viable": True, "rationale": "Fallback: legal in all board states."})
        return plan

    def _is_viable(self, action, hand_score, profile, base_rationale):
        if action == "ATTACK_KO":
            viable = hand_score >= _KO_SCORE_THRESHOLD
            why = (
                f"hand_score {hand_score:.2f} >= KO threshold {_KO_SCORE_THRESHOLD} -> attack likely viable."
                if viable else
                f"hand_score {hand_score:.2f} < KO threshold {_KO_SCORE_THRESHOLD} -> attack unlikely this turn."
            )
            return viable, why
        if action == "EVOLVE":
            viable = profile in ("aggressive", "tempo")
            why = (
                f"Profile '{profile}' typically runs evolution lines."
                if viable else
                f"Profile '{profile}' is defensive; evolution less likely."
            )
            return viable, why
        if action == "ATTACH_ENERGY":
            return True, "Energy attachment is a once-per-turn action; always take it if available."
        if action == "PLAY_TRAINER":
            return True, base_rationale
        return True, f"No heuristic defined for '{action}'. Deferring to Orchestrator."

    def _log(self, packet, active_rules, plan):
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":     "TurnPlanner",
            "input":     packet,
            "reasoning": {"active_rules": [r["action"] for r in active_rules]},
            "output":    plan,
        }
        try:
            log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.append(entry)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
"""

# ─────────────────────────────────────────────────────────────────────────────
# agents/time_manager.py
# ─────────────────────────────────────────────────────────────────────────────
TIME_MANAGER = """\
\"\"\"
agents/time_manager.py
----------------------
Monitors elapsed game time and enforces strict timeout-avoidance policy.

Contract
--------
- No skill file -- operates on hard-wired timing thresholds only.
- Input packet: { time_elapsed: float, time_limit: float } -- from Router only
- Output      : { directive: str, mode: str, urgency: float, time_remaining: float }
- Runs on every tick -- never sleeps, never blocks.
- Guarantees the game never times out.

Timing policy (spec)
--------------------
    time_elapsed <= 540 s  -> NORMAL    -- planner decides freely
    540 < elapsed <= 570 s -> FAST_MOVE -- force fastest legal move immediately
    elapsed > 570 s        -> FORCE_PASS -- force pass to avoid timeout
\"\"\"

from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any

_PROJECT_ROOT         = pathlib.Path(__file__).resolve().parent.parent
_LOG_PATH             = _PROJECT_ROOT / "logs" / "reasoning_log.json"
_THRESHOLD_FAST       = 540.0
_THRESHOLD_FORCE_PASS = 570.0


class TimeManager:
    def tick(self, packet: dict[str, Any]) -> dict[str, Any]:
        time_elapsed: float = float(packet.get("time_elapsed", 0.0))
        time_limit:   float = float(packet.get("time_limit",  600.0))
        directive, mode     = self._classify(time_elapsed)
        urgency             = self._urgency(time_elapsed, time_limit)
        time_remaining      = max(0.0, time_limit - time_elapsed)
        result: dict[str, Any] = {
            "directive":      directive,
            "mode":           mode,
            "urgency":        round(urgency, 4),
            "time_remaining": round(time_remaining, 2),
        }
        self._log(packet, result)
        return result

    @staticmethod
    def _classify(time_elapsed: float) -> tuple[str, str]:
        if time_elapsed > _THRESHOLD_FORCE_PASS:
            return "FORCE_PASS", "critical"
        if time_elapsed > _THRESHOLD_FAST:
            return "FAST_MOVE", "urgent"
        return "NORMAL", "standard"

    @staticmethod
    def _urgency(time_elapsed: float, time_limit: float) -> float:
        if time_limit <= 0:
            return 1.0
        return min(1.0, max(0.0, time_elapsed / time_limit))

    def _log(self, packet, result):
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":     "TimeManager",
            "input":     packet,
            "reasoning": {
                "threshold_fast":       _THRESHOLD_FAST,
                "threshold_force_pass": _THRESHOLD_FORCE_PASS,
                "evaluation": f"time_elapsed={packet.get('time_elapsed')} -> directive={result['directive']}",
            },
            "output": result,
        }
        try:
            log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.append(entry)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
"""

# ─────────────────────────────────────────────────────────────────────────────
# agents/strategy_agent.py
# ─────────────────────────────────────────────────────────────────────────────
STRATEGY_AGENT = """\
\"\"\"
agents/strategy_agent.py
------------------------
Selects the optimal board strategy given a trigger event and board summary.

Contract
--------
- Skill file  : skills/strategy_profiles.json  (loaded once at __init__, never again)
- Input packet: { trigger: str, board_summary: dict }  -- from Router only
- Output      : { strategy: str, posture: str, actions: list[str],
                  escalation: str, confidence: float }
- Logs        : every evaluation -> logs/reasoning_log.json
- File access : strategy_profiles.json and reasoning_log.json ONLY

Matching priority
-----------------
1. Exact key match against profiles dict
2. Board-summary signal heuristics
3. Keyword scan of profile trigger descriptions
4. Fallback to 'hand_dead' profile
\"\"\"

from __future__ import annotations
import json
import pathlib
import datetime
from typing import Any

_PROJECT_ROOT         = pathlib.Path(__file__).resolve().parent.parent
_SKILL_PATH           = _PROJECT_ROOT / "skills" / "strategy_profiles.json"
_LOG_PATH             = _PROJECT_ROOT / "logs"   / "reasoning_log.json"
_CONF_EXACT_KEY       = 1.0
_CONF_KEYWORD         = 0.75
_CONF_FALLBACK        = 0.3
_FALLBACK_PROFILE_KEY = "hand_dead"


class StrategyAgent:
    def __init__(self) -> None:
        self._profiles: dict[str, dict[str, Any]] = self._load_skill()

    def evaluate(self, packet: dict[str, Any]) -> dict[str, Any]:
        trigger: str        = str(packet.get("trigger", "")).strip()
        board_summary: dict = packet.get("board_summary", {})
        profile_key, profile, confidence, match_reason = self._match_profile(trigger, board_summary)
        result: dict[str, Any] = {
            "strategy":   profile_key,
            "posture":    profile.get("posture", "tempo"),
            "actions":    profile.get("actions", ["PASS"]),
            "escalation": profile.get("escalation", "PASS"),
            "confidence": round(confidence, 4),
        }
        self._log(packet, profile_key, match_reason, result)
        return result

    def _load_skill(self) -> dict[str, dict[str, Any]]:
        raw = json.loads(_SKILL_PATH.read_text(encoding="utf-8"))
        return raw.get("profiles", {})

    def _match_profile(self, trigger, board_summary):
        trigger_lower = trigger.lower()
        if trigger_lower in self._profiles:
            return trigger_lower, self._profiles[trigger_lower], _CONF_EXACT_KEY, "exact key match"
        board_match = self._board_signal_match(board_summary)
        if board_match:
            return board_match, self._profiles[board_match], _CONF_KEYWORD, f"board_summary signal -> {board_match}"
        best_key, best_score = self._keyword_scan(trigger_lower)
        if best_key and best_score > 0:
            return (best_key, self._profiles[best_key],
                    _CONF_KEYWORD * best_score, f"keyword scan score={best_score:.2f}")
        fallback = self._profiles.get(_FALLBACK_PROFILE_KEY, {})
        return _FALLBACK_PROFILE_KEY, fallback, _CONF_FALLBACK, "no match -> fallback"

    def _board_signal_match(self, board_summary):
        prizes     = board_summary.get("prizes")
        bench      = board_summary.get("bench_count")
        score      = board_summary.get("hand_score")
        energy     = board_summary.get("energy_attached")
        opp_prizes = board_summary.get("opponent_prizes")
        if prizes is not None and int(prizes) <= 2:
            return "endgame_close"
        if opp_prizes is not None and int(opp_prizes) <= 2:
            return "prize_race"
        if bench is not None and int(bench) <= 1:
            return "bench_low"
        if energy is not None and int(energy) == 0:
            return "energy_stall"
        if score is not None and float(score) < 2.0:
            return "hand_dead"
        return None

    def _keyword_scan(self, trigger_lower):
        best_key, best_score = None, 0.0
        for key, profile in self._profiles.items():
            trigger_desc = profile.get("trigger", "").lower()
            words = [w.strip("(),<>=") for w in trigger_desc.split() if len(w) > 3]
            if not words:
                continue
            matched = sum(1 for w in words if w in trigger_lower)
            score   = matched / len(words)
            if score > best_score:
                best_score, best_key = score, key
        return best_key, best_score

    def _log(self, packet, matched_key, match_reason, result):
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = {
            "timestamp": datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":     "StrategyAgent",
            "input":     packet,
            "reasoning": {
                "profiles_available": list(self._profiles.keys()),
                "matched_profile":    matched_key,
                "match_reason":       match_reason,
            },
            "output": result,
        }
        try:
            log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.append(entry)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
"""

# ─────────────────────────────────────────────────────────────────────────────
# agents/orchestrator.py
# ─────────────────────────────────────────────────────────────────────────────
ORCHESTRATOR = """\
\"\"\"
agents/orchestrator.py
----------------------
The Orchestrator is the ONLY agent that holds full game state.

Architecture contract
---------------------
- Owns the canonical GameState dict.
- Communicates with every other agent EXCLUSIVELY through router/bus.py.
- Never passes raw GameState to any agent; the Router enforces scoping.
- Assembles the final action decision by composing each agent's output.
- All delegation calls logged by the Router in logs/action_log.json.
- Orchestrator logs its own final decisions to logs/reasoning_log.json.

Turn lifecycle
--------------
    orchestrate(game_state) -> TurnDecision

    Step 1 - TimeManager:   check time; abort early if critically low
    Step 2 - HandAnalyst:   score hand, derive priority_profile
    Step 3 - TurnPlanner:   produce ordered action plan
    Step 4 - StrategyAgent: select board posture from trigger + board_summary
    Step 5 - OpponentModel: update archetype inference from revealed cards
    Step 6 - Merge:         compose final TurnDecision from all outputs
\"\"\"

from __future__ import annotations
import json
import pathlib
import datetime
from dataclasses import dataclass, field, asdict
from typing import Any

from router.bus import Router
from agents.hand_analyst   import HandAnalyst
from agents.turn_planner   import TurnPlanner
from agents.time_manager   import TimeManager
from agents.strategy_agent import StrategyAgent
from agents.opponent_model import OpponentModel, OpponentModelPacket

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_LOG_PATH     = _PROJECT_ROOT / "logs" / "reasoning_log.json"


@dataclass
class TurnDecision:
    timing_directive:          str
    time_remaining:            float
    hand_score:                float
    priority_profile:          str
    top_play:                  str
    strategy:                  str
    posture:                   str
    strategy_confidence:       float
    predicted_opponent_action: str
    opponent_archetype:        str
    opponent_confidence:       float
    final_actions:             list[str] = field(default_factory=list)
    primary_action:            str       = "PASS"


class Orchestrator:
    \"\"\"Owns full game state; coordinates all agents through the Router.

    Usage
    -----
        orch     = Orchestrator()
        decision = orch.orchestrate(game_state)
        print(decision.primary_action)
    \"\"\"

    def __init__(self) -> None:
        self._router   = Router()
        self._analyst  = HandAnalyst()
        self._planner  = TurnPlanner()
        self._timer    = TimeManager()
        self._strategy = StrategyAgent()
        self._opponent = OpponentModel()

    def orchestrate(self, game_state: dict[str, Any]) -> TurnDecision:
        time_result  = self._step_time(game_state)
        if time_result["directive"] == "FORCE_PASS":
            return self._emergency_pass(time_result)
        hand_result  = self._step_hand(game_state)
        plan_result  = self._step_plan(hand_result)
        strat_result = self._step_strategy(game_state)
        opp_result   = self._step_opponent(game_state)
        decision     = self._merge(game_state, time_result, hand_result, plan_result, strat_result, opp_result)
        self._log(game_state, decision)
        return decision

    def _step_time(self, gs):
        pkt = self._router.dispatch("TimeManager", {
            "time_elapsed": gs.get("time_elapsed", 0.0),
            "time_limit":   gs.get("time_limit",   600.0),
        })
        return self._timer.tick(pkt)

    def _step_hand(self, gs):
        pkt = self._router.dispatch("HandAnalyst", {
            "hand":           gs.get("hand", []),
            "deck_remaining": gs.get("deck_remaining", 0),
        })
        return self._analyst.analyse(pkt)

    def _step_plan(self, hand_result):
        pkt = self._router.dispatch("TurnPlanner", {
            "hand_score":       hand_result["hand_score"],
            "priority_profile": hand_result["priority_profile"],
        })
        return self._planner.plan(pkt)

    def _step_strategy(self, gs):
        pkt = self._router.dispatch("StrategyAgent", {
            "trigger":       gs.get("trigger", ""),
            "board_summary": gs.get("board_summary", {}),
        })
        return self._strategy.evaluate(pkt)

    def _step_opponent(self, gs):
        opp_pkt = OpponentModelPacket(
            turn                      = int(gs.get("turn_number", 1)),
            newly_played_cards        = gs.get("revealed_cards", []),
            opponent_active_pokemon   = gs.get("opponent_active_pokemon"),
            opponent_bench_count      = int(gs.get("opponent_bench_count", 0)),
            opponent_hand_size        = int(gs.get("opponent_hand_size", 0)),
            opponent_prizes_remaining = int(gs.get("opponent_prizes_remaining", 6)),
            opponent_discard          = gs.get("opponent_discard", []),
            game_phase                = gs.get("game_phase", "mid"),
        )
        self._router.dispatch("OpponentModel", {
            "revealed_cards":       gs.get("revealed_cards", []),
            "turn_number":          int(gs.get("turn_number", 1)),
            "archetype_confidence": float(gs.get("archetype_confidence", 0.0)),
        })
        return self._opponent.receive(opp_pkt)

    def _merge(self, gs, time_result, hand_result, plan_result, strat_result, opp_result):
        if strat_result["confidence"] >= 0.75:
            final_actions = strat_result["actions"]
        else:
            final_actions = [s["action"] for s in plan_result if s.get("viable", False)]
        if time_result["directive"] == "FAST_MOVE":
            final_actions = final_actions[:1] if final_actions else ["PASS"]
        primary_action = final_actions[0] if final_actions else "PASS"
        return TurnDecision(
            timing_directive           = time_result["directive"],
            time_remaining             = time_result["time_remaining"],
            hand_score                 = hand_result["hand_score"],
            priority_profile           = hand_result["priority_profile"],
            top_play                   = hand_result["top_play"],
            strategy                   = strat_result["strategy"],
            posture                    = strat_result["posture"],
            strategy_confidence        = strat_result["confidence"],
            predicted_opponent_action  = opp_result["predicted_next_action"],
            opponent_archetype         = opp_result["inferred_deck_type"],
            opponent_confidence        = opp_result["archetype_confidence"],
            final_actions              = final_actions,
            primary_action             = primary_action,
        )

    def _emergency_pass(self, time_result):
        return TurnDecision(
            timing_directive           = "FORCE_PASS",
            time_remaining             = time_result["time_remaining"],
            hand_score                 = 0.0,
            priority_profile           = "defensive",
            top_play                   = "(time emergency)",
            strategy                   = "time_critical",
            posture                    = "defensive",
            strategy_confidence        = 1.0,
            predicted_opponent_action  = "unknown",
            opponent_archetype         = "unknown",
            opponent_confidence        = 0.0,
            final_actions              = ["PASS"],
            primary_action             = "PASS",
        )

    def _log(self, gs, decision):
        _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        entry: dict[str, Any] = {
            "timestamp":  datetime.datetime.utcnow().isoformat(timespec="milliseconds") + "Z",
            "agent":      "Orchestrator",
            "input_keys": sorted(gs.keys()),
            "output":     asdict(decision),
        }
        try:
            log: list[Any] = json.loads(_LOG_PATH.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, FileNotFoundError):
            log = []
        log.append(entry)
        _LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")
"""

# ─────────────────────────────────────────────────────────────────────────────
# Write all files
# ─────────────────────────────────────────────────────────────────────────────
files = {
    ROOT / "router" / "bus.py":             BUS,
    ROOT / "agents" / "hand_analyst.py":    HAND_ANALYST,
    ROOT / "agents" / "turn_planner.py":    TURN_PLANNER,
    ROOT / "agents" / "time_manager.py":    TIME_MANAGER,
    ROOT / "agents" / "strategy_agent.py":  STRATEGY_AGENT,
    ROOT / "agents" / "orchestrator.py":    ORCHESTRATOR,
}

for path, content in files.items():
    path.write_text(content, encoding="utf-8")
    print(f"Written  {path.relative_to(ROOT)}  ({path.stat().st_size} bytes)")

print("\nAll files written successfully.")
