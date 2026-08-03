from typing import List

def _redact_assessment_match_fields(assessments: List[dict]) -> List[dict]:
    """
    Redact sensitive match-like fields from blocked assessment summaries.

    This is used for customer-visible error payloads (HTTPException.detail) where
    we want to preserve policy/type/action metadata without echoing raw matched
    content.
    """
    redacted = redact_nested_match_and_regex_keys(assessments)
    return redacted if isinstance(redacted, list) else assessments

