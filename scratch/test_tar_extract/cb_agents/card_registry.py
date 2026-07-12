import logging
from pathlib import Path
from typing import Dict, Any, Optional
from cb_agents.card_types import (
    CardType, CardStage, TrainerSubtype, ComboTag, TRAINER_MAP, COMBO_TAG_MAP
)
from cb_agents.card_entry import CardEntry
from cb_agents.card_registry_helpers import load_metadata_helper

logger = logging.getLogger(__name__)


class CardRegistry:
    _instance = None

    def __new__(cls, skills_dir: str = "skills"):
        if not cls._instance:
            cls._instance = super(CardRegistry, cls).__new__(cls)
            cls._instance._initialize(skills_dir)
        elif cls._instance.skills_dir != Path(skills_dir):
            cls._instance._initialize(skills_dir)
        return cls._instance

    def _initialize(self, skills_dir: str):
        self.skills_dir = Path(skills_dir)
        self.cards: Dict[Any, CardEntry] = {}
        self.full_cards: Dict[Any, CardEntry] = {}
        self.evolution_predecessors: Dict[str, str] = {}
        self.card_hp: Dict[int, int] = {}
        self.card_retreat: Dict[int, int] = {}
        load_metadata_helper(self.skills_dir, self.cards, self.evolution_predecessors)
        
        self.move_damage = {}
        import csv
        try:
            pool_path = self.skills_dir / "card_pool_raw.csv"
            if pool_path.exists():
                with open(pool_path, "r", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    header = next(reader, None)
                    if header:
                        move_idx = -1
                        dmg_idx = -1
                        hp_idx = -1
                        retreat_idx = -1
                        id_idx = -1
                        for idx, col in enumerate(header):
                            low = col.strip().lower()
                            if "move name" in low:
                                move_idx = idx
                            elif "damage" in low:
                                dmg_idx = idx
                            elif low == "hp":
                                hp_idx = idx
                            elif "retreat" in low:
                                retreat_idx = idx
                            elif "card id" in low:
                                id_idx = idx
                        for row in reader:
                            if len(row) > max(move_idx, dmg_idx):
                                move = row[move_idx].strip()
                                dmg = row[dmg_idx].strip()
                                if move and move.lower() != "n/a":
                                    self.move_damage[move.lower()] = dmg
                            if id_idx != -1 and len(row) > id_idx:
                                try:
                                    cid = int(row[id_idx].strip())
                                    if hp_idx != -1 and len(row) > hp_idx and cid not in self.card_hp:
                                        hp_val = row[hp_idx].strip()
                                        if hp_val and hp_val.lower() not in ("n/a", ""):
                                            self.card_hp[cid] = int(hp_val)
                                    if retreat_idx != -1 and len(row) > retreat_idx and cid not in self.card_retreat:
                                        ret_val = row[retreat_idx].strip()
                                        if ret_val and ret_val.lower() not in ("n/a", ""):
                                            self.card_retreat[cid] = int(ret_val)
                                except (ValueError, IndexError):
                                    pass
        except Exception as e:
            logger.error(f"Failed to load card_pool_raw.csv moves: {e}")
        
        # Load learned rules from crawler
        self.learned_dos = set()
        self.learned_donts = set()
        import json
        try:
            dos_path = self.skills_dir / "learned_dos.json"
            if dos_path.exists():
                dos_data = json.loads(dos_path.read_text(encoding="utf-8"))
                for item in dos_data.get("deck_dos", []):
                    cid = item.get("card_id")
                    if cid is not None:
                        self.learned_dos.add(int(cid))
        except Exception as e:
            logger.error(f"Failed to load learned_dos.json: {e}")

        try:
            donts_path = self.skills_dir / "learned_donts.json"
            if donts_path.exists():
                donts_data = json.loads(donts_path.read_text(encoding="utf-8"))
                for item in donts_data.get("deck_donts", []):
                    cid = item.get("card_id")
                    if cid is not None:
                        self.learned_donts.add(int(cid))
        except Exception as e:
            logger.error(f"Failed to load learned_donts.json: {e}")

    def get(self, card_id: Any) -> Optional[CardEntry]:
        """Get lightweight metadata card entry."""
        return self.cards.get(card_id)

    def get_full_skill(self, card_id: Any) -> Optional[CardEntry]:
        """Lazy loads and returns the heavy full skill data for a card."""
        if card_id in self.full_cards:
            return self.full_cards[card_id]
            
        base = self.cards.get(card_id)
        if not base:
            return None
            
        from cb_agents.context import SharedContext
        ctx = SharedContext()
        heavy_data = ctx.get_config(str(self.skills_dir), "card_scoring.json")
        
        if not hasattr(self, "_heavy_cards_index"):
            self._heavy_cards_index = {str(c.get("card_id", "")): c for c in heavy_data.get("cards", [])}
            
        card_data = self._heavy_cards_index.get(str(base.card_id))
                
        if not card_data:
            self.full_cards[card_id] = base
            return base
            
        trainer_subtype = TrainerSubtype.NONE
        if base.card_type == CardType.TRAINER:
            raw_stage_type = card_data.get("stage_type", "").lower()
            for key, val in TRAINER_MAP.items():
                if key in raw_stage_type:
                    trainer_subtype = val
                    break

        combo_mask = ComboTag.NONE
        for tag in card_data.get("combo_tags", []):
            tag_enum = COMBO_TAG_MAP.get(tag)
            if tag_enum:
                combo_mask |= tag_enum

        hp = int(card_data.get("hp", self.card_hp.get(int(base.card_id), 100)))
        retreat_cost = int(card_data.get("retreat_cost", self.card_retreat.get(int(base.card_id), 1)))

        entry = CardEntry(
            card_id=base.card_id,
            card_name=base.card_name,
            card_type=base.card_type,
            stage=base.stage,
            trainer_subtype=trainer_subtype,
            combo_tags=combo_mask,
            ev_score=float(card_data.get("ev_score", 0.0)),
            damage_output=int(card_data.get("damage_output", 0)),
            energy_cost=int(card_data.get("energy_cost", 0)),
            utility_score=float(card_data.get("utility_score", 0.0)),
            archetype=card_data.get("archetype", ""),
            previous_stage=base.previous_stage,
            hp=hp,
            retreat_cost=retreat_cost,
            is_full=True
        )
        
        self.full_cards[base.card_id] = entry
        self.full_cards[str(base.card_id)] = entry
        return entry

    def get_evolution_predecessor(self, card_name: str) -> str:
        """Returns the name of the previous stage, or empty string."""
        return self.evolution_predecessors.get(card_name.lower(), "")
