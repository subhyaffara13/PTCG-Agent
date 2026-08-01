
def _model_accepts_output_config_effort(model: str) -> bool:
    """Whether ``model`` accepts ``output_config.effort`` on Vertex.

    Opus/Sonnet 4.6+ advertise ``supports_output_config`` (or a reasoning
    effort level) and accept it; Haiku 4.5 advertises neither and 400s on
    ``output_config.effort: Extra inputs are not permitted``. Imported lazily
    so this stays a leaf module (see module docstring).
    """
    from litellm.llms.anthropic.chat.transformation import AnthropicConfig

    return AnthropicConfig._model_supports_effort_param(model)

