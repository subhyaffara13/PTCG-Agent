
def create_traced_fn(self, fn, cache_traced_fn=False):
    def traced_fn(*inputs, **kwargs):
        # `check_trace` is set to False because check_trace is run with @no_grad
        # Also, `check_against_reference` already does all the checks
        # against python function
        fn_tensors, split_inputs = partial_apply_nontensors(fn, inputs, kwargs)
        if not cache_traced_fn or not hasattr(traced_fn, 'traced'):
            traced = torch.jit.trace(fn_tensors, split_inputs.all_tensors, check_trace=False)
            self.assertExportImport(traced.graph, split_inputs.all_tensors)
            output = traced(*split_inputs.all_tensors)
            if cache_traced_fn:
                traced_fn.traced = traced
                traced_fn.split_inputs = split_inputs
        else:
            # Guard to check that nontensor inputs are the same as during tracing
            self.assertTrue(traced_fn.split_inputs.nontensors_match(split_inputs))
            output = traced_fn.traced(*split_inputs.all_tensors)
            traced = traced_fn.traced
        # skip type annotate function attributes for now, see: https://github.com/python/mypy/issues/2087
        traced_fn.last_graph = traced.graph_for(*split_inputs.all_tensors)  # type: ignore[attr-defined]
        traced_fn.graph = traced.graph  # type: ignore[attr-defined]
        return output
    return traced_fn

