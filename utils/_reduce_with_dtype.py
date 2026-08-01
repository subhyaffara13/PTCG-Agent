
def _reduce_with_dtype(onnx_op, name):
    symbolic = _reduce_op_symbolic(onnx_op)

    @symbolic_helper._overload_by_arg_count
    def reduce(g, *args, **kwargs):
        @symbolic_helper.parse_args("v", "none")
        def reduce_nodim(g, self, dtype):
            dtype_onnx = None
            if dtype.node().kind() == "onnx::Constant":
                dtype = symbolic_helper._get_const(dtype, "i", "dtype")
                dtype_onnx = _type_utils.JitScalarType(dtype).onnx_type()
                self = g.op("Cast", self, to_i=dtype_onnx)
            elif dtype.node().kind() != "prim::Constant":
                return symbolic_helper._unimplemented(name, "dtype", dtype)
            result = symbolic(g, self)
            if dtype_onnx is not None:
                result_dtype_onnx = _type_utils.JitScalarType.from_value(
                    result
                ).onnx_type()
                if result_dtype_onnx != dtype_onnx:
                    result = g.op("Cast", result, to_i=dtype_onnx)
            return result

        @symbolic_helper.parse_args("v", "v", "i", "none")
        def reduce_dim(g, self, dim, keepdim, dtype):
            dtype_onnx = None
            if dtype.node().kind() == "onnx::Constant":
                dtype = symbolic_helper._get_const(dtype, "i", "dtype")
                dtype_onnx = _type_utils.JitScalarType(dtype).onnx_type()
                self = g.op("Cast", self, to_i=dtype_onnx)
            elif dtype.node().kind() != "prim::Constant":
                return symbolic_helper._unimplemented(name, "dtype", dtype)
            result = symbolic(g, self, dim, keepdim)
            if dtype_onnx is not None:
                result_dtype_onnx = _type_utils.JitScalarType.from_value(
                    result
                ).onnx_type()
                if result_dtype_onnx != dtype_onnx:
                    result = g.op("Cast", result, to_i=dtype_onnx)
            return result

        return reduce_nodim, reduce_dim

    return reduce


def _reduce_with_dtype(onnx_op: str, name: str, allow_multi_dim_support: bool = True):
    return symbolic_helper._reduce_with_dtype_helper(
        onnx_op, name, allow_multi_dim_support
    )


def _reduce_with_dtype(onnx_op: str, name: str, allow_multi_dim_support: bool = True):
    return symbolic_helper._reduce_with_dtype_helper(
        onnx_op, name, allow_multi_dim_support
    )

