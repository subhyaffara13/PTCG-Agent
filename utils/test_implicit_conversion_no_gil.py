
def test_implicit_conversion_no_gil():
    a = Thread(m.test_no_gil)
    b = Thread(m.test_no_gil)
    c = Thread(m.test_no_gil)
    for x in [a, b, c]:
        x.start()
    for x in [c, b, a]:
        x.join()

