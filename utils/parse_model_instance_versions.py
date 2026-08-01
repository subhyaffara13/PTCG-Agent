
def parse_model_instance_versions(subparsers) -> None:
    parser_model_instance_versions = subparsers.add_parser(
        "versions",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.group_model_instance_versions,
        aliases=["v"],
    )

    subparsers_model_intance_versions = parser_model_instance_versions.add_subparsers(title="commands", dest="command")
    subparsers_model_intance_versions.required = True
    subparsers_model_intance_versions.choices = Help.model_instance_versions_choices

    # Model Instance Versions list
    parser_model_instance_versions_list = subparsers_model_intance_versions.add_parser(
        "list", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instance_versions_list
    )
    parser_model_instance_versions_list_optional = parser_model_instance_versions_list._action_groups.pop()
    parser_model_instance_versions_list_optional.add_argument("model_instance", help=Help.param_model_instance)
    _add_output_format_args(parser_model_instance_versions_list_optional)
    parser_model_instance_versions_list_optional.add_argument(
        "--page-size", dest="page_size", default=20, type=int, help=Help.param_page_size
    )
    parser_model_instance_versions_list_optional.add_argument(
        "--page-token", dest="page_token", required=False, help=Help.param_page_token
    )
    parser_model_instance_versions_list._action_groups.append(parser_model_instance_versions_list_optional)
    parser_model_instance_versions_list.set_defaults(func=api.model_instance_versions_list_cli)

    # Model Instance Versions create
    parser_model_instance_versions_create = subparsers_model_intance_versions.add_parser(
        "create", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instance_versions_new
    )
    parser_model_instance_versions_create_optional = parser_model_instance_versions_create._action_groups.pop()
    parser_model_instance_versions_create_optional.add_argument("model_instance", help=Help.param_model_instance)
    parser_model_instance_versions_create_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_model_instance_version_upfile
    )
    parser_model_instance_versions_create_optional.add_argument(
        "-n", "--version-notes", dest="version_notes", required=False, help=Help.param_model_instance_version_notes
    )
    parser_model_instance_versions_create_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_model_instance_versions_create_optional.add_argument(
        "-r", "--dir-mode", dest="dir_mode", choices=["skip", "zip", "tar"], default="skip", help=Help.param_dir_mode
    )
    parser_model_instance_versions_create._action_groups.append(parser_model_instance_versions_create_optional)
    parser_model_instance_versions_create.set_defaults(func=api.model_instance_version_create_cli)

    # Models Instance Versions download
    parser_model_instance_versions_download = subparsers_model_intance_versions.add_parser(
        "download", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instance_versions_download
    )
    parser_model_instance_versions_download_optional = parser_model_instance_versions_download._action_groups.pop()
    parser_model_instance_versions_download_optional.add_argument(
        "model_instance_version", help=Help.param_model_instance_version
    )
    parser_model_instance_versions_download_optional.add_argument(
        "-p", "--path", dest="path", required=False, help=Help.param_downfolder
    )
    parser_model_instance_versions_download_optional.add_argument(
        "--untar", dest="untar", action="store_true", help=Help.param_untar
    )
    parser_model_instance_versions_download_optional.add_argument(
        "-f", "--force", dest="force", action="store_true", help=Help.param_force
    )
    parser_model_instance_versions_download_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_model_instance_versions_download._action_groups.append(parser_model_instance_versions_download_optional)
    parser_model_instance_versions_download.set_defaults(func=api.model_instance_version_download_cli)

    # Models Instance Versions files
    parser_model_instance_versions_files = subparsers_model_intance_versions.add_parser(
        "files", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instance_versions_files
    )
    parser_model_instance_versions_files_optional = parser_model_instance_versions_files._action_groups.pop()
    parser_model_instance_versions_files_optional.add_argument(
        "model_instance_version", help=Help.param_model_instance_version
    )
    _add_output_format_args(parser_model_instance_versions_files_optional)
    parser_model_instance_versions_files_optional.add_argument(
        "--page-size", dest="page_size", default=20, type=int, help=Help.param_page_size
    )
    parser_model_instance_versions_files_optional.add_argument(
        "--page-token", dest="page_token", required=False, help=Help.param_page_token
    )
    parser_model_instance_versions_files._action_groups.append(parser_model_instance_versions_files_optional)
    parser_model_instance_versions_files.set_defaults(func=api.model_instance_version_files_cli)

    # Models Instance Versions delete
    parser_model_instance_versions_delete = subparsers_model_intance_versions.add_parser(
        "delete", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instance_versions_delete
    )
    parser_model_instance_versions_delete_optional = parser_model_instance_versions_delete._action_groups.pop()
    parser_model_instance_versions_delete_optional.add_argument(
        "model_instance_version", help=Help.param_model_instance_version
    )
    parser_model_instance_versions_delete_optional.add_argument(
        "-y", "--yes", dest="no_confirm", action="store_true", help=Help.param_yes
    )
    parser_model_instance_versions_delete._action_groups.append(parser_model_instance_versions_delete_optional)
    parser_model_instance_versions_delete.set_defaults(func=api.model_instance_version_delete_cli)

