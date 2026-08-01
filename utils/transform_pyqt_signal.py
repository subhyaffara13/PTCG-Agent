
def transform_pyqt_signal(node: nodes.FunctionDef) -> None:
    module = parse(
        """
    _UNSET = object()

    class pyqtSignal(object):
        def connect(self, slot, type=None, no_receiver_check=False):
            pass
        def disconnect(self, slot=_UNSET):
            pass
        def emit(self, *args):
            pass
    """
    )
    signal_cls: nodes.ClassDef = module["pyqtSignal"]
    node.instance_attrs["emit"] = [signal_cls["emit"]]
    node.instance_attrs["disconnect"] = [signal_cls["disconnect"]]
    node.instance_attrs["connect"] = [signal_cls["connect"]]

