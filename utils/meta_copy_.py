
def meta_copy_(self, src, non_blocking=False):
    # This code simulates the original decomp from inductor,
    # which runs most of the meta checks that we care about.
    # In theory, we should make this more robust by carefully
    # auditing our C++ copy_() kernel and copying the checks here.
    from torch.fx.experimental.symbolic_shapes import free_unbacked_symbols

    # TODO: Ideally, we'd insert a deferred runtime assert here, but if we are
    # calling an actual copy_, you'll get that automatically
    # https://github.com/pytorch/pytorch/issues/122477
    if (
        not free_unbacked_symbols(self) and torch._debug_has_internal_overlap(self) == 1
    ):  # 1 == MemOverlap::Yes
        raise RuntimeError(
            "more than one element of the written-to tensor refers to a single memory location"
        )

    if isinstance(src, Tensor):
        intermediate = src.to(self, non_blocking)
        # Validate broadcast compatibility. We call the _refs expand
        # directly rather than aten.expand_copy.default because the
        # aten dispatch path hits C++ that cannot handle unbacked
        # symints. The refs version performs the same checks using
        # sym_or(x == 1, requested_length == x) which gracefully
        # handles unbacked symints.
        torch._refs.expand(intermediate, self.size())
    return self

