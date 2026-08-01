
def _generate_test_points(typecodes):
    axes = tuple(TEST_POINTS[x] for x in typecodes)
    pts = list(product(*axes))
    return pts

