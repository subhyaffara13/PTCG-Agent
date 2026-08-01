
def _llm_judge(model: str = "gpt-4o-mini"):
    """LLM-as-judge using litellm.completion(). Requires API key env var."""
    return _LlmJudgeChecker(model=model)

