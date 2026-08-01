
def _check_input_constraints_for_module(self, args, kwargs):
    flat_args_with_path = _check_inputs_match(args, kwargs, self._in_spec)
    _check_input_constraints_for_graph(
        self.graph.find_nodes(op="placeholder"),
        flat_args_with_path,
        self.range_constraints,
    )

