"""
agents/opponent_model.py

Models the opponent's publicly visible game state and predicts their next action
using Bayesian archetype inference against skills/deck_archetypes.json.

Isolation contract (enforced by router/bus.py):
    - This agent accepts ONLY OpponentModelPacket.
    - It NEVER receives the player's hand, deck, or private state.
    - All inference derives exclusively from publicly observed opponent actions.

Data flow:
    Bus  →  OpponentModelPacket  →  OpponentModel.receive()
         →  updates RevealedState  (ground truth)
         →  updates InferredState  (Bayesian fill from deck_archetypes.json)
         →  returns {
                predicted_next_action: str,
                archetype_confidence:  float,   # confidence in top archetype
                inferred_deck_type:    str,
            }
"""

from __future__ import annotations

import json
import math
import logging
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_SKILLS_DIR = Path(__file__).parent.parent / "skills"
_ARCHETYPES_PATH = _SKILLS_DIR / "deck_archetypes.json"

# ---------------------------------------------------------------------------
# Packet (router contract — this is the ONLY input type accepted)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class OpponentModelPacket:
    """
    The single packet type the bus delivers to this agent.

    Fields are limited to information that is *publicly visible* in a real
    Pokémon TCG game:  active Pokémon, bench count, hand size (not contents),
    prizes remaining, discard pile (visible), and any cards actually played
    this turn.

    NEVER include player hand, player deck, or any private state here.
    """

    turn: int
    newly_played_cards: list[str]       # card_ids played by opponent this turn
    opponent_active_pokemon: str | None # card_id of active Pokémon (or None)
    opponent_bench_count: int           # 0–5
    opponent_hand_size: int             # card count only — not card identities
    opponent_prizes_remaining: int      # 1–6
    opponent_discard: list[str]         # card_ids visible in discard pile
    game_phase: str                     # "early" | "mid" | "late"

# ---------------------------------------------------------------------------
# State containers
# ---------------------------------------------------------------------------

@dataclass
class RevealedState:
    """
    Ground truth — cards the opponent has *actually* played.
    Updated directly from OpponentModelPacket fields.
    Never inferred; only observed.
    """

    played_cards: list[str] = field(default_factory=list)
    active_pokemon: str | None = None
    bench_count: int = 0
    hand_size: int = 0
    prizes_remaining: int = 6
    discard_pile: list[str] = field(default_factory=list)
    turn_count: int = 0

    def apply_packet(self, packet: OpponentModelPacket) -> list[str]:
        """
        Merge packet into revealed state.

        Returns the list of card_ids that are *new* since the last update
        (used by the Bayesian updater to compute evidence).
        """
        new_cards = [c for c in packet.newly_played_cards if c not in self.played_cards]
        self.played_cards.extend(new_cards)

        # merge discard — deduplicate while preserving order
        seen = set(self.discard_pile)
        for c in packet.opponent_discard:
            if c not in seen:
                self.discard_pile.append(c)
                seen.add(c)

        self.active_pokemon = packet.opponent_active_pokemon
        self.bench_count = packet.opponent_bench_count
        self.hand_size = packet.opponent_hand_size
        self.prizes_remaining = packet.opponent_prizes_remaining
        self.turn_count = packet.turn
        return new_cards


@dataclass
class InferredState:
    """
    Probabilistic model of the opponent's deck, derived from deck_archetypes.json.
    Never contains the player's private state.
    """

    inferred_deck_type: str = "unknown"
    archetype_priors: dict[str, float] = field(default_factory=dict)   # raw log-probs
    archetype_confidence: dict[str, float] = field(default_factory=dict)  # normalised
    probable_remaining_cards: list[str] = field(default_factory=list)
    predicted_next_action: str = "unknown"

    @property
    def top_archetype(self) -> str:
        if not self.archetype_confidence:
            return "unknown"
        return max(self.archetype_confidence, key=self.archetype_confidence.__getitem__)

    @property
    def top_confidence(self) -> float:
        if not self.archetype_confidence:
            return 0.0
        return self.archetype_confidence[self.top_archetype]

# ---------------------------------------------------------------------------
# Main agent
# ---------------------------------------------------------------------------

