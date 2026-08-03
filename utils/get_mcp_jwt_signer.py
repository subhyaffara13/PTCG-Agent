from typing import Optional

def get_mcp_jwt_signer() -> Optional["MCPJWTSigner"]:
    """Return the active MCPJWTSigner singleton, or None if not initialized."""
    return _mcp_jwt_signer_instance

