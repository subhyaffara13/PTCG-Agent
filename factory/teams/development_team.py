import concurrent.futures
import logging
from factory.deck_architect import DeckArchitect
from factory.builder_agent import BuilderAgent
from factory.improvement_agent import ImprovementAgent

logger = logging.getLogger("DevelopmentTeam")

class DevelopmentTeam:
    def __init__(self):
        self.deck_architect = DeckArchitect()
        self.builder_agent = BuilderAgent()
        self.improvement_agent = ImprovementAgent()

    def run_development(self, analytics_report: dict):
        """Runs the development cycle in parallel based on analytics feedback."""
        logger.info("Development Team starting parallel development...")
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # Improvement Agent analyzes what to fix
            # Since analytics_report replaces eval_report conceptually here, we pass it.
            # Real pipeline might adapt improvement_notes here.
            future_improve = executor.submit(self.improvement_agent.improve, analytics_report)
            improvements = future_improve.result() if hasattr(future_improve, "result") else {}
            
            # Devs work in parallel based on improvements
            # Assuming these methods take improvement notes/flaws dictionary
            future_deck = executor.submit(self.deck_architect.build, improvements)
            future_logic = executor.submit(self.builder_agent.build, improvements)
            
            try:
                results["deck_candidate"] = future_deck.result()
                results["logic_candidate"] = future_logic.result()
            except Exception as e:
                logger.error(f"Development Team encountered an error during parallel execution: {e}")
                
        logger.info("Development Team finished parallel development.")
        return results

    def run_kaggle_development(self, kaggle_report: dict):
        """Drives the dev loop using Kaggle analytics feedback instead of local simulations."""
        logger.info("Development Team starting dev cycle from Kaggle reports...")
        # Incorporate Kaggle report metrics (timeouts, win rates, etc.) into the improvements logic
        # For example, if Kaggle report shows many losses to stall decks, focus on stall counters!
        improvements = self.improvement_agent.improve(kaggle_report)
        results = {}
        
        # Parallel candidate generations
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_deck = executor.submit(self.deck_architect.build, improvements)
            future_logic = executor.submit(self.builder_agent.build, improvements)
            
            try:
                results["deck_candidate"] = future_deck.result()
                results["logic_candidate"] = future_logic.result()
            except Exception as e:
                logger.error(f"Development Team encountered an error during Kaggle optimization: {e}")
        return results
