
def require_optuna(test_case):
    """
    Decorator marking a test that requires optuna.

    These tests are skipped when optuna isn't installed.

    """
    return unittest.skipUnless(is_optuna_available(), "test requires optuna")(test_case)

