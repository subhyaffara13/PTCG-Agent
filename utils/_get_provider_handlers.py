from typing import Dict

def _get_provider_handlers() -> Dict[str, Type[BaseTranslation]]:
    global _PROVIDER_HANDLERS
    if not _PROVIDER_HANDLERS:
        from litellm.llms.bedrock.passthrough.guardrail_translation.handler import (
            BedrockPassthroughGuardrailHandler,
        )

        _PROVIDER_HANDLERS = {"bedrock": BedrockPassthroughGuardrailHandler}
    return _PROVIDER_HANDLERS

