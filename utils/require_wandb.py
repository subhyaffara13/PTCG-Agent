
def require_wandb(test_case):
    """
    Decorator marking a test that requires wandb.

    These tests are skipped when wandb isn't installed.

    """
    return unittest.skipUnless(is_wandb_available(), "test requires wandb")(test_case)

