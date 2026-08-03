from typing import Callable

def _supports_protocol(
    value: nodes.NodeNG, protocol_callback: Callable[[nodes.NodeNG], bool]
) -> bool:
    match value:
        case nodes.ClassDef():
            if not has_known_bases(value):
                return True
            # classobj can only be iterable if it has an iterable metaclass
            meta = value.metaclass()
            if meta is not None:
                if protocol_callback(meta):
                    return True
        case astroid.BaseInstance():
            if not has_known_bases(value):
                return True
            if value.has_dynamic_getattr():
                return True
            if protocol_callback(value):
                return True

        case nodes.ComprehensionScope():
            return True

        case bases.Proxy(_proxied=astroid.BaseInstance() as p) if has_known_bases(p):
            return protocol_callback(p)

    return False

