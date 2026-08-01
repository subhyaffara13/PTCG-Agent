
def _run_in_app(
    function: abc.Callable[..., None],
    args: abc.Sequence[str],
    kwargs: abc.Mapping[str, Any],
) -> None:
  """Executes a set of Python unit tests, ensuring app.run.

  This is a private function, users should call absltest.main().

  _run_in_app calculates argv to be the command-line arguments of this program
  (without the flags), sets the default of FLAGS.alsologtostderr to True,
  then it calls function(argv, args, kwargs), making sure that `function'
  will get called within app.run(). _run_in_app does this by checking whether
  it is called by app.run(), or by calling app.run() explicitly.

  The reason why app.run has to be ensured is to make sure that
  flags are parsed and stripped properly, and other initializations done by
  the app module are also carried out, no matter if absltest.run() is called
  from within or outside app.run().

  If _run_in_app is called from within app.run(), then it will reparse
  sys.argv and pass the result without command-line flags into the argv
  argument of `function'. The reason why this parsing is needed is that
  __main__.main() calls absltest.main() without passing its argv. So the
  only way _run_in_app could get to know the argv without the flags is that
  it reparses sys.argv.

  _run_in_app changes the default of FLAGS.alsologtostderr to True so that the
  test program's stderr will contain all the log messages unless otherwise
  specified on the command-line. This overrides any explicit assignment to
  FLAGS.alsologtostderr by the test program prior to the call to _run_in_app()
  (e.g. in __main__.main).

  Please note that _run_in_app (and the function it calls) is allowed to make
  changes to kwargs.

  Args:
    function: absltest.run_tests or a similar function. It will be called as
        function(argv, args, kwargs) where argv is a list containing the
        elements of sys.argv without the command-line flags.
    args: Positional arguments passed through to unittest.TestProgram.__init__.
    kwargs: Keyword arguments passed through to unittest.TestProgram.__init__.
  """
  if _is_in_app_main():
    _register_sigterm_with_faulthandler()

    # Change the default of alsologtostderr from False to True, so the test
    # programs's stderr will contain all the log messages.
    # If --alsologtostderr=false is specified in the command-line, or user
    # has called FLAGS.alsologtostderr = False before, then the value is kept
    # False.
    FLAGS.set_default('alsologtostderr', True)

    # Here we only want to get the `argv` without the flags. To avoid any
    # side effects of parsing flags, we temporarily stub out the `parse` method
    stored_parse_methods = {}
    noop_parse = lambda _: None
    for name in FLAGS:
      # Avoid any side effects of parsing flags.
      stored_parse_methods[name] = FLAGS[name].parse
    # This must be a separate loop since multiple flag names (short_name=) can
    # point to the same flag object.
    for name in FLAGS:
      FLAGS[name].parse = noop_parse  # type: ignore[method-assign]
    try:
      argv = FLAGS(sys.argv)
    finally:
      for name in FLAGS:
        FLAGS[name].parse = stored_parse_methods[name]  # type: ignore[method-assign]
      sys.stdout.flush()

    function(argv, args, kwargs)
  else:
    # Send logging to stderr. Use --alsologtostderr instead of --logtostderr
    # in case tests are reading their own logs.
    FLAGS.set_default('alsologtostderr', True)

    def main_function(argv):
      _register_sigterm_with_faulthandler()
      function(argv, args, kwargs)

    app.run(main=main_function)

