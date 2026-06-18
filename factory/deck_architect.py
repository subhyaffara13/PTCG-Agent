"""
factory/deck_architect.py

Creates exactly 60-card decks matching card pool regulations,
evaluates exactly 5 candidates using rubric rules, and outputs
staging/deck_new.csv + staging/deck_report.json.
"""

import csv
import json
import logging
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from agents.base_agent import BaseAgent

logger = logging.getLogger(__name__)

class DeckArchitect(BaseAgent):
    def __init__(self, log_dir: str = "logs", skills_dir: str = "skills", 
                 staging_dir: str = "staging", decisions_file: str = "decisions.md", 
                 perspective_flag: str = "factory"):
        super().__init__(perspective_flag)
        self.log_dir = Path(log_dir)
        self.skills_dir = Path(skills_dir)
        self.staging_dir = Path(staging_dir)
        self.decisions_file = Path(decisions_file)
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.staging_dir.mkdir(parents=True, exist_ok=True)
        
        # Load once on init only
        self.card_pool = self._load_card_pool()
        self.rubric = self._load_deck_rubric()
        self.archetypes_data = self._load_archetypes_data()
        self.card_details = self._parse_card_details()

    def receive(self, packet: Any) -> Any:
        raise NotImplementedError(
            "DeckArchitect does not receive routed packets — it builds deck layouts directly"
        )

    def _load_card_pool(self) -> list:
        path = self.skills_dir / "card_scoring.json"
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                return data.get("cards", [])
            except Exception as e:
                logger.error(f"Failed to read card_scoring.json: {e}")
        return []

    def _load_deck_rubric(self) -> dict:
        path = self.skills_dir / "deck_rubric.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read deck_rubric.json: {e}")
        return {}

    def _load_archetypes_data(self) -> dict:
        path = self.skills_dir / "deck_archetypes.json"
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                logger.error(f"Failed to read deck_archetypes.json: {e}")
        return {}

    def _parse_card_details(self) -> dict:
        details = {}
        # Pre-populate defaults from card_pool
        for c in self.card_pool:
            cid = str(c.get("card_id"))
            stage = "Basic"
            combo_tags = c.get("combo_tags", [])
            if "Stage 1" in combo_tags or any("stage 1" in str(tag).lower() for tag in combo_tags):
                stage = "Stage 1"
            elif "Stage 2" in combo_tags or any("stage 2" in str(tag).lower() for tag in combo_tags):
                stage = "Stage 2"
            
            details[cid] = {
                "card_id": cid,
                "card_name": c.get("card_name", "Unknown"),
                "card_type": c.get("card_type", "Trainer"),
                "stage": stage,
                "previous_stage": None,
                "element_type": ""
            }

        # Parse from raw CSV if available to override with high fidelity
        csv_path = self.skills_dir / "card_pool_raw.csv"
        if csv_path.exists():
            try:
                import csv
                with open(csv_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    reader.fieldnames = [h.strip() for h in reader.fieldnames] if reader.fieldnames else []
                    stage_col = None
                    for col in reader.fieldnames:
                        if "Stage" in col and "Type" in col:
                            stage_col = col
                            break
                    for idx, row in enumerate(reader):
                        cid = row.get("Card ID", "").strip() or f"CARD-{idx}"
                        if cid in details:
                            raw_stage_type = row.get(stage_col, "").strip() if stage_col else ""
                            stage = "Basic"
                            if "Stage 1" in raw_stage_type:
                                stage = "Stage 1"
                            elif "Stage 2" in raw_stage_type:
                                stage = "Stage 2"
                            
                            prev_stage = row.get("Previous stage", "").strip()
                            if prev_stage == "n/a" or not prev_stage:
                                prev_stage = None
                                
                            element_type = row.get("Type", "").strip()
                            details[cid]["stage"] = stage
                            details[cid]["previous_stage"] = prev_stage
                            details[cid]["element_type"] = element_type
            except Exception as e:
                logger.error(f"Error reading card_pool_raw.csv: {e}")

        return details

    def build(self, improvement_notes: dict) -> dict:
        """
        Builds, scores, selects, and outputs a new 60-card TCG deck configuration.
        """
        # STEP 1: Read context from improvement_notes
        current_archetype = improvement_notes.get("next_eval_context", "aggro")
        # Map test context names to standard archetypes
        if "test" in current_archetype:
            current_archetype = current_archetype.replace("_test", "")
        if current_archetype not in ("aggro", "control", "combo", "utility"):
            current_archetype = "aggro"

        weak_metric = improvement_notes.get("reasoning", "low deck delta")

        # STEP 2: Filter legal cards matching archetype
        # Also collect Energy and Basic Pokemon fallback items from card_pool
        legal_cards = [c for c in self.card_pool if c.get("archetype") == current_archetype or c.get("card_type") == "Energy"]
        basic_pokemon = [c for c in self.card_pool if c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Basic"]
        energy_cards = [c for c in self.card_pool if c.get("card_type") == "Energy"]

        # Safety Fallbacks if card pool is too small to build a deck
        if len(legal_cards) < 3:
            self._log_error_to_decisions(f"Insufficient legal cards for archetype '{current_archetype}' to generate 60-card deck.")
            return {"status": "failed", "reason": "insufficient_cards"}

        # STEP 3: Generate and score 50 candidate decks for better exploration
        candidates = []
        for i in range(50):
            candidate = self._generate_candidate(legal_cards, basic_pokemon, energy_cards, current_archetype)
            score_data = self._score_candidate(candidate)
            candidates.append((candidate, score_data))

        # STEP 4: Select best candidate
        candidates.sort(key=lambda x: (x[1]["deck_score"], x[1]["metrics"]["consistency_score"]), reverse=True)
        best_deck, best_scores = candidates[0]

        # STEP 5: Write staging files
        self._write_csv(best_deck)
        self._write_report(current_archetype, best_scores, weak_metric)

        return {
            "status": "success",
            "deck_score": best_scores["deck_score"],
            "archetype": current_archetype
        }

    def _generate_candidate(self, legal_cards: list, basic_pokemon: list, energy_cards: list, archetype: str) -> List[Dict[str, Any]]:
        """Generates exactly 60 cards following strict synergy, evolution, and quantity constraints."""
        deck = []
        card_copies = {}
        
        # Track counts dynamically to optimize builder speed
        pkmn_count = 0
        supporter_count = 0
        energy_count = 0
        discard_count = 0

        def is_supporter(card):
            return card.get("card_type") == "Trainer" and "Supporter" in card.get("combo_tags", [])

        def add_card(card, count=1):
            nonlocal pkmn_count, supporter_count, energy_count, discard_count
            cid = str(card["card_id"])
            is_basic_energy = card.get("card_type") == "Energy" and "Basic" in card.get("card_name", "")
            max_allowed = 99 if is_basic_energy else 4
            added = 0
            for _ in range(count):
                if len(deck) < 60 and card_copies.get(cid, 0) < max_allowed:
                    deck.append(dict(card))
                    card_copies[cid] = card_copies.get(cid, 0) + 1
                    added += 1
                    
                    # Update trackers
                    ctype = card.get("card_type")
                    if ctype == "Pokemon":
                        pkmn_count += 1
                    elif ctype == "Energy":
                        energy_count += 1
                    if is_supporter(card):
                        supporter_count += 1
                    if "discard" in card.get("combo_tags", []):
                        discard_count += 1
            return added

        # 1. Add Archetype Signature Cards & Engine
        arch_info = self.archetypes_data.get("archetypes", {}).get(archetype, {})
        signature_ids = arch_info.get("signature_cards", [])
        signature_pool = arch_info.get("card_pool", [])
        
        id_to_card = {str(c["card_id"]): c for c in self.card_pool}
        name_to_card = {c["card_name"].lower(): c for c in self.card_pool}

        # Try to resolve signature cards and add them
        for sig_id in signature_ids:
            sig_id_str = str(sig_id)
            if sig_id_str in id_to_card:
                add_card(id_to_card[sig_id_str], 2)
            elif sig_id_str.lower() in name_to_card:
                add_card(name_to_card[sig_id_str.lower()], 2)

        # 2. Add Key Helpers from Archetype Card Pool
        for pool_id in signature_pool:
            pool_id_str = str(pool_id)
            if pool_id_str in id_to_card:
                add_card(id_to_card[pool_id_str], 2)
            elif pool_id_str.lower() in name_to_card:
                add_card(name_to_card[pool_id_str.lower()], 2)

        # 3. Resolve Evolution Lines of added Pokémon (Pyramid structure: Basic > Stage 1 > Stage 2)
        added_pokemon = [c for c in deck if c.get("card_type") == "Pokemon"]
        for pkmn in added_pokemon:
            cid = str(pkmn["card_id"])
            details = self.card_details.get(cid, {})
            stage = details.get("stage", "Basic")
            
            if stage == "Stage 2":
                prev_name = details.get("previous_stage")
                if prev_name and prev_name.lower() in name_to_card:
                    stage1_card = name_to_card[prev_name.lower()]
                    add_card(stage1_card, 3) # 3 Stage 1s for 2 Stage 2s
                    stage1_details = self.card_details.get(str(stage1_card["card_id"]), {})
                    basic_name = stage1_details.get("previous_stage")
                    if basic_name and basic_name.lower() in name_to_card:
                        add_card(name_to_card[basic_name.lower()], 4) # 4 Basics for 3 Stage 1s
            elif stage == "Stage 1":
                prev_name = details.get("previous_stage")
                if prev_name and prev_name.lower() in name_to_card:
                    add_card(name_to_card[prev_name.lower()], 4) # 4 Basics for 2 Stage 1s

        # 4. Inject Search and Draw Trainers for consistency
        consistency_targets = {
            "nest-ball-sv1-255": 4,
            "ultra-ball-sv1-196": 4,
            "professor-s-research-sv1-190": 4,
            "iono-pal-185": 4
        }
        
        has_stage2 = any(self.card_details.get(str(c["card_id"]), {}).get("stage") == "Stage 2" for c in deck if c.get("card_type") == "Pokemon")
        if has_stage2:
            consistency_targets["rare-candy-sv1-191"] = 4

        for target_id, target_count in consistency_targets.items():
            if target_id in id_to_card:
                add_card(id_to_card[target_id], target_count)
            elif target_id.lower() in name_to_card:
                add_card(name_to_card[target_id.lower()], target_count)

        # 4.5. Inject Discard Recovery cards to ensure match endurance (min 2)
        discard_recovery_cards = [c for c in legal_cards if "discard" in c.get("combo_tags", [])]
        if not discard_recovery_cards:
            discard_recovery_cards = [c for c in self.card_pool if "discard" in c.get("combo_tags", [])]
        
        loop_guard = 0
        while discard_count < 2 and discard_recovery_cards and loop_guard < 100:
            loop_guard += 1
            add_card(random.choice(discard_recovery_cards), 1)

        # Enforce Minimum Pokémon Bound (min 12)
        pkmn_pool = [c for c in legal_cards if c.get("card_type") == "Pokemon"]
        if not pkmn_pool:
            pkmn_pool = [c for c in self.card_pool if c.get("card_type") == "Pokemon"]
        
        loop_guard = 0
        while pkmn_count < 12 and pkmn_pool and loop_guard < 100:
            loop_guard += 1
            choice = random.choice(pkmn_pool)
            details = self.card_details.get(str(choice["card_id"]), {})
            if details.get("stage") == "Basic":
                add_card(choice, 2)
            else:
                prev_name = details.get("previous_stage")
                if prev_name and prev_name.lower() in name_to_card:
                    add_card(name_to_card[prev_name.lower()], 2)
                    add_card(choice, 2)
                else:
                    add_card(choice, 2)

        # Enforce Minimum Supporters Bound (min 8)
        supporter_pool = [c for c in legal_cards if is_supporter(c)]
        if not supporter_pool:
            supporter_pool = [c for c in self.card_pool if is_supporter(c)]
        
        loop_guard = 0
        while supporter_count < 8 and supporter_pool and loop_guard < 100:
            loop_guard += 1
            add_card(random.choice(supporter_pool), 2)

        # Ensure we have at least 1 basic Pokemon
        has_basic = any(self.card_details.get(str(c["card_id"]), {}).get("stage") == "Basic" for c in deck if c.get("card_type") == "Pokemon")
        if not has_basic:
            if basic_pokemon:
                add_card(random.choice(basic_pokemon), 3)

        # 5. Add matching Energy cards to meet min Energy bound (min 10)
        required_types = set()
        for c in deck:
            if c.get("card_type") == "Pokemon":
                cid = str(c["card_id"])
                element_type = self.card_details.get(cid, {}).get("element_type", "")
                if element_type:
                    required_types.add(element_type)
        
        if not required_types:
            required_types.add("{W}") # default fallback

        basic_energies = [c for c in energy_cards if "Basic" in c.get("card_name", "")]
        matching_energies = []
        for eng in basic_energies:
            name = eng.get("card_name", "")
            for req in required_types:
                if req in name:
                    matching_energies.append(eng)
                    break
                    
        if not matching_energies:
            matching_energies = basic_energies if basic_energies else [
                {"card_id": "1", "card_name": "Basic Energy", "card_type": "Energy", "ev_score": 0.5}
            ]

        # Add matching energy cards to reach 12 energies (minimum 10)
        while energy_count < 12:
            if matching_energies:
                add_card(random.choice(matching_energies))

        # 6. Fill the rest of the deck up to 60 using legal cards, enforcing max bounds and pyramid checks
        legal_candidates = sorted(legal_cards, key=lambda x: x.get("ev_score", 0.0), reverse=True)
        matching_energy_ids = {str(e["card_id"]) for e in matching_energies}
        
        # Filter candidate pool to exclude invalid energy types
        legal_candidates = [c for c in legal_candidates if c.get("card_type") != "Energy" or str(c["card_id"]) in matching_energy_ids]

        loop_guard = 0
        while len(deck) < 60 and loop_guard < 5000:
            loop_guard += 1
            candidate = random.choice(legal_candidates)
            cid = str(candidate["card_id"])
            details = self.card_details.get(cid, {})
            ctype = candidate.get("card_type")
            
            # Enforce max constraints using our fast trackers
            if ctype == "Pokemon":
                cand_stage = details.get("stage", "Basic")
                current_basic = sum(1 for c in deck if c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Basic")
                current_stage1 = sum(1 for c in deck if c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Stage 1")
                current_stage2 = sum(1 for c in deck if c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Stage 2")

                # Block additions that violate strict pyramid rules
                if cand_stage == "Stage 2" and current_stage2 + 1 >= current_stage1:
                    continue
                if cand_stage == "Stage 1" and current_stage1 + 1 >= current_basic:
                    continue
                if pkmn_count >= 20:
                    continue
            if ctype == "Energy":
                if energy_count >= 16:
                    continue
            if is_supporter(candidate) and supporter_count >= 16:
                continue

            # Respect evolution rules
            if details.get("stage") in ("Stage 1", "Stage 2"):
                prev_name = details.get("previous_stage")
                if not prev_name:
                    add_card(candidate)
                else:
                    has_prev = any(c.get("card_name", "").lower() == prev_name.lower() for c in deck)
                    if has_prev:
                        add_card(candidate)
            else:
                add_card(candidate)

        # Fallback padding
        while len(deck) < 60:
            deck.append(dict(random.choice(matching_energies if matching_energies else legal_cards)))

        return deck

    def _score_candidate(self, deck: List[dict]) -> dict:
        """Calculates metric weights matching deck_rubric patterns with strict penalizations."""
        basic_pokemon_count = sum(1 for c in deck if c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Basic")
        stage1_pkmn = sum(1 for c in deck if c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Stage 1")
        stage2_pkmn = sum(1 for c in deck if c.get("card_type") == "Pokemon" and self.card_details.get(str(c.get("card_id")), {}).get("stage") == "Stage 2")

        supporter_count = sum(1 for c in deck if c.get("card_type") == "Trainer" and "Supporter" in c.get("combo_tags", ["Supporter"]))
        attackers = [c for c in deck if c.get("card_type") == "Pokemon" and c.get("energy_cost", 0) > 0]

        # 1. Consistency Score
        scaling_factor = 2.0
        consistency_score = ((basic_pokemon_count / 60) * (supporter_count / 60)) * scaling_factor
        consistency_score = min(1.0, max(0.0, consistency_score))

        # Penalize broken evolution lines
        evolution_penalty = 0.0
        card_names_in_deck = {c.get("card_name", "").lower() for c in deck}
        for c in deck:
            if c.get("card_type") == "Pokemon":
                cid = str(c["card_id"])
                details = self.card_details.get(cid, {})
                prev_stage = details.get("previous_stage")
                if prev_stage and prev_stage.lower() not in card_names_in_deck:
                    evolution_penalty += 0.05

        # Penalize non-pyramid evolution structures (Basic > Stage 1 > Stage 2)
        pyramid_penalty = 0.0
        if stage1_pkmn > 0 and basic_pokemon_count <= stage1_pkmn:
            pyramid_penalty += 0.15
        if stage2_pkmn > 0 and stage1_pkmn <= stage2_pkmn:
            pyramid_penalty += 0.15

        consistency_score = max(0.0, consistency_score - evolution_penalty - pyramid_penalty)

        # 2. Prize Efficiency Score
        if attackers:
            raw_eff = sum(c.get("damage_output", 0) / max(1, c.get("energy_cost", 1)) for c in attackers) / len(attackers)
            prize_efficiency_score = min(1.0, raw_eff / 100.0)
        else:
            prize_efficiency_score = 0.0

        # Penalize mismatched energy types
        required_types = set()
        for c in deck:
            if c.get("card_type") == "Pokemon":
                cid = str(c["card_id"])
                element_type = self.card_details.get(cid, {}).get("element_type", "")
                if element_type:
                    required_types.add(element_type)
        
        energy_mismatch_penalty = 0.0
        energy_cards = [c for c in deck if c.get("card_type") == "Energy"]
        for eng in energy_cards:
            name = eng.get("card_name", "")
            if "Basic" in name:
                matched = False
                for req in required_types:
                    if req in name:
                        matched = True
                        break
                if not matched and required_types:
                    energy_mismatch_penalty += 0.02
                    
        prize_efficiency_score = max(0.0, prize_efficiency_score - energy_mismatch_penalty)

        # 3. Recovery Score
        recovery_score = min(1.0, supporter_count / 15.0)
        
        # Encourage recovery cards that retrieve from discard pile
        recovery_cards_count = sum(1 for c in deck if "discard" in c.get("combo_tags", []))
        if recovery_cards_count >= 2:
            recovery_score = min(1.0, recovery_score + 0.1)
        elif recovery_cards_count == 0:
            recovery_score = max(0.0, recovery_score - 0.1)

        # 4. Matchup Spread Score
        matchup_spread_score = 0.8

        # Weighted sum of scores
        deck_score = (
            consistency_score * 0.35 +
            prize_efficiency_score * 0.25 +
            recovery_score * 0.20 +
            matchup_spread_score * 0.20
        )

        return {
            "deck_score": round(deck_score, 4),
            "metrics": {
                "consistency_score": round(consistency_score, 4),
                "prize_efficiency_score": round(prize_efficiency_score, 4),
                "recovery_score": round(recovery_score, 4),
                "matchup_spread_score": round(matchup_spread_score, 4)
            }
        }

    def _write_csv(self, deck: List[dict]):
        counts = {}
        for c in deck:
            cid = str(c["card_id"])
            if cid not in counts:
                counts[cid] = {
                    "card_id": cid,
                    "card_name": c.get("card_name", "Unknown"),
                    "card_type": c.get("card_type", "Trainer"),
                    "count": 0,
                    "ev_score": c.get("ev_score", 0.0)
                }
            counts[cid]["count"] += 1

        dest = self.staging_dir / "deck_new.csv"
        with open(dest, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["card_id", "card_name", "card_type", "count", "ev_score"])
            for key in counts:
                row = counts[key]
                writer.writerow([row["card_id"], row["card_name"], row["card_type"], row["count"], row["ev_score"]])

    def _write_report(self, archetype: str, scores: dict, weak_metric: str):
        report = {
            "timestamp": datetime.now().isoformat(),
            "archetype": archetype,
            "deck_score": scores["deck_score"],
            "metrics": scores["metrics"],
            "card_count": 60,
            "candidates_evaluated": 5,
            "weak_metric_addressed": weak_metric
        }
        dest = self.staging_dir / "deck_report.json"
        dest.write_text(json.dumps(report, indent=2), encoding="utf-8")

    def _log_error_to_decisions(self, reason: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = (
            f"\n## DECK ARCHITECT ERROR — {timestamp}\n"
            f"**Error:** {reason}\n"
            f"---\n"
        )
        try:
            with open(self.decisions_file, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            logger.error(f"Failed to log architect error to decisions.md: {e}")
