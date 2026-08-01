import os
import json
import shutil
from pathlib import Path
from cb_agents.hand_analyst import HandAnalyst
from cb_agents.strategy_agent import StrategyAgent
from router.bus import HandAnalystPacket, StrategyPacket
from cb_agents.context import SharedContext

from utils.run_empirical_verification import run_empirical_verification

if __name__ == "__main__":
    run_empirical_verification()
