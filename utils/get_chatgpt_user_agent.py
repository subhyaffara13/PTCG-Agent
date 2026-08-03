import os

def get_chatgpt_user_agent(originator: str) -> str:
    override = os.getenv("CHATGPT_USER_AGENT")
    if override:
        return _safe_header_value(override) or DEFAULT_USER_AGENT
    version = _get_litellm_version()
    os_type = platform.system() or "Unknown"
    os_version = platform.release() or "0"
    arch = platform.machine() or "unknown"
    terminal_ua = _terminal_user_agent()
    suffix = os.getenv("CHATGPT_USER_AGENT_SUFFIX", "").strip()
    suffix = f" ({suffix})" if suffix else ""
    candidate = (
        f"{originator}/{version} ({os_type} {os_version}; {arch}) {terminal_ua}{suffix}"
    )
    return _safe_header_value(candidate) or DEFAULT_USER_AGENT

