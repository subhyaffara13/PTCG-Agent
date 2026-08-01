
def require_gptqmodel(test_case):
    """
    Decorator for gptqmodel dependency
    """
    return unittest.skipUnless(is_gptqmodel_available(), "test requires gptqmodel")(test_case)

