
def _get_prompt_template(
    prompt_spec: PromptSpec, base_prompt_id: str
) -> Optional[PromptTemplateBase]:
    """Resolve the raw prompt template from dotprompt content or the in-memory registry."""
    from litellm.proxy.prompts.prompt_registry import IN_MEMORY_PROMPT_REGISTRY

    try:
        dotprompt_content = prompt_spec.litellm_params.dotprompt_content
        if dotprompt_content:
            from litellm.integrations.dotprompt import (
                _get_prompt_data_from_dotprompt_content,
            )

            parsed = _get_prompt_data_from_dotprompt_content(dotprompt_content)
            if parsed:
                return PromptTemplateBase(
                    litellm_prompt_id=base_prompt_id,
                    content=parsed.get("content", ""),
                    metadata=parsed.get("metadata"),
                )
        else:
            prompt_callback = IN_MEMORY_PROMPT_REGISTRY.get_prompt_callback_by_id(
                prompt_spec.prompt_id
            )
            if prompt_callback is not None:
                integration_name = prompt_callback.integration_name
                if integration_name == "dotprompt":
                    from litellm.integrations.dotprompt.dotprompt_manager import (
                        DotpromptManager,
                    )

                    if isinstance(prompt_callback, DotpromptManager):
                        template = (
                            prompt_callback.prompt_manager.get_all_prompts_as_json()
                        )
                        if template is not None and len(template) == 1:
                            template_id = list(template.keys())[0]
                            return PromptTemplateBase(
                                litellm_prompt_id=template_id,
                                content=template[template_id]["content"],
                                metadata=template[template_id]["metadata"],
                            )
    except Exception:
        pass
    return None

