from . import Path, agent
from .mockobservation_mockselectoption_mockselect import MockCurrentState, MockObservation, MockSelect

class RealisticMockObservation:
    def __init__(self):
        self.select = MockSelect()
        self.current = MockCurrentState()
        self.legal_actions = ["pass", "attack:Thunderbolt"]

def test_submission_agent_legacy_mock_fallback():
    # When select is None, it should hit the legacy fallback and return the first legal action
    obs = MockObservation()
    action = agent(obs)
    assert action[0] in obs.legal_actions

def test_realistic_submission_agent_orchestration():
    # When select is a real turn choice, it should run orchestrator and return selected option indices
    obs = RealisticMockObservation()
    action = agent(obs)
    
    # Assert return value is a list of indices representing the selected option(s)
    assert isinstance(action, list)
    for idx in action:
        assert 0 <= idx < len(obs.select.option)

def test_submission_py_compatibility():
    # Verify that all Python files inside the submission/ directory are Python 3.11 compatible (no PEP 701 nested quotes in f-strings)
    sub_dir = Path(__file__).parent.parent / "submission"
    if sub_dir.exists():
        import ast
        for py_file in sub_dir.rglob("*.py"):
            content = py_file.read_text(encoding="utf-8")
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, ast.JoinedStr):
                    for val in node.values:
                        if isinstance(val, ast.FormattedValue):
                            expr_str = ast.unparse(val.value)
                            assert "'" not in expr_str and '"' not in expr_str, f"PEP 701 f-string compatibility error in {py_file.name}: f-string expression contains quotes: {{{expr_str}}}"

