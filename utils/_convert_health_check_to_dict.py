
def _convert_health_check_to_dict(check) -> dict:
    """Convert health check database record to dictionary format"""
    return {
        "health_check_id": check.health_check_id,
        "model_name": check.model_name,
        "model_id": check.model_id,
        "status": check.status,
        "healthy_count": check.healthy_count,
        "unhealthy_count": check.unhealthy_count,
        "error_message": check.error_message,
        "response_time_ms": check.response_time_ms,
        "details": check.details,
        "checked_by": check.checked_by,
        "checked_at": check.checked_at.isoformat() if check.checked_at else None,
        "created_at": check.created_at.isoformat() if check.created_at else None,
    }

