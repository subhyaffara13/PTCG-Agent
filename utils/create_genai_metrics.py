
def create_genai_metrics(meter: Meter) -> GenAIMetrics:
    return GenAIMetrics(
        operation_duration=meter.create_histogram(
            name=Metric.OPERATION_DURATION,
            unit="s",
            description="GenAI operation duration",
        ),
        token_usage=meter.create_histogram(
            name=Metric.TOKEN_USAGE,
            unit="{token}",
            description="GenAI token usage",
        ),
        token_cost=meter.create_histogram(
            name=Metric.TOKEN_COST,
            unit="USD",
            description="GenAI request cost",
        ),
        time_to_first_token=meter.create_histogram(
            name=Metric.TIME_TO_FIRST_TOKEN,
            unit="s",
            description="Time to first token for streaming requests",
        ),
        time_per_output_token=meter.create_histogram(
            name=Metric.TIME_PER_OUTPUT_TOKEN,
            unit="s",
            description="Average time per output token (generation time / completion tokens)",
        ),
        response_duration=meter.create_histogram(
            name=Metric.RESPONSE_DURATION,
            unit="s",
            description="Total LLM API generation time (excludes LiteLLM overhead)",
        ),
    )

