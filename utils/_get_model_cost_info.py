
def _get_model_cost_info(
    model: str,
    llm_router: Optional[Router],
) -> Optional[Dict[str, Any]]:
    if llm_router is not None:
        try:
            model_group_info = llm_router.get_model_group_info(model_group=model)
            if model_group_info is not None:
                return model_group_info.model_dump()
        except Exception:
            verbose_proxy_logger.debug(
                "Unable to load router model group info for budget reservation",
                exc_info=True,
            )

    try:
        return dict(litellm.get_model_info(model=model))
    except Exception:
        return None

