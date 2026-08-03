from typing import Any, List, Optional

def build_code_interpreter_log_outputs(
    content: Any,
) -> Optional[List[OutputCodeInterpreterCallLog]]:
    """Convert Anthropic bash_code_execution stdout/stderr to log outputs.

    Shared by streaming (handler.py) and non-streaming (transformation.py) paths.
    """
    if not isinstance(content, dict):
        return None
    parts = []
    if content.get("stdout"):
        parts.append(content["stdout"])
    if content.get("stderr"):
        parts.append(f"STDERR: {content['stderr']}")
    logs = "".join(parts)
    return [OutputCodeInterpreterCallLog(type="logs", logs=logs)] if logs else None

