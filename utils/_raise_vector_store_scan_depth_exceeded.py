
def _raise_vector_store_scan_depth_exceeded() -> None:
    raise HTTPException(
        status_code=400,
        detail={
            "error": f"Max depth of {DEFAULT_MAX_RECURSE_DEPTH} exceeded while scanning vector_store_id values"
        },
    )

