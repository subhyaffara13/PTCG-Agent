
def _handle_match(
    guardrail: SemanticGuardrail,
    route_name: str,
    similarity_score: Optional[float],
    user_text: str,
    data: dict,
) -> None:
    """Block or passthrough based on config."""
    violation_msg = (
        f"Request blocked by semantic guardrail '{guardrail.guardrail_name}'. "
        f"Matched route: {route_name}"
    )

    detection_info = {
        "route_name": route_name,
        "similarity_score": similarity_score,
        "guardrail": guardrail.guardrail_name,
    }

    verbose_logger.warning(
        f"SemanticGuard match: route={route_name}, score={similarity_score}, "
        f"action={guardrail.on_flagged_action}"
    )

    if guardrail.on_flagged_action == "passthrough":
        guardrail.raise_passthrough_exception(
            violation_message=violation_msg,
            request_data=data,
            detection_info=detection_info,
        )
    else:
        raise HTTPException(  # type: ignore[reportOptionalCall]
            status_code=400,
            detail={
                "error": violation_msg,
                "route": route_name,
                "similarity_score": similarity_score,
                "type": "semantic_guard_violation",
            },
        )

