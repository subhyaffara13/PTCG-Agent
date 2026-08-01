
def check_build_constraints(options: Values) -> None:
    """Function for validating build constraints options.

    :param options: The OptionParser options.
    """
    if hasattr(options, "build_constraints") and options.build_constraints:
        if not options.build_isolation:
            raise CommandError(
                "--build-constraint cannot be used with --no-build-isolation."
            )

        # Import here to avoid circular imports
        from pip._internal.network.session import PipSession
        from pip._internal.req.req_file import get_file_content

        # Eagerly check build constraints file contents
        # is valid so that we don't fail in when trying
        # to check constraints in isolated build process
        with PipSession() as session:
            for constraint_file in options.build_constraints:
                get_file_content(constraint_file, session)

