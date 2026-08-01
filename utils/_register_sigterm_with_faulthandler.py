
def _register_sigterm_with_faulthandler() -> None:
  """Have faulthandler dump stacks on SIGTERM.  Useful to diagnose timeouts."""
  if getattr(faulthandler, 'register', None):
    # faulthandler.register is not available on Windows.
    # faulthandler.enable() is already called by app.run.
    try:
      faulthandler.register(signal.SIGTERM, chain=True)  # pytype: disable=module-attr
    except Exception as e:  # pylint: disable=broad-except
      sys.stderr.write('faulthandler.register(SIGTERM) failed '
                       '%r; ignoring.\n' % e)

