
def _assert_noop(*args,
                 custom_message: Optional[str] = None,
                 custom_message_format_vars: Sequence[Any] = (),
                 include_default_message: bool = True,
                 exception_type: Type[Exception] = AssertionError,
                 **kwargs) -> None:
  """No-op."""
  del args, custom_message, custom_message_format_vars
  del include_default_message, exception_type, kwargs

