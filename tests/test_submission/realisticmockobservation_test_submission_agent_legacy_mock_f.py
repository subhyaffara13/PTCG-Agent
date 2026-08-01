from . import Path, agent
from .mockobservation_mockselectoption_mockselect import MockCurrentState, MockObservation, MockSelect

class RealisticMockObservation:
    def __init__(self):
        self.select = MockSelect()
        self.current = MockCurrentState()
        self.legal_actions = ["pass", "attack:Thunderbolt"]

from utils.test_submission_agent_legacy_mock_fallback import test_submission_agent_legacy_mock_fallback

from utils.test_realistic_submission_agent_orchestration import test_realistic_submission_agent_orchestration

from utils.test_submission_py_compatibility import test_submission_py_compatibility

