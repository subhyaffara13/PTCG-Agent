
def require_serve(test_case):
    """
    Decorator marking a test that requires the serving dependencies (fastapi, uvicorn, pydantic, openai).
    """
    return unittest.skipUnless(is_serve_available(), "test requires serving dependencies")(test_case)

