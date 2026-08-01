
def require_bs4(test_case):
    """
    Decorator marking a test that requires BeautifulSoup4. These tests are skipped when BeautifulSoup4 isn't installed.
    """
    return unittest.skipUnless(is_bs4_available(), "test requires BeautifulSoup4")(test_case)

