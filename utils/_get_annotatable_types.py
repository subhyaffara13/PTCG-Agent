
def _get_annotatable_types() -> set[Any]:
    global _ANNOTATABLE_TYPES
    if _ANNOTATABLE_TYPES is None:
        _ANNOTATABLE_TYPES = {
            _cuda_runtime.cudaGraphNodeType.cudaGraphNodeTypeKernel,  # pyrefly: ignore[missing-attribute]
            _cuda_runtime.cudaGraphNodeType.cudaGraphNodeTypeMemcpy,  # pyrefly: ignore[missing-attribute]
        }
    return _ANNOTATABLE_TYPES

