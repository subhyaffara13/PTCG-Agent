
def _vlog_dispatch(fn: Callable[..., Any], dispatcher_name: str):
  if logging.vlog_is_on(1):
    logging.vlog(
        1,
        'Executing function %r via %s on process=%s/%s',
        fn,
        dispatcher_name,
        multihost.process_index(),
        multihost.process_count(),
    )

