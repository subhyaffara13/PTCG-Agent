import functools
import sys
import time

def _log_export_wrapper(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        global _EXPORT_FLAGS, _EXPORT_MODULE_HIERARCHY
        try:
            start = time.time()
            ep = fn(*args, **kwargs)
            end = time.time()
            log_export_usage(
                event="export.time",
                metrics=end - start,
                flags=_EXPORT_FLAGS,
                **get_ep_stats(ep),
            )
        except Exception as e:
            t = type(e)
            error_type = t.__module__ + "." + t.__qualname__
            case_name = get_class_if_classified_error(e)
            if case_name is not None:
                log.error(exportdb_error_message(case_name))
                log_export_usage(
                    event="export.error.classified",
                    type=error_type,
                    message=str(e),
                    flags=_EXPORT_FLAGS,
                )
            else:
                log_export_usage(
                    event="export.error.unclassified",
                    type=error_type,
                    message=str(e),
                    flags=_EXPORT_FLAGS,
                )

            if hasattr(e, "partial_fx_graph"):
                print(
                    e.partial_fx_graph,
                    file=sys.stderr,
                )

            raise e
        finally:
            _EXPORT_FLAGS = None
            _EXPORT_MODULE_HIERARCHY = None

        return ep

    return wrapper

