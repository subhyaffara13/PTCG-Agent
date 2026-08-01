
def _test_function(fn, device):
    def run_test_function(self):
        return fn(self, device)
    return run_test_function

