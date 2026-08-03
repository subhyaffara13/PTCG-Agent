import sys
from typing import Any

def _is_pytreespec_instance(
    obj: Any,
    /,
) -> TypeIs[TreeSpec | python_pytree.PyTreeSpec]:
    if isinstance(obj, (TreeSpec, python_pytree.PyTreeSpec)):
        return True
    if "torch._dynamo.polyfills.pytree" in sys.modules:
        # The PyTorch Dynamo pytree module is not always available, so we check if it is loaded.
        # If the PyTorch Dynamo pytree module is loaded, we can check if the treespec
        # is an instance of the PyTorch Dynamo TreeSpec class.
        import torch._dynamo.polyfills.pytree as dynamo_pytree

        return isinstance(obj, dynamo_pytree.PyTreeSpec)
    return False


def _is_pytreespec_instance(
    obj: Any,
) -> TypeIs["TreeSpec | cxx_pytree.PyTreeSpec"]:
    if isinstance(obj, TreeSpec):
        return True
    if "torch.utils._cxx_pytree" in sys.modules:
        # The C++ pytree module is not always available, so we check if it is loaded.
        # If the C++ pytree module is loaded, we can check if the treespec
        # is an instance of the C++ TreeSpec class.
        import torch.utils._cxx_pytree as cxx_pytree

        if isinstance(obj, cxx_pytree.PyTreeSpec):
            return True
    if "torch._dynamo.polyfills.pytree" in sys.modules:
        # The PyTorch Dynamo pytree module is not always available, so we check if it is loaded.
        # If the PyTorch Dynamo pytree module is loaded, we can check if the treespec
        # is an instance of the PyTorch Dynamo TreeSpec class.
        import torch._dynamo.polyfills.pytree as dynamo_pytree

        return isinstance(obj, dynamo_pytree.PyTreeSpec)
    return False


def _is_pytreespec_instance(obj: Any, /) -> TypeIs[PyTreeSpec | python_pytree.TreeSpec]:
    return isinstance(obj, (PyTreeSpec, python_pytree.TreeSpec))

