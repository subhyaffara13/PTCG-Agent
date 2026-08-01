
def load_guardrail_translation_mappings():
    global endpoint_guardrail_translation_mappings
    if endpoint_guardrail_translation_mappings is None:
        endpoint_guardrail_translation_mappings = (
            discover_guardrail_translation_mappings()
        )
    return endpoint_guardrail_translation_mappings

