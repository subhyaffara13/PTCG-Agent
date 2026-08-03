import os

def is_colab_enterprise() -> bool:
    """Return `True` if code is executed in a Google Colab Enterprise environment."""
    return os.environ.get("VERTEX_PRODUCT") == "COLAB_ENTERPRISE"

