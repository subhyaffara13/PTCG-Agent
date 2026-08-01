
def _fx_compile_mode_default() -> FxCompileConfig:
    name = "TORCHINDUCTOR_FX_COMPILE_MODE"
    value = os.environ.get(name)
    if value is None:
        return FxCompileConfig(FxCompileMode.NORMAL, False, False)

    use_async = False
    use_progressive = False

    if value.lower().startswith("progressive+"):
        use_progressive = True
        value = value[12:]
    if value.lower().startswith("async+"):
        use_async = True
        value = value[6:]

    try:
        value = value.upper()
        return FxCompileConfig(FxCompileMode[value], use_async, use_progressive)
    except KeyError:
        import logging

        log = logging.getLogger(__name__)
        log.error(
            "Invalid value of %s for %s. Expected one of %s. Using default.",
            value,
            name,
            ", ".join(sorted(repr(x) for x in FxCompileMode.__members__)),
        )
        # Remove from the environment so subprocesses don't ALSO complain.
        os.environ.pop(name)
        return FxCompileConfig(FxCompileMode.NORMAL, False, False)

