
def unbind(x, dim=0):
    dim = _validate_dim(x, dim, 0)
    x_size = V.graph.sizevars.guard_int(x.get_size()[dim])
    result = [select(x, dim, i) for i in range(x_size)]
    return result


def unbind(t: TensorLikeType, dim: int = 0) -> TensorSequenceType:
    dim = utils.canonicalize_dim(t.ndim, dim)
    torch._check_index(
        len(t.shape) > 0,
        lambda: "Dimension specified as 0 but tensor has no dimensions",
    )

    # Note: t.shape[dim] can't be dynamic or unbacked, even if we use guard_or_false here we will fail
    # later in the split since t.shape[dim] control the number of output tensors.
    if t.shape[dim] == 0:
        return ()
    else:
        return tuple(
            torch.squeeze(s, dim) for s in torch.tensor_split(t, t.shape[dim], dim)
        )


def unbind(g: jit_utils.GraphContext, self, dim=0, _outputs=None):
    if _outputs is None:
        return g.op(
            "SplitToSequence",
            self,
            g.op("Constant", value_t=torch.tensor(1, dtype=torch.long)),
            axis_i=dim,
            keepdims_i=0,
        )
    else:
        return opset9.unbind(g, self, dim, _outputs)


def unbind(g: jit_utils.GraphContext, self, dim=0, _outputs=None):
    if _outputs is None:
        return g.op(
            "SplitToSequence",
            self,
            g.op("Constant", value_t=torch.tensor(1, dtype=torch.long)),
            axis_i=dim,
            keepdims_i=0,
        )

    splits = g.op("Constant", value_t=torch.tensor([1] * _outputs))
    outputs = g.op("Split", self, splits, axis_i=dim, outputs=_outputs)
    outputs = [outputs] if _outputs == 1 else outputs
    squeezed_outputs = [
        g.op("Squeeze", out, g.op("Constant", value_t=torch.tensor([dim])))
        for out in outputs
    ]
    return squeezed_outputs


def unbind(g: jit_utils.GraphContext, self, dim=0, _outputs=None):
    if _outputs is None:
        return symbolic_helper._onnx_opset_unsupported_detailed(
            "unbind", 9, 11, "Dynamic number of outputs not supported", self
        )

    outputs = g.op("Split", self, split_i=[1] * _outputs, axis_i=dim, outputs=_outputs)
    outputs = [outputs] if _outputs == 1 else outputs
    squeezed_outputs = [
        symbolic_helper._squeeze_helper(g, out, [dim]) for out in outputs
    ]
    return squeezed_outputs

