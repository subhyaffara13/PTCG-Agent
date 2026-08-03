from typing import Optional

def get_chatgpt_default_headers(
    access_token: str,
    account_id: Optional[str],
    session_id: Optional[str] = None,
) -> dict:
    originator = get_chatgpt_originator()
    user_agent = get_chatgpt_user_agent(originator)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "content-type": "application/json",
        "accept": "text/event-stream",
        "originator": originator,
        "user-agent": user_agent,
    }
    if session_id:
        headers["session_id"] = session_id
    if account_id:
        headers["ChatGPT-Account-Id"] = account_id
    return headers

