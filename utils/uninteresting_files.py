import os
import sys

def uninteresting_files() -> set[str]:
    import torch._dynamo.external_utils
    import torch._dynamo.polyfills

    mods = [torch._dynamo.external_utils, torch._dynamo.polyfills]

    from torch._dynamo.polyfills.loader import POLYFILLED_MODULES

    # pyrefly: ignore [bad-argument-type]
    mods.extend(POLYFILLED_MODULES)

    return {inspect.getfile(m) for m in mods}


def uninteresting_files() -> set[str]:
    import torch._compile
    import torch._dynamo.eval_frame
    import torch._higher_order_ops
    import torch._inductor.sizevars
    import torch._library.custom_ops
    import torch._library.fake_impl
    import torch._logging
    import torch._subclasses.fake_tensor
    import torch._subclasses.meta_utils
    import torch.export._trace

    mods = [
        sys.modules[__name__],
        torch.export._trace,
        torch.fx.experimental.recording,
        torch.fx.experimental.sym_node,
        torch.fx.interpreter,
        torch.fx._symbolic_trace,
        torch,
        torch._compile,
        torch._dynamo.eval_frame,
        torch._inductor.sizevars,
        torch._library.custom_ops,
        torch._library.fake_impl,
        torch._subclasses.meta_utils,
        torch._subclasses.fake_tensor,
        torch._logging._internal,
        torch._logging.structured,
    ]
    import torch._dynamo.guards

    files = {inspect.getfile(m) for m in mods}

    # Add all Python files in torch._higher_order_ops directory
    higher_order_ops_dir = os.path.dirname(torch._higher_order_ops.__file__)
    hop_files = glob.glob(os.path.join(higher_order_ops_dir, "*.py"))

    return (
        files
        | set(hop_files)
        | torch._dynamo.guards.uninteresting_files()
        | {"<string>"}
    )

