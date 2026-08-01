
def require_cv2(test_case):
    """
    Decorator marking a test that requires OpenCV.

    These tests are skipped when OpenCV isn't installed.

    """
    return unittest.skipUnless(is_cv2_available(), "test requires OpenCV")(test_case)

