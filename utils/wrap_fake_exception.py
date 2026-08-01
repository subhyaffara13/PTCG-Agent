
def wrap_fake_exception(fn: Callable[[], Any]) -> Any:
    try:
        return fn()
    except UnsupportedFakeTensorException as e:
        from .exc import unimplemented

        msg = f"Encountered exception ({e.reason}) during fake tensor propagation."
        log.warning(msg)
        unimplemented(
            gb_type="Fake tensor propagation exception",
            context=str(e.reason),
            explanation=msg,
            hints=[],
            from_exc=e,
        )

