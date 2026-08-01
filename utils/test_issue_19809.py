
def test_issue_19809():

    def f():
        assert _dotprodsimp_state.state == None
        m = Matrix([[1]])
        m = m * m
        return True

    with dotprodsimp(True):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(f)
            assert future.result()


def test_issue_19809():

    def f():
        assert _dotprodsimp_state.state == None
        m = Matrix([[1]])
        m = m * m
        return True

    with dotprodsimp(True):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(f)
            assert future.result()

