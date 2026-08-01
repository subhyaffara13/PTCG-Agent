
def _looks_like_signal(
    node: nodes.FunctionDef, signal_name: str = "pyqtSignal"
) -> bool:
    """Detect a Signal node."""
    klasses = node.instance_attrs.get("__class__", [])
    # On PySide2 or PySide6 (since  Qt 5.15.2) the Signal class changed locations
    if node.qname().partition(".")[0] in {"PySide2", "PySide6"}:
        return any(cls.qname() == "Signal" for cls in klasses)  # pragma: no cover
    if klasses:
        try:
            return klasses[0].name == signal_name
        except AttributeError:  # pragma: no cover
            # return False if the cls does not have a name attribute
            pass
    return False

