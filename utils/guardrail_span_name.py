
def guardrail_span_name(data: "GuardrailSpanData") -> str:
    return f"execute_guardrail {data.guardrail_name}".strip()

