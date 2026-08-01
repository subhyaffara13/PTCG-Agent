
def _install_completion_no_auto_placeholder_function(
    install_completion: Shells = Option(
        None,
        callback=install_callback,
        expose_value=False,
        help="Install completion for the specified shell.",
    ),
    show_completion: Shells = Option(
        None,
        callback=show_callback,
        expose_value=False,
        help="Show completion for the specified shell, to copy it or customize the installation.",
    ),
) -> Any:
    pass  # pragma: no cover

