
def _validate_enrichment_request(data: EnrichTemplateRequest) -> tuple[dict, dict, str]:
    """
    Validate enrichment request and return (template, llm_enrichment, brand_name).

    Raises HTTPException on validation failure.
    """
    templates = _load_policy_templates_from_local_backup()
    template = next((t for t in templates if t.get("id") == data.template_id), None)
    if template is None:
        raise HTTPException(
            status_code=404, detail=f"Template '{data.template_id}' not found"
        )

    llm_enrichment = template.get("llm_enrichment")
    if llm_enrichment is None:
        raise HTTPException(
            status_code=400, detail="Template does not support LLM enrichment"
        )

    # Validate competitors list size if provided
    if data.competitors and len(data.competitors) > MAX_COMPETITOR_NAMES:
        raise HTTPException(
            status_code=400,
            detail=f"competitors list exceeds maximum of {MAX_COMPETITOR_NAMES}",
        )

    brand_name = data.parameters.get(llm_enrichment["parameter"], "")
    if not brand_name:
        raise HTTPException(
            status_code=400,
            detail=f"Parameter '{llm_enrichment['parameter']}' is required",
        )

    return template, llm_enrichment, brand_name

