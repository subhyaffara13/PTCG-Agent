
def get_arg_uses(typemap: dict[Expression, Type], func: FuncDef) -> list[list[Type]]:
    """Find all the types of arguments that each arg is passed to.

    For example, given
      def foo(x: int) -> None: ...
      def bar(x: str) -> None: ...
      def test(x, y):
          foo(x)
          bar(y)

    this will return [[int], [str]].
    """
    finder = ArgUseFinder(func, typemap)
    func.body.accept(finder)
    return [finder.arg_types[arg.variable] for arg in func.arguments]

