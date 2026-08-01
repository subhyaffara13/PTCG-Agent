
def show_formats():
    """Print list of available formats (arguments to "--format" option)."""
    from ..fancy_getopt import FancyGetopt

    formats = [
        ("formats=" + format, None, bdist.format_commands[format][1])
        for format in bdist.format_commands
    ]
    pretty_printer = FancyGetopt(formats)
    pretty_printer.print_help("List of available distribution formats:")


def show_formats():
    """Print all possible values for the 'formats' option (used by
    the "--help-formats" command-line option).
    """
    from ..archive_util import ARCHIVE_FORMATS
    from ..fancy_getopt import FancyGetopt

    formats = sorted(
        ("formats=" + format, None, ARCHIVE_FORMATS[format][2])
        for format in ARCHIVE_FORMATS.keys()
    )
    FancyGetopt(formats).print_help("List of available source distribution formats:")

