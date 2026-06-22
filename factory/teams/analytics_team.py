import concurrent.futures
import logging
from factory.data_analyst import DataAnalystSwarm
from factory.anti_pattern_extractor import AntiPatternExtractor
from factory.degradation_tracker import DegradationTracker

logger = logging.getLogger("AnalyticsTeam")

class AnalyticsTeam:
    def __init__(self):
        self.data_analyst = DataAnalystSwarm()
        self.anti_pattern_extractor = AntiPatternExtractor()
        self.degradation_tracker = DegradationTracker()

    def run_analysis(self, iteration_id: int = 0, log_dir: str = "logs",
                     iteration_result: dict = None, decks: dict = None):
        """Runs the entire analytics pipeline in parallel threads."""
        logger.info("Analytics Team starting parallel analysis...")
        results = {}

        if iteration_result is None:
            iteration_result = {}
        if decks is None:
            decks = {}

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_macro = executor.submit(self.data_analyst.run_analysis, iteration_id)
            future_anti = executor.submit(self.anti_pattern_extractor.analyze_iteration, iteration_result, {}, decks)
            future_deg = executor.submit(self.degradation_tracker.evaluate_health)
            
            try:
                results["macro_analysis"] = future_macro.result()
                future_anti.result()
                results["degradation"] = future_deg.result()
            except Exception as e:
                logger.error(f"Analytics Team encountered an error during parallel execution: {e}")
                
        logger.info("Analytics Team finished parallel analysis.")
        return results

    def run_kaggle_analysis(self, submission_id: int) -> dict:
        """Fetches and analyzes replays from Kaggle to extract anti-patterns."""
        logger.info(f"Analytics Team fetching Kaggle submission {submission_id}...")
        from factory.kaggle_scraper import KaggleScraper
        scraper = KaggleScraper()
        
        episode_ids = scraper.get_submission_episodes(submission_id)
        if not episode_ids:
            logger.warning("No episodes found or failed to fetch episodes from Kaggle.")
            return {}
            
        # Download and parse the latest 5 episodes
        latest_episodes = episode_ids[:5]
        parsed_replays = []
        for ep_id in latest_episodes:
            replay_path = scraper.download_episode_replay(ep_id)
            if replay_path:
                history = scraper.parse_replay_to_history(replay_path)
                parsed_replays.extend(history)
                
        # Analyze the loaded episodes for deck and behavioral faults
        # In a full meta-learning setup, we would run AntiPatternExtractor or update heuristics
        # based on where our agent lost (e.g. tracking turn counts, prizes, etc.)
        logger.info(f"Kaggle Replay analysis complete. Analyzed {len(latest_episodes)} episodes.")
        return {
            "analyzed_episodes": latest_episodes, 
            "log_events_count": len(parsed_replays)
        }
