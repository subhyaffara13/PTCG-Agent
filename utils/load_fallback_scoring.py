
def load_fallback_scoring(skills_dir: Path, cards: Dict[Any, Any]):
    scoring_path = skills_dir / "card_scoring.json"
    if scoring_path.exists():
        try:
            data = json.loads(scoring_path.read_text(encoding="utf-8"))
            for c in data.get("cards", []):
                cid_str = str(c.get("card_id", ""))
                if not cid_str:
                    continue
                try:
                    cid_int = int(cid_str)
                except ValueError:
                    continue
                name = c.get("card_name", "")
                c_type_str = c.get("card_type", "").lower()
                c_type = CARD_TYPE_MAP.get(c_type_str, CardType.UNKNOWN)
                stage_type_str = c.get("stage_type", "").lower()
                stage = CardStage.NONE
                if "basic" in stage_type_str:
                    stage = CardStage.BASIC
                elif "stage 1" in stage_type_str:
                    stage = CardStage.STAGE1
                elif "stage 2" in stage_type_str:
                    stage = CardStage.STAGE2

                from cb_agents.card_entry import CardEntry
                entry = CardEntry(
                    card_id=cid_int,
                    card_name=name,
                    card_type=c_type,
                    stage=stage
                )
                cards[cid_int] = entry
                cards[cid_str] = entry
        except Exception as e:
            logger.error(f"Failed parsing fallback card_scoring: {e}")


def load_fallback_scoring(skills_dir: Path, cards: Dict[Any, Any]):
    scoring_path = skills_dir / "card_scoring.json"
    if scoring_path.exists():
        try:
            data = json.loads(scoring_path.read_text(encoding="utf-8"))
            for c in data.get("cards", []):
                cid_str = str(c.get("card_id", ""))
                if not cid_str:
                    continue
                try:
                    cid_int = int(cid_str)
                except ValueError:
                    continue
                name = c.get("card_name", "")
                c_type_str = c.get("card_type", "").lower()
                c_type = CARD_TYPE_MAP.get(c_type_str, CardType.UNKNOWN)
                stage_type_str = c.get("stage_type", "").lower()
                stage = CardStage.NONE
                if "basic" in stage_type_str:
                    stage = CardStage.BASIC
                elif "stage 1" in stage_type_str:
                    stage = CardStage.STAGE1
                elif "stage 2" in stage_type_str:
                    stage = CardStage.STAGE2

                from cb_agents.card_entry import CardEntry
                entry = CardEntry(
                    card_id=cid_int,
                    card_name=name,
                    card_type=c_type,
                    stage=stage
                )
                cards[cid_int] = entry
                cards[cid_str] = entry
        except Exception as e:
            logger.error(f"Failed parsing fallback card_scoring: {e}")

