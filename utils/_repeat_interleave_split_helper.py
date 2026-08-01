
def _repeat_interleave_split_helper(g: jit_utils.GraphContext, self, reps, dim):
    if g.opset <= 12:
        split_out = g.op("Split", self, split_i=[1] * reps, axis_i=dim, outputs=reps)
    else:
        from torch.onnx._internal.torchscript_exporter.symbolic_opset13 import split

        repeats = g.op("Constant", value_t=torch.tensor([1] * reps))
        split_out = split(g, self, repeats, dim, _outputs=reps)
    return split_out if reps > 1 else [split_out]

