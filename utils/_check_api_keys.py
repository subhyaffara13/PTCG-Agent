
def _check_api_keys() -> bool:
    if os.environ.get("GEMINI_API_KEY") or os.environ.get("OPENAI_API_KEY"):
        return True
    print("Set GEMINI_API_KEY or OPENAI_API_KEY to run this test.")
    print("Example: export GEMINI_API_KEY=your_key")
    return False

