
def semi_sparse_detach(func, types, args, kwargs) -> torch.Tensor:
    if len(args) != 1:
        raise AssertionError(f"expected 1 arg, got {len(args)}")
    self = args[0]
    return self.__class__(
        shape=self.shape,
        packed=self.packed,
        meta=self.meta,
        packed_t=self.packed_t,
        meta_t=self.meta_t,
        compressed_swizzled_bitmask=self.compressed_swizzled_bitmask,
        fuse_transpose_cusparselt=self.fuse_transpose_cusparselt,
        alg_id_cusparselt=self.alg_id_cusparselt,
        requires_grad=False,
    )

