
def test_event_terminal_integer(n_events):
    f, event = _get_harmonic_oscillator()
    event.terminal = n_events
    res = solve_ivp(f, (0, 100), [1, 0], events=event)
    assert len(res.t_events[0]) == n_events
    assert len(res.y_events[0]) == n_events
    assert_allclose(res.y_events[0][:, 0], 0, atol=1e-14)

