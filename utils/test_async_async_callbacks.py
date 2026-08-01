
def test_async_async_callbacks():
    t = Thread(target=test_async_callbacks)
    t.start()
    t.join()

