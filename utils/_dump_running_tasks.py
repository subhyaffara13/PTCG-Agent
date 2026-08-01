
def _dump_running_tasks(
    printout=True, cancel=True, exc=FSSpecCoroutineCancel, with_task=False
):
    import traceback

    tasks = [t for t in asyncio.tasks.all_tasks(loop[0]) if not t.done()]
    if printout:
        [task.print_stack() for task in tasks]
    out = [
        {
            "locals": task._coro.cr_frame.f_locals,
            "file": task._coro.cr_frame.f_code.co_filename,
            "firstline": task._coro.cr_frame.f_code.co_firstlineno,
            "linelo": task._coro.cr_frame.f_lineno,
            "stack": traceback.format_stack(task._coro.cr_frame),
            "task": task if with_task else None,
        }
        for task in tasks
    ]
    if cancel:
        for t in tasks:
            cbs = t._callbacks
            t.cancel()
            asyncio.futures.Future.set_exception(t, exc)
            asyncio.futures.Future.cancel(t)
            [cb[0](t) for cb in cbs]  # cancels any dependent concurrent.futures
            try:
                t._coro.throw(exc)  # exits coro, unless explicitly handled
            except exc:
                pass
    return out

