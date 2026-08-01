
def _scatter_meta_output(self):
    from torch.fx.experimental.symbolic_shapes import free_unbacked_symbols

    # Match clone_preserve_strides() in aten/native/TensorShape.cpp: overlapping
    # bases cannot preserve their logical strides because the scatter writes would
    # alias, so eager falls back to clone().
    if not free_unbacked_symbols(self) and torch._debug_has_internal_overlap(self) == 1:
        return self.clone()
    return utils.clone_preserve_strides(self)

