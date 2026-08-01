
def test_app(req: Request) -> Response:
    """Simple test application that dumps the environment.  You can use
    it to check if Werkzeug is working properly:

    .. sourcecode:: pycon

        >>> from werkzeug.serving import run_simple
        >>> from werkzeug.testapp import test_app
        >>> run_simple('localhost', 3000, test_app)
         * Running on http://localhost:3000/

    The application displays important information from the WSGI environment,
    the Python interpreter and the installed libraries.
    """
    try:
        import pkg_resources
    except ImportError:
        eggs: t.Iterable[t.Any] = ()
    else:
        eggs = sorted(
            pkg_resources.working_set,
            key=lambda x: x.project_name.lower(),
        )
    python_eggs = []
    for egg in eggs:
        try:
            version = egg.version
        except (ValueError, AttributeError):
            version = "unknown"
        python_eggs.append(
            f"<li>{escape(egg.project_name)} <small>[{escape(version)}]</small>"
        )

    wsgi_env = []
    sorted_environ = sorted(req.environ.items(), key=lambda x: repr(x[0]).lower())
    for key, value in sorted_environ:
        value = "".join(wrap(str(escape(repr(value)))))
        wsgi_env.append(f"<tr><th>{escape(key)}<td><code>{value}</code>")

    sys_path = []
    for item, virtual, expanded in iter_sys_path():
        css = []
        if virtual:
            css.append("virtual")
        if expanded:
            css.append("exp")
        class_str = f' class="{" ".join(css)}"' if css else ""
        sys_path.append(f"<li{class_str}>{escape(item)}")

    context = {
        "python_version": "<br>".join(escape(sys.version).splitlines()),
        "platform": escape(sys.platform),
        "os": escape(os.name),
        "api_version": sys.api_version,
        "byteorder": sys.byteorder,
        "werkzeug_version": _get_werkzeug_version(),
        "python_eggs": "\n".join(python_eggs),
        "wsgi_env": "\n".join(wsgi_env),
        "sys_path": "\n".join(sys_path),
    }
    return Response(TEMPLATE % context, mimetype="text/html")

