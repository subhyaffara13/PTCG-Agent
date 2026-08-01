
def get_test_results(raw_return):
    test_results = TEST_RESULTS_RE.search(raw_return)
    if test_results:
        try:
            return eval(test_results.group(1))
        except:
            print(f"BUGGY TEST RESULTS EVAL:\n {test_results.group(1)}")
            raise

