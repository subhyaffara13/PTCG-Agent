
def _impl_test_interactive_timers():
    # A timer with <1 millisecond gets converted to int and therefore 0
    # milliseconds, which the mac framework interprets as singleshot.
    # We only want singleshot if we specify that ourselves, otherwise we want
    # a repeating timer
    from unittest.mock import Mock
    import matplotlib.pyplot as plt
    pause_time = 0.5
    fig = plt.figure()
    plt.pause(pause_time)
    timer = fig.canvas.new_timer(0.1)
    mock = Mock()
    timer.add_callback(mock)
    timer.start()
    plt.pause(pause_time)
    timer.stop()
    assert mock.call_count > 1

    # Now turn it into a single shot timer and verify only one gets triggered
    mock.reset_mock()
    timer.single_shot = True
    timer.start()
    plt.pause(pause_time)
    assert mock.call_count == 1

    # Make sure we can start the timer a second time
    timer.start()
    plt.pause(pause_time)
    assert mock.call_count == 2
    plt.close("all")

