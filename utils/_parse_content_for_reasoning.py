import re
from typing import Optional, Tuple

def _parse_content_for_reasoning(
    message_text: Optional[str],
) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse the content for reasoning

    Returns:
    - reasoning_content: The content of the reasoning
    - content: The content of the message
    """
    if not message_text:
        return None, message_text

    reasoning_match = re.match(
        r"<(?:think|thinking|budget:thinking)>(.*?)</(?:think|thinking|budget:thinking)>(.*)",
        message_text,
        re.DOTALL,
    )

    if reasoning_match:
        return reasoning_match.group(1), reasoning_match.group(2)

    return None, message_text

