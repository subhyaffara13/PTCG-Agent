
def _onnx_backend_session(model: str | io.BytesIO, backend: OnnxBackend):
    if backend == OnnxBackend.REFERENCE:
        raise NotImplementedError
    elif backend in {OnnxBackend.ONNX_RUNTIME_CPU, OnnxBackend.ONNX_RUNTIME_CUDA}:
        onnx_session = _ort_session(model, (backend.value,))
    else:
        raise ValueError(f"Unsupported backend: {backend}")
    return onnx_session

