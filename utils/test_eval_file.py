import os

def test_eval_file():
    filename = os.path.join(os.path.dirname(__file__), "test_eval_call.py")
    assert m.test_eval_file(filename)

    assert m.test_eval_file_failure()

