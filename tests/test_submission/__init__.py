"""
tests/test_submission.py

Unit tests for submission/main.py.
"""
import os
import json
import pytest
import sys
from pathlib import Path
submission_dir = str(Path(__file__).parent.parent / "submission")
if submission_dir not in sys.path:
    sys.path.insert(0, submission_dir)
from main import agent

from .mockobservation_mockselectoption_mockselect import MockObservation
from .mockobservation_mockselectoption_mockselect import MockSelectOption
from .mockobservation_mockselectoption_mockselect import MockSelect
from .mockobservation_mockselectoption_mockselect import MockCard
from .mockobservation_mockselectoption_mockselect import MockPlayerState
from .mockobservation_mockselectoption_mockselect import MockCurrentState
from .realisticmockobservation_test_submission_agent_legacy_mock_f import RealisticMockObservation
from .realisticmockobservation_test_submission_agent_legacy_mock_f import test_submission_agent_legacy_mock_fallback
from .realisticmockobservation_test_submission_agent_legacy_mock_f import test_realistic_submission_agent_orchestration
from .realisticmockobservation_test_submission_agent_legacy_mock_f import test_submission_py_compatibility
