from typing import Any, Dict

def _validate_plugin_source(source: Dict[str, Any]) -> None:
    """Validate plugin source format, raising HTTPException on invalid input."""
    source_type = source.get("source")
    if source_type == "github":
        if "repo" not in source:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "GitHub source must include 'repo' field (e.g., 'org/repo')"
                },
            )
    elif source_type == "url":
        if "url" not in source:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "URL source must include 'url' field (e.g., 'https://github.com/org/repo.git')"
                },
            )
    elif source_type == "git-subdir":
        if not source.get("url"):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "git-subdir source must include 'url' field (e.g., 'https://github.com/org/repo.git')"
                },
            )
        if not source.get("path"):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "git-subdir source must include 'path' field (e.g., 'plugins/plugin-name')"
                },
            )
        if not _VALID_GIT_SUBDIR_PATH_RE.match(source["path"]):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "git-subdir 'path' must be a relative path of the form 'segment/segment' (alphanumeric, dots, hyphens, underscores only)"
                },
            )
    else:
        raise HTTPException(
            status_code=400,
            detail={"error": "source.source must be 'github', 'url', or 'git-subdir'"},
        )

