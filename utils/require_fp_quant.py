
def require_fp_quant(test_case):
    """
    Decorator marking a test that requires fp_quant and qutlass
    """
    return unittest.skipUnless(is_fp_quant_available(), "test requires fp_quant")(test_case)

