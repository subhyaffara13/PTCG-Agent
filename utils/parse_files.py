
def parse_files(subparsers) -> None:
    parser_files = subparsers.add_parser("files", formatter_class=argparse.RawTextHelpFormatter, help=Help.group_files)

    subparsers_files = parser_files.add_subparsers(title="commands", dest="command")
    subparsers_files.required = True
    subparsers_files.choices = Help.files_choices

    # Files upload
    parser_files_upload = subparsers_files.add_parser(
        "upload", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_files_upload, aliases=["u"]
    )
    parser_files_upload_optional = parser_files_upload._action_groups.pop()
    parser_files_upload_optional.add_argument(
        "-i", "--inbox-path", dest="inbox_path", required=False, default="", help=Help.param_files_upload_inbox_path
    )
    parser_files_upload_optional.add_argument(
        "local_paths", metavar="local-path", nargs="+", help=Help.param_files_upload_local_paths
    )
    parser_files_upload_optional.add_argument(
        "--no-resume",
        dest="no_resume",
        action="store_true",
        required=False,
        default=False,
        help=Help.param_files_upload_no_resume,
    )
    parser_files_upload_optional.add_argument(
        "--no-compress",
        dest="no_compress",
        action="store_true",
        required=False,
        default=False,
        help=Help.param_files_upload_no_compress,
    )
    parser_files_upload._action_groups.append(parser_files_upload_optional)
    parser_files_upload.set_defaults(func=api.files_upload_cli)

