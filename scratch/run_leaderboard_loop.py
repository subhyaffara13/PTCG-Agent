"""
scratch/run_leaderboard_loop.py

A script to manually trigger the leaderboard analysis, scraper,
and policy update feedback loops.
"""

import sys
import os
from dotenv import load_dotenv
load_dotenv()

cwd = os.getcwd()
if cwd not in sys.path:
    sys.path.insert(0, cwd)

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("RunLeaderboardLoop")

from factory.teams.leaderboard_team import LeaderboardTeam

def main():
    logger.info("Starting leaderboard team execution...")
    # Initialize LeaderboardTeam
    team = LeaderboardTeam()
    
    # Run the feedback loop
    results = team.run_leaderboard_feedback_loop()
    
    logger.info(f"Leaderboard feedback loop execution complete. Results: {results}")

if __name__ == "__main__":
    main()
