
def chex_assertion(
    assert_fn: TAssertFn,
    jittable_assert_fn: Optional[TJittableAssertFn],
    name: Optional[str] = None) -> TChexAssertion:
  """Wraps Chex assert functions to control their common behaviour.

  Extends the assertion to support the following optional auxiliary kwargs:
    custom_message: A string to include into the emitted exception messages.
    custom_message_format_vars: A list of variables to pass as arguments to
      `custom_message.format()`.
    include_default_message: Whether to include the default Chex message into
      the emitted exception messages.
    exception_type: An exception type to use. `AssertionError` by default.

  Args:
    assert_fn: A function implementing the check.
    jittable_assert_fn: An optional jittable version of `assert_fn` implementing
      a predicate (returning `True` only if assertion passes).
      Required for value assertions.
    name: A name for assertion. If not provided, use `assert_fn.__name__`.

  Returns:
    A Chex assertion (with auxiliary kwargs).
  """
  if name is None:
    name = assert_fn.__name__

  host_assertion_fn = _make_host_assertion(assert_fn, name)

  @functools.wraps(assert_fn)
  def _chex_assert_fn(*args,
                      custom_message: Optional[str] = None,
                      custom_message_format_vars: Sequence[Any] = (),
                      include_default_message: bool = True,
                      exception_type: Type[Exception] = AssertionError,
                      **kwargs) -> None:
    if DISABLE_ASSERTIONS:
      return
    if (jittable_assert_fn is not None and has_tracers((args, kwargs))):
      if not CHEXIFY_STORAGE.level:
        raise RuntimeError(
            "Value assertions can only be called from functions wrapped "
            "with `@chex.chexify`. See the docs.")

      # A wrapped to inject auxiliary debug info and `custom_message`.
      original_check = checkify.check

      def _check(pred, msg, *fmt_args, **fmt_kwargs):
        # Add chex info.
        msg = get_chexify_err_message(name, msg)

        # Add a custom message.
        if custom_message:
          msg += f" Custom message: {custom_message}."
          fmt_args = list(fmt_args) + list(custom_message_format_vars)

        # Add a traceback and a pointer to the callsite.
        stacktrace = get_stacktrace_without_chex_internals()
        msg += (
            f" [failed at: {stacktrace[-1].filename}:{stacktrace[-1].lineno}]"
        )

        # Call original `checkify.check()`.
        original_check(pred, msg, *fmt_args, **fmt_kwargs)

      # Mock during the assertion's execution time.
      checkify.check = _check
      pred = jittable_assert_fn(*args, **kwargs)  # execute the assertion
      checkify.check = original_check  # return the original implementation

      # A safeguard to ensure that the results of a check are not ignored.
      # In particular, this check fails when `pred` is False and no
      # `checkify.check` calls took place in `jittable_assert_fn`, which would
      # be a bug in the assertion's implementation.
      checkify.check(pred, "assertion failed!")
    else:
      try:
        host_assertion_fn(
            *args,
            custom_message=custom_message,
            custom_message_format_vars=custom_message_format_vars,
            include_default_message=include_default_message,
            exception_type=exception_type,
            **kwargs)
      except jax.errors.ConcretizationTypeError as exc:
        msg = ("Chex assertion detected `ConcretizationTypeError`: it is very "
               "likely that it tried to access tensors' values during tracing. "
               "Make sure that you defined a jittable version of this chex "
               "assertion; if that does not help, please file a bug.")
        raise exc from RuntimeError(msg)

  # Override name.
  setattr(_chex_assert_fn, "__name__", name)
  return _chex_assert_fn

