import json
import csv
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, Optional
from agents.card_types import (
    CardType, CardStage, TrainerSubtype, ComboTag, 
    CARD_TYPE_MAP, STAGE_MAP, TRAINER_MAP, COMBO_TAG_MAP
)

logger = logging.getLogger(__name__)

@dataclass(frozen=True)
class CardEntry:
    card_id: int
    card_name: str
    card_type: CardType
    stage: CardStage
    trainer_subtype: TrainerSubtype
    combo_tags: ComboTag
    ev_score: float
    damage_output: int
    energy_cost: int
    utility_score: float
    archetype: str
    previous_stage: str = ""

class CardRegistry:
    _instance = None

    def __new__(cls, skills_dir: str = "skills"):
        if not cls._instance:
            cls._instance = super(CardRegistry, cls).__new__(cls)
            cls._instance._initialize(skills_dir)
        return cls._instance

    def _initialize(self, skills_dir: str):
        self.skills_dir = Path(skills_dir)
        self.cards: Dict[Any, CardEntry] = {}
        self.evolution_predecessors: Dict[str, str] = {}
        self._load_data()

    def _load_data(self):
        # 1. Parse raw CSV for evolution chains and stage types
        raw_data = {}
        csv_path = self.skills_dir / "card_pool_raw.csv"
        if csv_path.exists():
            try:
                with open(csv_path, mode="r", encoding="utf-8") as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        name = row.get("card_name", "").strip()
                        raw_data[name] = {
                            "stage_type": row.get("Stage/Type", "").strip().lower(),
                            "previous_stage": row.get("previous_stage", "").strip()
                        }
                        prev = row.get("previous_stage", "").strip().lower()
                        if name and prev and prev != "none":
                            self.evolution_predecessors[name.lower()] = prev
            except Exception as e:
                logger.error(f"Failed to parse card_pool_raw.csv: {e}")

        # 2. Parse scoring JSON
        json_path = self.skills_dir / "card_scoring.json"
        if json_path.exists():
            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
                for c in data.get("cards", []):
                    card_id_str = str(c.get("card_id", ""))
                    if not card_id_str:
                        continue
                        
                    try:
                        card_id_int = int(card_id_str)
                    except ValueError:
                        continue
                        
                    name = c.get("card_name", "").strip()
                    c_type_str = c.get("card_type", "").lower()
                    c_type = CARD_TYPE_MAP.get(c_type_str, CardType.UNKNOWN)
                    
                    # Merge with raw data
                    raw = raw_data.get(name, {})
                    stage_type_str = raw.get("stage_type", "")
                    
                    # Parse stage
                    stage = CardStage.NONE
                    if "basic" in stage_type_str:
                        stage = CardStage.BASIC
                    elif "stage 1" in stage_type_str:
                        stage = CardStage.STAGE1
                    elif "stage 2" in stage_type_str:
                        stage = CardStage.STAGE2
                        
                    # Parse trainer subtype
                    trainer_subtype = TrainerSubtype.NONE
                    if c_type == CardType.TRAINER:
                        for key, val in TRAINER_MAP.items():
                            if key in stage_type_str:
                                trainer_subtype = val
                                break

                    # Parse combo tags
                    combo_mask = ComboTag.NONE
                    for tag in c.get("combo_tags", []):
                        tag_enum = COMBO_TAG_MAP.get(tag)
                        if tag_enum:
                            combo_mask |= tag_enum

                    entry = CardEntry(
                        card_id=card_id_int,
                        card_name=name,
                        card_type=c_type,
                        stage=stage,
                        trainer_subtype=trainer_subtype,
                        combo_tags=combo_mask,
                        ev_score=float(c.get("ev_score", 0.0)),
                        damage_output=int(c.get("damage_output", 0)),
                        energy_cost=int(c.get("energy_cost", 0)),
                        utility_score=float(c.get("utility_score", 0.0)),
                        archetype=c.get("archetype", ""),
                        previous_stage=raw.get("previous_stage", "")
                    )
                    
                    # Map both integer and string IDs to the same entry
                    self.cards[card_id_int] = entry
                    self.cards[card_id_str] = entry
                    
                logger.info(f"CardRegistry loaded {len(self.cards)//2} unique cards")
            except Exception as e:
                logger.error(f"Failed to parse card_scoring.json: {e}")

    def get(self, card_id: Any) -> Optional[CardEntry]:
        """Get card entry by integer or string ID."""
        return self.cards.get(card_id)

    def get_evolution_predecessor(self, card_name: str) -> str:
        """Returns the name of the previous stage, or empty string."""
        return self.evolution_predecessors.get(card_name.lower(), "")
