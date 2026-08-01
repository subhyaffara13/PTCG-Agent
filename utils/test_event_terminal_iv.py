
def test_event_terminal_iv():
    f, event = _get_harmonic_oscillator()
    args = (f, (0, 100), [1, 0])

    event.terminal = None
    res = solve_ivp(*args, events=event)
    event.terminal = 0
    ref = solve_ivp(*args, events=event)
    assert_allclose(res.t_events, ref.t_events)

    message = "The `terminal` attribute..."
    event.terminal = -1
    with pytest.raises(ValueError, match=message):
        solve_ivp(*args, events=event)
    event.terminal = 3.5
    with pytest.raises(ValueError, match=message):
        solve_ivp(*args, events=event)

