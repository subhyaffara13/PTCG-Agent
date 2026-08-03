from typing import List

def _get_protected_indices(messages: List[dict]) -> List[int]:
    """
    Return indices of messages that must never be compressed:
    - All system messages
    - The last user message
    - The last assistant message
    """
    protected: List[int] = []

    last_user_idx = None
    last_assistant_idx = None

    for i, msg in enumerate(messages):
        role = msg.get("role", "")
        if role == "system":
            protected.append(i)
        elif role == "user":
            last_user_idx = i
        elif role == "assistant":
            last_assistant_idx = i

    if last_user_idx is not None:
        protected.append(last_user_idx)
    if last_assistant_idx is not None:
        protected.append(last_assistant_idx)

    return protected

