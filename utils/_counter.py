
def _counter():
    # Used internally to generate unique dummy symbols
    counter = 0
    while True:
        counter += 1
        yield counter

