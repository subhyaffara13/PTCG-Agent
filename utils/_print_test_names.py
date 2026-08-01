
def _print_test_names():
    suite = unittest.TestLoader().loadTestsFromModule(__main__)
    test_cases = discover_test_cases_recursively(suite)
    for name in get_test_names(test_cases):
        print(name)

