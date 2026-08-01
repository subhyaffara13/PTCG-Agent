
def make_flags_parser(
    cls: _DataclassT,
    *,
    prog: Optional[str] = None,
    description: Optional[str] = None,
    **extra_kwargs,
) -> Callable[[list[str]], _DataclassT]:
  """Dataclass flag parser for absl.

  Allow to define CLI flags through dataclasses.

  Usage:

  ```python
  @dataclasses.dataclass
  class Args:
    user: str
    verbose: bool = False


  def main(args: Args):
    if args.verbose:
      print(args.user)


  if __name__ == '__main__':
    app.run(main, flags_parser=eapp.make_flags_parser(Args))
  ```

  Allow to call your program with `my_program --user=$USER --verbose`

  This is a wrapper around `simple_parsing`
  (https://github.com/lebrice/SimpleParsing). See documentation for details.

  Args:
    cls: Dataclass containing the arguments to be parsed
    prog: Program name. Forwarded to `argparse.ArgumentParser`
    description: Description (auto-extracted from the `__main__` docstring)
      Forwarded to `argparse.ArgumentParser`
    **extra_kwargs: Extra arguments to be forwarded to `argparse.ArgumentParser`

  Returns:
    flags_parser function, for `app.run(main, flags_parser=...)`.
  """

  if not description and __main__.__doc__:
    description = __main__.__doc__.split('\n', 1)[0]

  def _flag_parser(argv: list[str]) -> _DataclassT:
    parser = simple_parsing.ArgumentParser(
        prog=prog,
        description=description,
        **extra_kwargs,
    )
    parser.add_arguments(cls, dest='args')

    namespace, remaining_argv = parser.parse_known_args(argv[1:])

    # Parse absl.flags
    # For consistency with argparse, we could catch
    # `flags.IllegalFlagValueError` and exit through sys.exit(),
    # like absl.flags.argparse_flags
    FLAGS([''] + remaining_argv)

    # Forward the parsed args to `main`
    return namespace.args

  return _flag_parser

