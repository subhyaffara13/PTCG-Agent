"""
tests/test_shared_context.py

Unit tests for cb_agents/context.py (SharedContext singleton cache manager).
"""

import json
from pathlib import Path
from cb_agents.context import SharedContext
from cb_agents.orchestrator import Orchestrator

from utils.test_shared_context_singleton import test_shared_context_singleton

from utils.test_orchestrator_context_injection import test_orchestrator_context_injection
