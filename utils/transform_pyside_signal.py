
def transform_pyside_signal(node: nodes.FunctionDef) -> None:
    module = parse(
        """
    class NotPySideSignal(object):
        def connect(self, receiver, type=None):
            pass
        def disconnect(self, receiver):
            pass
        def emit(self, *args):
            pass
    """
    )
    signal_cls: nodes.ClassDef = module["NotPySideSignal"]
    node.instance_attrs["connect"] = [signal_cls["connect"]]
    node.instance_attrs["disconnect"] = [signal_cls["disconnect"]]
    node.instance_attrs["emit"] = [signal_cls["emit"]]

