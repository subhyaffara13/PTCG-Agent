import json
import logging
from pathlib import Path
from collections import Counter
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

from factory.do_pattern_logger import load_dos, save_dos, run_winning_analysis

class DoPatternExtractor:
    """
    Extracts positive behavioral and deck-building patterns from winning tournament/leaderboard games.
    
    This acts as a meta-learning guide. By analyzing top-performing player matches, it extracts
    recommended deck inclusions ("do's") and behavioral targets, saving them to a JSON configuration
    which is then utilized by DeckArchitect to refine deck creation.
    """
    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        self.dos_file = self.skills_dir / "learned_dos.json"
        self.learned_dos = load_dos(self.dos_file)

    def _save_dos(self):
        save_dos(self.dos_file, self.learned_dos)

    def analyze_winning_replays(self, replay_paths: List[Path], player_name_or_id: str):
        """
        Analyzes a list of winning replay JSON files for a specific player/team
        to extract recommended cards and behavior patterns.
        """
        run_winning_analysis(replay_paths, player_name_or_id, self)

