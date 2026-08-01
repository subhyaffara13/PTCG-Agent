
def create_script_fn(self, method_name, func_type):
    # function returns tuple containing original output and
    # filtered output to be used in checking gradients
    def script_fn(*args, **kwargs):
        fn, tensors = gen_script_fn_and_args(method_name, func_type, *args, **kwargs)
        self.assertExportImport(fn.graph, tensors)
        output = fn(*tensors)
        # skip type annotate function attributes for now, see: https://github.com/python/mypy/issues/2087
        script_fn.last_graph = fn.graph_for(*tensors)  # type: ignore[attr-defined]
        return output
    return script_fn