class OpponentModel:
    """
    Opponent modelling sub-agent.

    Initialized with ``perspective_flag="opponent"`` to mark that all state
    it holds belongs to the *opponent*, not the player.  The router bus
    checks this flag before delivery to enforce the information boundary.

    Usage
    -----
    ::

        model = OpponentModel()
        result = model.receive(packet)
        # result → {
        #     "predicted_next_action": "attack",
        #     "archetype_confidence": 0.74,
        #     "inferred_deck_type": "aggro",
        # }
    """

    PERSPECTIVE_FLAG = "opponent"   # router reads this to enforce isolation

    def __init__(self) -> None:
        self.perspective_flag: str = self.PERSPECTIVE_FLAG
        self._archetypes: dict[str, Any] = self._load_archetypes()
        self.revealed: RevealedState = RevealedState()
        self.inferred: InferredState = InferredState()
        self._initialize_priors()
        logger.info("OpponentModel initialised (perspective=%s)", self.perspective_flag)

    # ------------------------------------------------------------------
    # Initialisation helpers
    # ------------------------------------------------------------------

    def _load_archetypes(self) -> dict[str, Any]:
        """Load deck_archetypes.json. Returns empty dict on failure."""
        try:
            data = json.loads(_ARCHETYPES_PATH.read_text(encoding="utf-8"))
            archetypes = data.get("archetypes", {})
            logger.debug("Loaded %d archetypes from %s", len(archetypes), _ARCHETYPES_PATH)
            return archetypes
        except FileNotFoundError:
            logger.warning("deck_archetypes.json not found at %s — using empty archetypes", _ARCHETYPES_PATH)
            return {}
        except json.JSONDecodeError as exc:
            logger.error("Invalid JSON in deck_archetypes.json: %s", exc)
            return {}

    def _initialize_priors(self) -> None:
        """
        Set uniform log-probability priors across all known archetypes.
        Uses log-space to avoid floating-point underflow during updates.
        """
        if not self._archetypes:
            self.inferred.archetype_priors = {}
            self.inferred.archetype_confidence = {}
            return

        uniform = -math.log(len(self._archetypes))   # ln(1/n)
        self.inferred.archetype_priors = {k: uniform for k in self._archetypes}
        self._normalise_priors()

    def _normalise_priors(self) -> None:
        """Convert log-priors to a normalised probability distribution."""
        priors = self.inferred.archetype_priors
        if not priors:
            return

        # log-sum-exp for numerical stability
        max_log = max(priors.values())
        total = sum(math.exp(v - max_log) for v in priors.values())
        self.inferred.archetype_confidence = {
            k: math.exp(v - max_log) / total for k, v in priors.items()
        }
        self.inferred.inferred_deck_type = self.inferred.top_archetype

    # ------------------------------------------------------------------
    # Public entry point (router calls this)
    # ------------------------------------------------------------------

    def receive(self, packet: OpponentModelPacket) -> dict[str, Any]:
        """
        Process one OpponentModelPacket and return a prediction payload.

        Parameters
        ----------
        packet : OpponentModelPacket
            Delivery from router/bus.py.  Must not contain player-private info.

        Returns
        -------
        dict with keys:
            predicted_next_action : str
            archetype_confidence  : float   — confidence score of top archetype
            inferred_deck_type    : str
        """
        self._assert_packet_type(packet)

        # 1. Update ground-truth revealed state; get newly observed cards
        new_cards = self.revealed.apply_packet(packet)
        logger.debug("Turn %d: %d new card(s) observed — %s", packet.turn, len(new_cards), new_cards)

        # 2. Bayesian update on archetype priors from new evidence
        if new_cards:
            self._update_archetype_confidence(new_cards)

        # 3. Infer probable remaining cards from top archetype
        self._infer_remaining_cards()

        # 4. Predict next action
        self.inferred.predicted_next_action = self._predict_next_action(packet.game_phase)

        return self._build_response()

    # ------------------------------------------------------------------
    # Bayesian inference
    # ------------------------------------------------------------------

    def _update_archetype_confidence(self, newly_played_cards: list[str]) -> None:
        """
        Update log-prior for each archetype using new card evidence.

        Likelihood model:
            - If the card is in an archetype's ``signature_cards``:  +2.0 log-pts
            - If the card is in an archetype's ``card_pool``:        +0.5 log-pts
            - If the card is in neither:                             -0.3 log-pts
              (slight evidence *against*, but not conclusive — pool data may be incomplete)

        After updating all archetypes, priors are re-normalised.
        """
        SIGNATURE_BOOST = 2.0
        POOL_BOOST      = 0.5
        MISS_PENALTY    = -0.3

        for archetype, log_prior in self.inferred.archetype_priors.items():
            arch_data = self._archetypes.get(archetype, {})
            sig_cards  = set(arch_data.get("signature_cards", []))
            card_pool  = set(arch_data.get("card_pool", []))

            delta = 0.0
            for card_id in newly_played_cards:
                if card_id in sig_cards:
                    delta += SIGNATURE_BOOST
                elif card_id in card_pool:
                    delta += POOL_BOOST
                else:
                    delta += MISS_PENALTY

            self.inferred.archetype_priors[archetype] = log_prior + delta

        self._normalise_priors()
        logger.debug(
            "Archetype confidences after update: %s",
            {k: f"{v:.2f}" for k, v in self.inferred.archetype_confidence.items()},
        )

    def _infer_remaining_cards(self) -> None:
        """
        Fill ``inferred_state.probable_remaining_cards`` from the top archetype's
        ``card_pool``, excluding cards already seen in ``revealed_state.played_cards``
        and ``revealed_state.discard_pile``.
        """
        top = self.inferred.top_archetype
        arch_data = self._archetypes.get(top, {})
        pool = arch_data.get("card_pool", [])

        already_seen = set(self.revealed.played_cards) | set(self.revealed.discard_pile)
        self.inferred.probable_remaining_cards = [c for c in pool if c not in already_seen]

    # ------------------------------------------------------------------
    # Action prediction
    # ------------------------------------------------------------------

    def _predict_next_action(self, game_phase: str) -> str:
        """
        Predict the opponent's most likely next action.

        Priority logic:
            1. If the opponent is in prize-race mode (aggro, low prizes remaining),
               predict ``attack``.
            2. If the opponent has a small hand and it's early game, predict
               ``play_supporter`` (draw/search).
            3. Fall back to the archetype's phase-typical action list.
            4. If archetypes are unavailable, return ``"unknown"``.
        """
        top = self.inferred.top_archetype
        if top == "unknown" or top not in self._archetypes:
            return "unknown"

        arch_data = self._archetypes[top]
        phase_actions: list[str] = arch_data.get("typical_actions", {}).get(game_phase, [])

        # Override 1 — aggro prize-race: if prizes ≤ 2 and aggro, almost certainly attacking
        prize_race_priority: float = arch_data.get("prize_race_priority", 0.5)
        if (
            self.revealed.prizes_remaining <= 2
            and prize_race_priority >= 0.8
            and self.inferred.top_confidence >= 0.5
        ):
            return "attack"

        # Override 2 — low hand size in early game → likely to draw/search
        if self.revealed.hand_size <= 2 and game_phase == "early":
            return "play_supporter"

        # Fallback to archetype phase-action list
        if phase_actions:
            return phase_actions[0]

        return "unknown"

    # ------------------------------------------------------------------
    # Response builder
    # ------------------------------------------------------------------

    def _build_response(self) -> dict[str, Any]:
        """Return the standardised response dict consumed by the orchestrator."""
        return {
            "predicted_next_action": self.inferred.predicted_next_action,
            "archetype_confidence":  round(self.inferred.top_confidence, 4),
            "inferred_deck_type":    self.inferred.inferred_deck_type,
        }

    # ------------------------------------------------------------------
    # Safety guard
    # ------------------------------------------------------------------

    def _assert_packet_type(self, packet: Any) -> None:
        """Hard-fail if a non-OpponentModelPacket is delivered to this agent."""
        if not isinstance(packet, OpponentModelPacket):
            raise TypeError(
                f"OpponentModel received an illegal packet type: {type(packet).__name__}. "
                "The router bus must only deliver OpponentModelPacket to this agent. "
                "Check router/bus.py delegation_map enforcement."
            )

    # ------------------------------------------------------------------
    # Debug helpers
    # ------------------------------------------------------------------

    def snapshot(self) -> dict[str, Any]:
        """Return a read-only snapshot of both state objects (for logging)."""
        return {
            "revealed": {
                "played_cards":      list(self.revealed.played_cards),
                "active_pokemon":    self.revealed.active_pokemon,
                "bench_count":       self.revealed.bench_count,
                "hand_size":         self.revealed.hand_size,
                "prizes_remaining":  self.revealed.prizes_remaining,
                "discard_pile":      list(self.revealed.discard_pile),
                "turn_count":        self.revealed.turn_count,
            },
            "inferred": {
                "inferred_deck_type":       self.inferred.inferred_deck_type,
                "archetype_confidence":     dict(self.inferred.archetype_confidence),
                "probable_remaining_cards": list(self.inferred.probable_remaining_cards),
                "predicted_next_action":    self.inferred.predicted_next_action,
            },
        }

    def reset(self) -> None:
        """
        Reset to initial state (call between games, not between turns).
        Archetypes data is preserved; only game-state is cleared.
        """
        self.revealed = RevealedState()
        self.inferred = InferredState()
        self._initialize_priors()
        logger.info("OpponentModel reset for new game.")
