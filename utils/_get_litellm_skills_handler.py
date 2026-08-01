
def _get_litellm_skills_handler():
    """Lazy initialization of LiteLLM skills handler to avoid import overhead."""
    global _litellm_skills_handler
    if _litellm_skills_handler is None:
        from litellm.llms.litellm_proxy.skills.transformation import (
            LiteLLMSkillsTransformationHandler,
        )

        _litellm_skills_handler = LiteLLMSkillsTransformationHandler()
    return _litellm_skills_handler

