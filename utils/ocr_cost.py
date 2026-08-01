
def ocr_cost(
    model: str,
    custom_llm_provider: Optional[str],
    response: Optional[Any] = None,
) -> Tuple[float, float]:
    """
    Args:
        model: str - model name
        custom_llm_provider: Optional[str] - custom LLM provider
        response: Optional[Any] - response object

    Returns:
        Tuple[float, float]: cost of OCR processing

        (Parent function requires a tuple, so we return a tuple. Cost is only in the first element.)
    """
    from litellm.llms.base_llm.ocr.transformation import OCRResponse

    #########################################################
    # validate it's an OCR response
    #########################################################
    if response is None or not isinstance(response, OCRResponse):
        raise ValueError(
            f"response must be of type OCRResponse got type={type(response)}"
        )

    if response.usage_info is None:
        raise ValueError("OCR response usage_info is None")

    try:
        model_info: Optional[ModelInfo] = litellm.get_model_info(
            model=model, custom_llm_provider=custom_llm_provider
        )
    except Exception:
        model_info = None

    credits = getattr(response.usage_info, "credits", None)
    cost_per_credit = None
    if model_info is not None:
        cost_per_credit = model_info.get("ocr_cost_per_credit")
    if credits is not None and cost_per_credit is not None:
        return cost_per_credit * credits, 0.0

    ocr_cost_per_page: Optional[float] = None
    if model_info is not None:
        ocr_cost_per_page = model_info.get("ocr_cost_per_page")

    pages_processed = response.usage_info.pages_processed
    if pages_processed is None:
        if cost_per_credit is not None or ocr_cost_per_page is None:
            # Surface missing usage data instead of silently under-reporting
            # cost. The previous behavior raised ValueError; we now return 0.0
            # for credit-priced or unpriced models, so log a warning to keep
            # the regression visible to operators.
            verbose_logger.warning(
                "OCR cost: model=%s custom_llm_provider=%s response.usage_info."
                "pages_processed is None and credits=%s; returning 0.0 cost.",
                model,
                custom_llm_provider,
                credits,
            )
            return 0.0, 0.0
        raise ValueError("OCR response pages_processed is None")

    if ocr_cost_per_page is None:
        # No per-page pricing configured. Either the model is on credit-based
        # pricing (and credits weren't returned, so the credit branch above did
        # not match) or the model has no OCR pricing entry at all. Surface a
        # warning so that missing pricing entries are visible rather than
        # silently producing zero cost for billable usage.
        verbose_logger.warning(
            "OCR cost: model=%s custom_llm_provider=%s reported "
            "pages_processed=%s but no ocr_cost_per_page is configured; "
            "returning 0.0 cost.",
            model,
            custom_llm_provider,
            pages_processed,
        )
        return 0.0, 0.0

    total_ocr_processing_cost: float = ocr_cost_per_page * pages_processed
    return total_ocr_processing_cost, 0.0

