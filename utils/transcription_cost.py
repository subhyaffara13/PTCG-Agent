
def transcription_cost(
    model: str, custom_llm_provider: Optional[str], duration: float
) -> Tuple[float, float]:
    return openai_cost_per_second(
        model=model, custom_llm_provider=custom_llm_provider, duration=duration
    )

