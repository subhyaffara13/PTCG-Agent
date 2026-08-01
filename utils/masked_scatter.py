
def masked_scatter(
    self: torch.Tensor,
    mask: torch.Tensor,
    source: torch.Tensor,
) -> torch.Tensor:
    from .codegen.common import BackendFeature, has_backend_feature

    if has_backend_feature(self.device, BackendFeature.MASKED_SCATTER_WITH_INDEX):
        # This two-step algorithm is the same as eager CUDA, for eager CPU we
        # use a 1-shot serial iteration.
        self, mask = aten.broadcast_tensors([self, mask])
        source_idx = mask.reshape(-1).cumsum(0) - 1
        self_flat, mask_flat, source_flat = (x.flatten() for x in (self, mask, source))
        result = aten._unsafe_masked_index(source_flat, mask_flat, [source_idx], 0)
        return torch.where(mask_flat, result, self_flat).view(self.shape)
    return NotImplemented


def masked_scatter(g: jit_utils.GraphContext, self, mask, source):
    index = opset9.nonzero(g, opset9.expand_as(g, mask, self))
    # NOTE: source can have more elements than needed.
    # It could also have arbitrary shape.
    # This is not supported by ONNX::ScatterND, so we need to flatten and slice source tensor.
    source = symbolic_helper._reshape_helper(g, source, torch.LongTensor([-1]))
    source = symbolic_helper._slice_helper(
        g,
        source,
        axes=torch.LongTensor([0]),
        starts=torch.LongTensor([0]),
        ends=opset9.size(g, index, torch.LongTensor([0])),
    )
    return g.op("ScatterND", self, index, source)

