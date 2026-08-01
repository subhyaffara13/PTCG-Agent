
def sample_inputs_max_unpool_grad(op_info, device, dtype, requires_grad, **kwargs):
    for sample in sample_inputs_max_unpool(op_info, device, dtype, requires_grad, **kwargs):
        indices = sample.args[0]
        # The samples for max_unpool are generated with max_pool.
        # It could be that a single element from the max_pool's
        # input is mapped to several locations in its output.
        # This situation leads to failed gradchecks because
        # the finite difference algorithm perturbs the elements
        # of the output one by one, and not in classes of
        # equivalences determined by whether two elements
        # in the output are coming from the same location in the
        # input (simply put, they have the same corresponding index).
        # So, there are two ways to resolve this issue:
        # 1. Extract a perturbation for one element and apply it all
        #    the elements from the same equivalence class, or
        # 2. Make sure that the equivalence classes are all singletons,
        # i.e. the index tensor has to be comprised of only unique
        # indices.
        # Here we go with the solution 2, the easiest of all.
        if indices.unique().numel() == indices.numel():
            yield sample

