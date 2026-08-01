
def _resolve_model_id_with_router(
    model_id: Optional[str], llm_router: Optional[Router]
) -> Optional[str]:
    if model_id is None or llm_router is None:
        return model_id
    try:
        return llm_router.resolve_model_name_from_model_id(model_id) or model_id
    except Exception as e:
        verbose_proxy_logger.debug(
            "Unable to resolve model_id from managed resource ID: %s", str(e)
        )
        return model_id

