
def generate_compose_test_cases():
    """
    Generate test cases for parametrized tests of the compose function.
    """

    def add_then_multiply(a, b, c=10):
        return (a + b) * c

    return (
        (
            (),        # arguments to compose()
            (0,), {},  # positional and keyword args to the Composed object
            0          # expected result
        ),
        (
            (inc,),
            (0,), {},
            1
        ),
        (
            (double, inc),
            (0,), {},
            2
        ),
        (
            (str, iseven, inc, double),
            (3,), {},
            "False"
        ),
        (
            (str, add),
            (1, 2), {},
            '3'
        ),
        (
            (str, inc, add_then_multiply),
            (1, 2), {"c": 3},
            '10'
        ),
    )

