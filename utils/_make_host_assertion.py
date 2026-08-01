
def _make_host_assertion(assert_fn: TAssertFn,
                         name: Optional[str] = None) -> TChexAssertion:
  """Constructs a host assertion given `assert_fn`.

  This wrapper should only be applied to the assertions that are either
    a) never used in jitted code, or
    b) when used in jitted code they do not check/access tensor values (i.e.
       they do not introduce value-dependent python control flow, see
       https://jax.readthedocs.io/en/latest/errors.html#jax.errors.ConcretizationTypeError).

  Args:
    assert_fn: A function implementing the check.
    name: A name for assertion.

  Returns:
    A chex assertion.
  """
  if name is None:
    name = assert_fn.__name__

  def _assert_on_host(*args,
                      custom_message: Optional[str] = None,
                      custom_message_format_vars: Sequence[Any] = (),
                      include_default_message: bool = True,
                      exception_type: Type[Exception] = AssertionError,
                      **kwargs) -> None:
    # Format error's stack trace to remove Chex' internal frames.
    assertion_exc = None
    value_exc = None
    try:
      assert_fn(*args, **kwargs)
    except AssertionError as e:
      assertion_exc = e
    except ValueError as e:
      value_exc = e
    finally:
      if value_exc is not None:
        raise ValueError(str(value_exc))

      if assertion_exc is not None:
        # Format the exception message.
        error_msg = str(assertion_exc)

        # Include only the name of the outermost chex assertion.
        if error_msg.startswith(ERR_PREFIX):
          error_msg = error_msg[error_msg.find("failed:") + len("failed:"):]

        # Whether to include the default error message.
        default_msg = (f"Assertion {name} failed: "
                       if include_default_message else "")
        error_msg = f"{ERR_PREFIX}{default_msg}{error_msg}"

        # Whether to include a custom error message.
        if custom_message:
          if custom_message_format_vars:
            custom_message = custom_message.format(*custom_message_format_vars)
          error_msg = f"{error_msg} [{custom_message}]"

        raise exception_type(error_msg)

  return _assert_on_host

