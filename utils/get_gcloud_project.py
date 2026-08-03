import os
from typing import Optional

def get_gcloud_project() -> Optional[str]:
    """Attempts to get the Google Cloud project ID from environment or gcloud config."""
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if project:
        return project
    
    try:
        # Try gcloud
        import subprocess
        result = subprocess.run(
            ["gcloud", "config", "get-value", "project"],
            capture_output=True, text=True, check=True
        )
        project = result.stdout.strip()
        if project and "unset" not in project:
            return project
    except Exception:
        pass
    return None

