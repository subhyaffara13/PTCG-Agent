
def compare_onnx_shape_with_qnn_shape(onnx_dims, qnn_dims):
    assert len(onnx_dims) == len(qnn_dims), "Onnx shape and Qnn shape has different rank."
    return all(onnx_dims[i].dim_value == qnn_dims[i] for i in range(len(onnx_dims)))

