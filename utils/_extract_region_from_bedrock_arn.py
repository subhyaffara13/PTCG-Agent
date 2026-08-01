
def _extract_region_from_bedrock_arn(arn: str) -> Optional[str]:
    """ARN shape: ``arn:aws:bedrock:<region>:<account>:<type>/<id>``"""
    try:
        parts = arn.split(":")
        if len(parts) >= 4 and parts[2] == "bedrock":
            return parts[3] or None
    except Exception:
        pass
    return None

