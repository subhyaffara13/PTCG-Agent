
def test_await(event_loop):
    assert event_loop.run_until_complete(get_await_result(m.SupportsAsync())) == 5

