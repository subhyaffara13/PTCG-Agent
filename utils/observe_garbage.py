
def observe_garbage(observer):
    enabled = True

    def disable() -> None:
        # when GC runs during exit, things like `sys` will already be unloaded
        # so we have to disable the callback to avoid hitting errors.
        nonlocal enabled
        enabled = False
    atexit.register(disable)

    def gc_callback(phase, info) -> None:
        nonlocal enabled
        if not enabled:
            return
        if phase == "start":
            gc.set_debug(gc.DEBUG_SAVEALL)
        elif phase == "stop":
            orig_trace = sys.getprofile()
            self_return = [False]

            def do_collect(*args, **kwargs):
                nonlocal enabled
                if not self_return[0]:
                    self_return[0] = True
                else:
                    sys.setprofile(orig_trace)
                    enabled = False
                    try:
                        # things in gc.garbage have survived a collection
                        # so to free them we have to collect a generation greater than them
                        # but that might _also_ free other stuff and we don't want to miss
                        # that stuff. So we have to now force gc at the highest level here,
                        # report all of what we found, _then_ we can free it up.
                        if info['generation'] != 2:
                            gc.collect()
                        observer(gc.garbage)
                        gc.garbage.clear()
                        # we have to re-run GC to clean up the cycles
                        # we saved from before.
                        gc.set_debug(0)
                        before = torch.cuda.memory_allocated()
                        gc.collect()
                        after = torch.cuda.memory_allocated()
                        if before != after:
                            logger.warning("CUDA Memory changed during GC, %d bytes freed.", before - after)
                    finally:
                        enabled = True
                if orig_trace is not None:
                    return orig_trace(*args, **kwargs)
            sys.setprofile(do_collect)

    gc.callbacks.append(gc_callback)

    # provide a way to disarm the callback
    def remove() -> None:
        gc.callbacks.remove(gc_callback)
    return remove

