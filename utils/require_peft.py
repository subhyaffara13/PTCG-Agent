
def require_peft(test_case):
    """
    Decorator marking a test that requires PEFT.

    These tests are skipped when PEFT isn't installed.

    """
    return unittest.skipUnless(is_peft_available(), "test requires PEFT")(test_case)

