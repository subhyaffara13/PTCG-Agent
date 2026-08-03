from typing import Any

def get_style_guide(**kwargs: Any) -> StyleGuide:
    r"""Provision a StyleGuide for use.

    :param \*\*kwargs:
        Keyword arguments that provide some options for the StyleGuide.
    :returns:
        An initialized StyleGuide
    """
    application = app.Application()
    application.plugins, application.options = parse_args([])
    # We basically want application.initialize to be called but with these
    # options set instead before we make our formatter, notifier, internal
    # style guide and file checker manager.
    options = application.options
    for key, value in kwargs.items():
        try:
            getattr(options, key)
            setattr(options, key, value)
        except AttributeError:
            LOG.error('Could not update option "%s"', key)
    application.make_formatter()
    application.make_guide()
    application.make_file_checker_manager([])
    return StyleGuide(application)

