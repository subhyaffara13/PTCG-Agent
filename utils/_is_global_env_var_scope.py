from typing import Any

def _is_global_env_var_scope(scope: Any) -> bool:
    """``scope="user"`` entries are placeholders the user fills in; everything
    else (including a missing scope) is an admin-supplied global value."""
    return scope != MCPEnvVarScope.user and scope != "user"

