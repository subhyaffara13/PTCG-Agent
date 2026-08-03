import functools

def catch_config_error(method: T) -> T:
    """Method decorator for catching invalid config (Trait/ArgumentErrors) during init.

    On a TraitError (generally caused by bad config), this will print the trait's
    message, and exit the app.

    For use on init methods, to prevent invoking excepthook on invalid input.
    """

    @functools.wraps(method)
    def inner(app: Application, *args: t.Any, **kwargs: t.Any) -> t.Any:
        try:
            return method(app, *args, **kwargs)
        except (TraitError, ArgumentError) as e:
            app.log.fatal("Bad config encountered during initialization: %s", e)
            app.log.debug("Config at the time: %s", app.config)
            app.exit(1)

    return t.cast(T, inner)

