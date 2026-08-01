
def fake_run():
    for i in range(3):
        yield {'file-{0}'.format(i): i ** 2}

