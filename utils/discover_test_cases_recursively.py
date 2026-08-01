
def discover_test_cases_recursively(suite_or_case):
    if isinstance(suite_or_case, unittest.TestCase):
        return [suite_or_case]
    rc = []
    for element in suite_or_case:
        print(element)
        rc.extend(discover_test_cases_recursively(element))
    return rc

