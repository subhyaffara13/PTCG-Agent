
def test_async_callbacks():
    # serves as state for async callback
    class Item:
        def __init__(self, value):
            self.value = value

    res = []

    # generate stateful lambda that will store result in `res`
    def gen_f():
        s = Item(3)
        return lambda j: res.append(s.value + j)

    # do some work async
    work = [1, 2, 3, 4]
    m.test_async_callback(gen_f(), work)
    # wait until work is done
    from time import sleep

    sleep(0.5)
    assert sum(res) == sum(x + 3 for x in work)

