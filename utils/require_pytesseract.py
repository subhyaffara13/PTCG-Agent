
def require_pytesseract(test_case):
    """
    Decorator marking a test that requires PyTesseract. These tests are skipped when PyTesseract isn't installed.
    """
    return unittest.skipUnless(is_pytesseract_available(), "test requires PyTesseract")(test_case)

