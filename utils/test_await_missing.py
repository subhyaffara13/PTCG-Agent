
def test_await_missing(event_loop):
    with pytest.raises(TypeError):
        event_loop.run_until_complete(get_await_result(m.DoesNotSupportAsync()))

