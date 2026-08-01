
def fail(msg: str, stderr: TextIO, options: Options) -> NoReturn:
    """Fail with a serious error."""
    stderr.write(f"{msg}\n")
    maybe_write_junit_xml(
        0.0, serious=True, all_messages=[msg], messages_by_file={None: [msg]}, options=options
    )
    sys.exit(2)


def fail(message: str) -> NoReturn:
    # TODO: Is there something else we should do to fail?
    sys.exit(message)


def fail(msg: str) -> NoReturn:
    print(msg, file=sys.stderr)
    sys.exit(2)


def fail(ctx: PluginContext, msg: str, context: Context | None) -> None:
    """Emit an error message.

    This tries to emit an error message at the location specified by `context`, falling back to the
    location specified by `ctx.context`. This is helpful when the only context information about
    where you want to put the error message may be None (like it is for `CallableType.definition`)
    and falling back to the location of the calling function is fine."""
    # TODO: figure out if there is some more reliable way of getting context information, so this
    # function isn't necessary
    if context is not None:
        err_context = context
    else:
        err_context = ctx.context
    ctx.api.fail(msg, err_context)


def fail(validator, errors, instance, schema):
    for each in errors:
        each.setdefault("message", "You told me to fail!")
        yield exceptions.ValidationError(**each)


def fail(e: Exception, device_id: int | None):
  shared_memory = _get_shared_memory()
  shared_memory.set_failed(e, device_id=device_id, top_level=True)

