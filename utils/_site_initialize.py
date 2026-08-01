
def _site_initialize():
    import importlib
    import itertools
    import logging
    from ._mlir import ir

    logger = logging.getLogger(__name__)
    post_init_hooks = []
    disable_multithreading = False
    # This flag disables eagerly loading all dialects. Eagerly loading is often
    # not the desired behavior (see
    # https://github.com/llvm/llvm-project/issues/56037), and the logic is that
    # if any module has this attribute set, then we don't load all (e.g., it's
    # being used in a solution where the loading is controlled).
    disable_load_all_available_dialects = False

    def process_initializer_module(module_name):
        nonlocal disable_multithreading
        nonlocal disable_load_all_available_dialects
        try:
            m = importlib.import_module(f".{module_name}", __name__)
        except ModuleNotFoundError:
            return False
        except ImportError:
            message = (
                f"Error importing mlir initializer {module_name}. This may "
                "happen in unclean incremental builds but is likely a real bug if "
                "encountered otherwise and the MLIR Python API may not function."
            )
            logger.warning(message, exc_info=True)
            return False

        logger.debug("Initializing MLIR with module: %s", module_name)
        if hasattr(m, "register_dialects"):
            logger.debug("Registering dialects from initializer %r", m)
            m.register_dialects(get_dialect_registry())
        if hasattr(m, "context_init_hook"):
            logger.debug("Adding context init hook from %r", m)
            post_init_hooks.append(m.context_init_hook)
        if hasattr(m, "disable_multithreading"):
            if bool(m.disable_multithreading):
                logger.debug("Disabling multi-threading for context")
                disable_multithreading = True
        if hasattr(m, "disable_load_all_available_dialects"):
            disable_load_all_available_dialects = True
        return True

    # If _mlirRegisterEverything is built, then include it as an initializer
    # module.
    init_module = None
    if process_initializer_module("_mlirRegisterEverything"):
        init_module = importlib.import_module(f"._mlirRegisterEverything", __name__)

    # Load all _site_initialize_{i} modules, where 'i' is a number starting
    # at 0.
    for i in itertools.count():
        module_name = f"_site_initialize_{i}"
        if not process_initializer_module(module_name):
            break

    ir._Context = ir.Context

    class Context(ir._Context):
        def __init__(
            self, load_on_create_dialects=None, thread_pool=None, *args, **kwargs
        ):
            super().__init__(*args, **kwargs)
            self.append_dialect_registry(get_dialect_registry())
            for hook in post_init_hooks:
                hook(self)
            if disable_multithreading and thread_pool is not None:
                raise ValueError(
                    "Context constructor has given thread_pool argument, "
                    "but disable_multithreading flag is True. "
                    "Please, set thread_pool argument to None or "
                    "set disable_multithreading flag to False."
                )
            if not disable_multithreading:
                if thread_pool is None:
                    self.enable_multithreading(True)
                else:
                    self.set_thread_pool(thread_pool)
            if load_on_create_dialects is not None:
                logger.debug(
                    "Loading all dialects from load_on_create_dialects arg %r",
                    load_on_create_dialects,
                )
                for dialect in load_on_create_dialects:
                    # This triggers loading the dialect into the context.
                    _ = self.dialects[dialect]
            else:
                if disable_load_all_available_dialects:
                    dialects = get_load_on_create_dialects()
                    if dialects:
                        logger.debug(
                            "Loading all dialects from global load_on_create_dialects %r",
                            dialects,
                        )
                        for dialect in dialects:
                            # This triggers loading the dialect into the context.
                            _ = self.dialects[dialect]
                else:
                    logger.debug("Loading all available dialects")
                    self.load_all_available_dialects()
            if init_module:
                logger.debug(
                    "Registering translations from initializer %r", init_module
                )
                init_module.register_llvm_translations(self)

    ir.Context = Context

    # Register containers as Sequences, so they can be used with `match`.

    Sequence.register(ir.BlockArgumentList)
    Sequence.register(ir.BlockList)
    Sequence.register(ir.BlockSuccessors)
    Sequence.register(ir.BlockPredecessors)
    Sequence.register(ir.OperationList)
    Sequence.register(ir.OpOperandList)
    Sequence.register(ir.OpOperands)
    Sequence.register(ir.OpResultList)
    Sequence.register(ir.OpSuccessors)
    Sequence.register(ir.RegionSequence)
    Mapping.register(ir.OpAttributeMap)

