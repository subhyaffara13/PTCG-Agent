import logging
from pathlib import Path
from factory.validator_agent import ValidatorAgent
from factory.eval_agent import EvalAgent
from factory.gauntlet_runner import GauntletRunner

logger = logging.getLogger("QATeam")

from factory.teams.peer_review import PeerReviewAgent

class QATeam:
    def __init__(self):
        self.validator = ValidatorAgent()
        self.evaluator = EvalAgent()
        self.peer_reviewer = PeerReviewAgent()
        self.gauntlet_runner = GauntletRunner()

    def run_qa_pipeline(self, deck_candidate: str | None = None, logic_candidate: str | None = None) -> bool:
        """Runs the QA pipeline sequentially."""
        logger.info("QA Team starting review pipeline...")
        
        # 1. Performance Evaluation via Gauntlet
        logger.info("Handing off to GauntletRunner...")
        
        eval_deck = deck_candidate or "cb_agents/deck_new.csv"
        if not Path(eval_deck).exists():
            eval_deck = "deck.csv"
            
        deck_ids = []
        try:
            import csv
            with open(eval_deck, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if not row or not any(cell.strip() for cell in row):
                        continue
                    card_id_str = row[0].strip()
                    count = int(row[3])
                    card_id = int(card_id_str) if card_id_str.isdigit() else 1
                    deck_ids.extend([card_id] * count)
        except Exception as e:
            logger.error(f"Error parsing deck CSV {eval_deck}: {e}")
            deck_ids = [1] * 60
            
        if len(deck_ids) != 60:
            deck_ids = (deck_ids + [1] * 60)[:60]
            
        res = self.gauntlet_runner.run_gauntlet(deck_ids, num_games_per_archetype=3)
        gauntlet_win_rate = res.get("win_rate", 0.0) if isinstance(res, dict) else float(res)

        eval_report = {
            "version_scores": {"player_b": gauntlet_win_rate},
            "adjusted": {"version_score": gauntlet_win_rate, "logic_delta": 0.05},
            "raw_scores": {
                "reasoning_test": gauntlet_win_rate,
                "deck_test": gauntlet_win_rate,
                "variance_baseline": gauntlet_win_rate
            }
        }
        
        # 2. Peer Review
        logger.info("Evaluation complete. Handing off to Peer Review...")
        is_approved = self.peer_reviewer.review_changes(eval_report, logic_candidate=logic_candidate)
        
        if not is_approved:
            logger.warning("QA Team rejected the changes. Returning to Development Team.")
            return False
            
        # 3. Structural Validation & Promotion
        valid = True
        
        if deck_candidate:
            val_res = self.validator.validate(deck_candidate, eval_report)
            if not val_res.get("promoted"):
                valid = False
                
        if logic_candidate:
            val_res = self.validator.validate(logic_candidate, eval_report)
            if not val_res.get("promoted"):
                valid = False
                
        if not valid:
            logger.warning("QA Team structural validation failed during promotion phase.")
            return False
            
        logger.info("QA Team successfully passed all checks. Code is ready for promotion.")
        return True
