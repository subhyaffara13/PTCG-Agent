
def save_module(pickler, obj):
    if False: #_use_diff:
        if obj.__name__.split('.', 1)[0] != "dill":
            try:
                changed = diff.whats_changed(obj, seen=pickler._diff_cache)[0]
            except RuntimeError:  # not memorised module, probably part of dill
                pass
            else:
                logger.trace(pickler, "M2: %s with diff", obj)
                logger.info("Diff: %s", changed.keys())
                pickler.save_reduce(_import_module, (obj.__name__,), obj=obj,
                                    state=changed)
                logger.trace(pickler, "# M2")
                return

        logger.trace(pickler, "M1: %s", obj)
        pickler.save_reduce(_import_module, (obj.__name__,), obj=obj)
        logger.trace(pickler, "# M1")
    else:
        builtin_mod = _is_builtin_module(obj)
        is_session_main = is_dill(pickler, child=True) and obj is pickler._main
        if (obj.__name__ not in ("builtins", "dill", "dill._dill") and not builtin_mod
                or is_session_main):
            logger.trace(pickler, "M1: %s", obj)
            # Hack for handling module-type objects in load_module().
            mod_name = obj.__name__ if _is_imported_module(obj) else '__runtime__.%s' % obj.__name__
            # Second references are saved as __builtin__.__main__ in save_module_dict().
            main_dict = obj.__dict__.copy()
            for item in ('__builtins__', '__loader__'):
                main_dict.pop(item, None)
            for item in IPYTHON_SINGLETONS: #pragma: no cover
                if getattr(main_dict.get(item), '__module__', '').startswith('IPython'):
                    del main_dict[item]
            pickler.save_reduce(_import_module, (mod_name,), obj=obj, state=main_dict)
            logger.trace(pickler, "# M1")
        elif obj.__name__ == "dill._dill":
            logger.trace(pickler, "M2: %s", obj)
            pickler.save_global(obj, name="_dill")
            logger.trace(pickler, "# M2")
        else:
            logger.trace(pickler, "M2: %s", obj)
            pickler.save_reduce(_import_module, (obj.__name__,), obj=obj)
            logger.trace(pickler, "# M2")
    return

