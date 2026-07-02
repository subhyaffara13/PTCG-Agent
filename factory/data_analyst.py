import os
import json
import glob
import logging
from pathlib import Path
from factory.data_analyst_reporter import generate_tips_and_report
from factory.data_analyst_helpers import analyze_log_file

logger = logging.getLogger("data_analyst")

class DataAnalystSwarm:
    def __init__(self, logs_dir="logs", skills_dir="skills", report_path="C:/Users/subhy/.gemini/antigravity/brain/b947fb8c-201c-4223-95c1-d9e0b75db1ba/analysis_report.md"):
        self.logs_dir = Path(logs_dir)
        self.skills_dir = Path(skills_dir)
        self.report_path = Path(report_path)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.trend_stats = {"total_games": 0, "vnew_wins": 0, "vbase_wins": 0, "total_turns": 0, "fast_losses": 0, "timeouts": 0}
        self.strategy_trackers = {"passed_turns": 0, "supporter_wastes": 0, "bench_clogs": 0, "stadium_wastes": 0, "tool_efficiency": 0}
        self.deck_trackers = {"energy_starve": 0, "basic_drought": 0}
        self.best_plays = []
        self.worst_plays = []

    def run_analysis(self, iteration_id: int = 0):
        logger.info(f"Starting Data Analyst Swarm over {self.logs_dir}")
        log_files = glob.glob(str(self.logs_dir / "action_game_*.json"))
        log_files.sort(key=os.path.getmtime)
        if iteration_id == 0 or iteration_id % 100 != 0:
            log_files = log_files[-300:]
            
        for filepath in log_files:
            self._analyze_file(filepath)
            
        logger.info("Parsing complete. Delegating to reporter.")
        generate_tips_and_report(
            self.logs_dir, self.skills_dir, self.report_path,
            self.trend_stats, self.strategy_trackers, self.deck_trackers,
            self.best_plays, self.worst_plays
        )

    def _analyze_file(self, filepath):
        analyze_log_file(filepath, self.trend_stats, self.strategy_trackers, self.deck_trackers, self.best_plays, self.worst_plays)

if __name__ == "__main__":
    DataAnalystSwarm().run_analysis()
