
def _get_uncollectable_objects_info() -> Dict[str, Any]:
    """Get information about uncollectable objects (potential memory leaks)."""
    uncollectable = gc.garbage
    return {
        "count": len(uncollectable),
        "sample_types": [type(obj).__name__ for obj in uncollectable[:10]],
        "warning": (
            "If count > 0, you may have reference cycles preventing garbage collection"
            if len(uncollectable) > 0
            else None
        ),
    }

