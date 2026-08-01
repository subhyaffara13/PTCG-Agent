
def _add_output_format_args(parser) -> None:
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--csv", dest="csv_display", action="store_true", help=Help.param_csv)
    group.add_argument(
        "--format",
        dest="output_format",
        help=Help.param_format,
    )

