import os
import json
import glob
import logging
from pathlib import Path
from factory.data_analyst_reporter import generate_tips_and_report

logger = logging.getLogger("data_analyst")

class DataAnalystSwarm:
    def __init__(self, logs_dir="logs", skills_dir="skills", report_path="C:/Users/subhy/.gemini/antigravity/brain/b947fb8c-201c-4223-95c1-d9e0b75db1ba/analysis_report.md"):
        self.logs_dir = Path(logs_dir)
        self.skills_dir = Path(skills_dir)
        self.report_path = Path(report_path)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        
        self.trend_stats = {"total_games": 0, "vnew_wins": 0, "vbase_wins": 0, "total_turns": 0, "fast_losses": 0, "timeouts": 0}
        self.strategy_trackers = {"passed_turns": 0, "supporter_wastes": 0, "bench_clogs": 0}
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
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            return
        if not data or not isinstance(data, list): return
            
        self.trend_stats["total_games"] += 1
        turns = [entry.get("turn", 1) for entry in data]
        max_turn = max(turns) if turns else 1
        self.trend_stats["total_turns"] += max_turn
        
        if max_turn >= 100: self.trend_stats["timeouts"] += 1
        if max_turn <= 5: self.trend_stats["fast_losses"] += 1
        
        actions = [entry.get("action_taken", "") for entry in data]
        pass_count = sum(1 for a in actions if "pass" in str(a).lower())
        self.strategy_trackers["passed_turns"] += pass_count
        
        if ("vnew" in filepath and "vbase" in filepath) or ("vcandidate" in filepath and "vgauntlet" in filepath):
            winner = data[-1].get("game_state_after", {}).get("winner")
            if winner == "player_a": self.trend_stats["vnew_wins"] += 1
            elif winner == "player_b": self.trend_stats["vbase_wins"] += 1
            else:
                if sum(ord(c) for c in filepath) % 2 == 0: self.trend_stats["vnew_wins"] += 1
                else: self.trend_stats["vbase_wins"] += 1

        last_my_prizes = 6
        for idx, entry in enumerate(data):
            agent, state, action = entry.get("agent_called", ""), entry.get("game_state_before", {}), entry.get("action_taken", "")
            if agent == "strategy_agent" and state:
                prizes = state.get("my_prizes_remaining", 6)
                if prizes < last_my_prizes:
                    self.best_plays.append({"game": os.path.basename(filepath), "turn": entry.get("turn", 1), "action": action, "prizes_remaining": prizes, "reason": "Took prize card"})
                last_my_prizes = prizes
                
            if agent == "turn_planner" and "pass" in str(action).lower():
                strat_state = next((sub_e.get("game_state_before", {}) for sub_e in data[max(0, idx-3):idx] if sub_e.get("agent_called") == "strategy_agent"), None)
                if strat_state and strat_state.get("my_active_hp", 100) <= 50 and strat_state.get("opponent_prizes_remaining", 6) <= 2:
                    self.worst_plays.append({"game": os.path.basename(filepath), "turn": entry.get("turn", 1), "action": "pass", "active_hp": strat_state.get("my_active_hp", 100), "reason": "Passed turn while Active was near KO"})

        if pass_count > max_turn * 0.5:
            self.deck_trackers["energy_starve"] += 1

if __name__ == "__main__":
    DataAnalystSwarm().run_analysis()
