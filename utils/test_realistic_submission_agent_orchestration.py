
def test_realistic_submission_agent_orchestration():
    # When select is a real turn choice, it should run orchestrator and return selected option indices
    obs = RealisticMockObservation()
    action = agent(obs)
    
    # Assert return value is a list of indices representing the selected option(s)
    assert isinstance(action, list)
    for idx in action:
        assert 0 <= idx < len(obs.select.option)

