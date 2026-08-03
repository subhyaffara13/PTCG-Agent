import sys

def no_init_weights():
    """
    Disable weight initialization both at the torch-level, and at the transformers-level (`init_weights`).
    This is used to speed-up initializing an empty model with deepspeed, as we do not initialize the model on meta device
    with deepspeed, but we still don't need to run expensive weight initializations as we are loading params afterwards.
    """
    from .modeling_utils import PreTrainedModel

    def empty_func(*args, **kwargs):
        pass

    originals = defaultdict(dict)
    try:
        # Replace all torch funcs by empty ones
        for module_name in TORCH_MODULES_TO_PATCH:
            if module_name in sys.modules:
                module = sys.modules[module_name]
                for func_name in TORCH_INIT_FUNCTIONS.keys():
                    if hasattr(module, func_name):
                        originals[module][func_name] = getattr(module, func_name)
                        setattr(module, func_name, empty_func)

        # Also patch our own `init_weights`
        original_init_weights = PreTrainedModel.init_weights
        PreTrainedModel.init_weights = empty_func

        yield
    finally:
        # Set back the original torch functions on all modules
        for module, functions in originals.items():
            for func_name, func in functions.items():
                setattr(module, func_name, func)
        # Set back `init_weights`
        PreTrainedModel.init_weights = original_init_weights

