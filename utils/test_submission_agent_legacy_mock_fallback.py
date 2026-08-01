
def test_submission_agent_legacy_mock_fallback():
    # When select is None, it should hit the legacy fallback and return the first legal action
    obs = MockObservation()
    action = agent(obs)
    assert action[0] in obs.legal_actions

