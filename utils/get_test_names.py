
def get_test_names(test_cases):
    return ['.'.join(case.id().split('.')[-2:]) for case in test_cases]

