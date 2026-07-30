"""
factory/orchestration_agent_helpers.py
Helpers for the orchestration agent: auto-submission, analytics, script config.
"""
import sys
import json
import subprocess
import logging
from pathlib import Path
from factory.orchestration_agent_utils import get_training_scripts, read_fitness
logger = logging.getLogger("orchestration_agent")

from .run_analytics_check import run_analytics_check
from .auto_submit_if_ready import auto_submit_if_ready
