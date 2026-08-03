from typing import Any, Dict, List, Optional

def _last_user_content(messages: Optional[List[Dict[str, Any]]]) -> Optional[str]:
    if not messages:
        return None
    for msg in reversed(messages):
        if msg.get("role") == "user":
            content = msg.get("content")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                # OpenAI vision-style content: pick first text part.
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "text":
                        return part.get("text")
            return None
    return None

