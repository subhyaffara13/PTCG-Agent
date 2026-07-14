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
                     iteration_result: dict | None = None, decks: dict | None = None):
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
        """Fetches and analyzes replays from Kaggle to extract anti-patterns and run self-healing."""
        import json
        import os
        import re
        from pathlib import Path
        from kaggle.api.kaggle_api_extended import KaggleApi
        from factory.kaggle_scraper import KaggleScraper
        
        logger.info(f"Analytics Team fetching Kaggle submission {submission_id}...")
        try:
            api = KaggleApi()
            api.authenticate()
        except Exception as e:
            logger.error(f"Kaggle authentication failed for Analytics Team: {e}")
            return {}

        # 1. Fetch episodes
        try:
            episodes = api.competition_list_episodes(submission_id)
        except Exception as e:
            logger.error(f"Failed to fetch episodes for submission {submission_id}: {e}")
            return {}

        if not episodes:
            logger.warning("No episodes found for the submission.")
            return {}

        logger.info(f"Found {len(episodes)} episodes. Checking for crashes or losses...")
        
        # 2. Identify losses or errors
        losses = []
        for ep in episodes:
            agents = getattr(ep, 'agents', [])
            ep_id = getattr(ep, 'id', None)
            if not ep_id:
                continue
            for agent in agents:
                reward = getattr(agent, 'reward', 0)
                status = getattr(agent, 'status', '')
                team_id = str(getattr(agent, 'team_id', getattr(agent, 'teamId', '')))
                if reward < 0 or status in ['ERROR', 'TIMEOUT']:
                    losses.append((ep_id, team_id, status))

        if not losses:
            logger.info("No losses or errors found in the episodes!")
            return {"status": "all_wins_or_draws"}

        logger.info(f"Found {len(losses)} losses/errors. Downloading and auditing the latest 3 losses...")
        scraper = KaggleScraper(output_dir="logs/kaggle_replays")
        
        analyzed_episodes = []
        for ep_id, team_id, status in losses[:3]:
            replay_path = scraper.download_episode_replay(ep_id)
            if not (replay_path and replay_path.exists()):
                continue
            
            analyzed_episodes.append(ep_id)
            try:
                with open(replay_path, "r", encoding="utf-8") as f:
                    replay = json.load(f)
                steps = replay.get("steps", [])
                
                # Identify which player index we were
                info = replay.get("info", {})
                team_names = info.get("TeamNames", ["", ""])
                player_idx = -1
                for idx, name in enumerate(team_names):
                    if str(team_id) in name or any(part in name.lower() for part in ["subhy", "antigravity", "apex"]):
                        player_idx = idx
                        break

                if player_idx == -1:
                    # Fallback check
                    for idx, p_state in enumerate(steps[1] if len(steps) > 1 else []):
                        obs_dict = p_state.get("observation") or {}
                        current = obs_dict.get("current") or {}
                        players = current.get("players", [])
                        if idx < len(players) and str(players[idx].get("teamId")) == str(team_id):
                            player_idx = idx
                            break

                if player_idx == -1:
                    logger.warning(f"Could not identify our player index in episode {ep_id}.")
                    continue

                # Parse the error or traceback
                stderr_content = ""
                for step in steps:
                    if len(step) > player_idx:
                        stderr = step[player_idx].get("stderr", "")
                        if stderr:
                            stderr_content += stderr + "\n"

                # Analyze failure reasons
                target_file = "cb_agents/turn_planner_sort.py"
                reason_desc = f"Loss in episode {ep_id} with status {status}."
                
                if "Traceback" in stderr_content:
                    reason_desc += f"\nPython crash detected! Traceback log:\n{stderr_content}"
                    matches = re.findall(r'File "([^"]+\.py)"', stderr_content)
                    if matches:
                        for match in matches:
                            if "cb_agents/" in match:
                                target_file = match
                                break

                # Run AntiPatternExtractor on the replay to log the flaw for the DevelopmentTeam
                self.anti_pattern_extractor.analyze_losing_replays([replay_path], team_id)
                logger.info(f"[SECO] Extracted anti-patterns and logged flaws for episode {ep_id}. DevelopmentTeam will handle healing.")

            except Exception as e:
                logger.error(f"Error analyzing episode {ep_id}: {e}")

        logger.info(f"Kaggle Replay analysis and self-healing complete. Analyzed: {analyzed_episodes}")
        return {"analyzed_episodes": analyzed_episodes}
