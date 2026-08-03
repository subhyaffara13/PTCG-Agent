import random

def test_wikipedia_counterexample():
    # The Levinson-Durbin implementation also fails in other cases.
    # This example is from the talk page of the wikipedia article.
    random = np.random.RandomState(1234)
    c = [2, 2, 1]
    y = random.randn(3)
    assert_raises(np.linalg.LinAlgError, solve_toeplitz, c, b=y)

