
def _log_atan_table():
    return {
        # first quadrant only
        sqrt(3): pi / 3,
        1: pi / 4,
        sqrt(5 - 2 * sqrt(5)): pi / 5,
        sqrt(2) * sqrt(5 - sqrt(5)) / (1 + sqrt(5)): pi / 5,
        sqrt(5 + 2 * sqrt(5)): pi * Rational(2, 5),
        sqrt(2) * sqrt(sqrt(5) + 5) / (-1 + sqrt(5)): pi * Rational(2, 5),
        sqrt(3) / 3: pi / 6,
        sqrt(2) - 1: pi / 8,
        sqrt(2 - sqrt(2)) / sqrt(sqrt(2) + 2): pi / 8,
        sqrt(2) + 1: pi * Rational(3, 8),
        sqrt(sqrt(2) + 2) / sqrt(2 - sqrt(2)): pi * Rational(3, 8),
        sqrt(1 - 2 * sqrt(5) / 5): pi / 10,
        (-sqrt(2) + sqrt(10)) / (2 * sqrt(sqrt(5) + 5)): pi / 10,
        sqrt(1 + 2 * sqrt(5) / 5): pi * Rational(3, 10),
        (sqrt(2) + sqrt(10)) / (2 * sqrt(5 - sqrt(5))): pi * Rational(3, 10),
        2 - sqrt(3): pi / 12,
        (-1 + sqrt(3)) / (1 + sqrt(3)): pi / 12,
        2 + sqrt(3): pi * Rational(5, 12),
        (1 + sqrt(3)) / (-1 + sqrt(3)): pi * Rational(5, 12)
    }

