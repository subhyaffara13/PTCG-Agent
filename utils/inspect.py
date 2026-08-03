from typing import Any, Optional

def inspect(cls):
    """
    Inspect the class and return its effective build parameters.

    Warning:
        This feature is currently **experimental** and is not covered by our
        strict backwards-compatibility guarantees.

    Args:
        cls: The *attrs*-decorated class to inspect.

    Returns:
        The effective build parameters of the class.

    Raises:
        NotAnAttrsClassError: If the class is not an *attrs*-decorated class.

    .. versionadded:: 25.4.0
    """
    try:
        return cls.__dict__["__attrs_props__"]
    except KeyError:
        msg = f"{cls!r} is not an attrs-decorated class."
        raise NotAnAttrsClassError(msg) from None


def inspect(path):
    print("Inspecting", path)
    dists = list(Distribution.discover(path=[path]))
    if not dists:
        return
    print("Found", len(dists), "packages:", end=' ')
    print(', '.join(dist.name for dist in dists))


def inspect(
    obj: Any,
    *,
    console: Optional["Console"] = None,
    title: Optional[str] = None,
    help: bool = False,
    methods: bool = False,
    docs: bool = True,
    private: bool = False,
    dunder: bool = False,
    sort: bool = True,
    all: bool = False,
    value: bool = True,
) -> None:
    """Inspect any Python object.

    * inspect(<OBJECT>) to see summarized info.
    * inspect(<OBJECT>, methods=True) to see methods.
    * inspect(<OBJECT>, help=True) to see full (non-abbreviated) help.
    * inspect(<OBJECT>, private=True) to see private attributes (single underscore).
    * inspect(<OBJECT>, dunder=True) to see attributes beginning with double underscore.
    * inspect(<OBJECT>, all=True) to see all attributes.

    Args:
        obj (Any): An object to inspect.
        title (str, optional): Title to display over inspect result, or None use type. Defaults to None.
        help (bool, optional): Show full help text rather than just first paragraph. Defaults to False.
        methods (bool, optional): Enable inspection of callables. Defaults to False.
        docs (bool, optional): Also render doc strings. Defaults to True.
        private (bool, optional): Show private attributes (beginning with underscore). Defaults to False.
        dunder (bool, optional): Show attributes starting with double underscore. Defaults to False.
        sort (bool, optional):  Sort attributes alphabetically, callables at the top, leading and trailing underscores ignored. Defaults to True.
        all (bool, optional): Show all attributes. Defaults to False.
        value (bool, optional): Pretty print value. Defaults to True.
    """
    _console = console or get_console()
    from rich._inspect import Inspect

    # Special case for inspect(inspect)
    is_inspect = obj is inspect

    _inspect = Inspect(
        obj,
        title=title,
        help=is_inspect or help,
        methods=is_inspect or methods,
        docs=is_inspect or docs,
        private=private,
        dunder=dunder,
        sort=sort,
        all=all,
        value=value,
    )
    _console.print(_inspect)


def inspect(path):
    print("Inspecting", path)
    dists = list(Distribution.discover(path=[path]))
    if not dists:
        return
    print("Found", len(dists), "packages:", end=' ')
    print(', '.join(dist.name for dist in dists))


def inspect(
    obj: Any,
    *,
    console: Optional["Console"] = None,
    title: Optional[str] = None,
    help: bool = False,
    methods: bool = False,
    docs: bool = True,
    private: bool = False,
    dunder: bool = False,
    sort: bool = True,
    all: bool = False,
    value: bool = True,
) -> None:
    """Inspect any Python object.

    * inspect(<OBJECT>) to see summarized info.
    * inspect(<OBJECT>, methods=True) to see methods.
    * inspect(<OBJECT>, help=True) to see full (non-abbreviated) help.
    * inspect(<OBJECT>, private=True) to see private attributes (single underscore).
    * inspect(<OBJECT>, dunder=True) to see attributes beginning with double underscore.
    * inspect(<OBJECT>, all=True) to see all attributes.

    Args:
        obj (Any): An object to inspect.
        title (str, optional): Title to display over inspect result, or None use type. Defaults to None.
        help (bool, optional): Show full help text rather than just first paragraph. Defaults to False.
        methods (bool, optional): Enable inspection of callables. Defaults to False.
        docs (bool, optional): Also render doc strings. Defaults to True.
        private (bool, optional): Show private attributes (beginning with underscore). Defaults to False.
        dunder (bool, optional): Show attributes starting with double underscore. Defaults to False.
        sort (bool, optional): Sort attributes alphabetically. Defaults to True.
        all (bool, optional): Show all attributes. Defaults to False.
        value (bool, optional): Pretty print value. Defaults to True.
    """
    _console = console or get_console()
    from pip._vendor.rich._inspect import Inspect

    # Special case for inspect(inspect)
    is_inspect = obj is inspect

    _inspect = Inspect(
        obj,
        title=title,
        help=is_inspect or help,
        methods=is_inspect or methods,
        docs=is_inspect or docs,
        private=private,
        dunder=dunder,
        sort=sort,
        all=all,
        value=value,
    )
    _console.print(_inspect)


def inspect(obj: object) -> None:
  """Inspect all attributes of a Python object interactivelly.

  Args:
    obj: Any object to inspect (module, class, dict,...).
  """
  root = nodes.Node.from_obj(obj)

  html_content = IPython.display.HTML(f"""
      {resource_utils.resource_import('theme.css')}
      {pyjs_com.js_import()}
      {resource_utils.resource_import('main.js')}

      {main_inspect_html(root)}
      <script>
        load_content("{root.id}");
      </script>
      """)
  IPython.display.display(html_content)

