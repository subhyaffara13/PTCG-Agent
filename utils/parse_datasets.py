
def parse_datasets(subparsers) -> None:
    parser_datasets = subparsers.add_parser(
        "datasets", formatter_class=argparse.RawTextHelpFormatter, help=Help.group_datasets, aliases=["d"]
    )
    subparsers_datasets = parser_datasets.add_subparsers(title="commands", dest="command")
    subparsers_datasets.required = True
    subparsers_datasets.choices = Help.datasets_choices

    # Datasets delete
    parser_datasets_delete = subparsers_datasets.add_parser(
        "delete", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_datasets_delete
    )
    parser_datasets_delete_optional = parser_datasets_delete._action_groups.pop()
    parser_datasets_delete_optional.add_argument("dataset", help=Help.param_dataset)
    parser_datasets_delete_optional.add_argument(
        "-y", "--yes", dest="no_confirm", action="store_true", help=Help.param_yes
    )
    parser_datasets_delete._action_groups.append(parser_datasets_delete_optional)
    parser_datasets_delete.set_defaults(func=api.dataset_delete_cli)

    # Datasets list
    parser_datasets_list = subparsers_datasets.add_parser(
        "list", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_datasets_list
    )
    parser_datasets_list_optional = parser_datasets_list._action_groups.pop()
    parser_datasets_list.add_argument("--sort-by", dest="sort_by", required=False, help=Help.param_dataset_sort_by)
    parser_datasets_list.add_argument("--size", dest="size", type=int, required=False, help=Help.param_dataset_size)
    parser_datasets_list.add_argument(
        "--file-type", dest="file_type", required=False, help=Help.param_dataset_file_type
    )
    parser_datasets_list.add_argument("--license", dest="license_name", required=False, help=Help.param_dataset_license)
    parser_datasets_list.add_argument("--tags", dest="tag_ids", required=False, help=Help.param_dataset_tags)
    parser_datasets_list.add_argument("-s", "--search", dest="search", required=False, help=Help.param_search)
    parser_datasets_list.add_argument("-m", "--mine", dest="mine", action="store_true", help=Help.param_mine)
    parser_datasets_list.add_argument("--user", dest="user", required=False, help=Help.param_dataset_user)
    parser_datasets_list.add_argument(
        "-p", "--page", dest="page", default=1, type=int, required=False, help=Help.param_page
    )
    _add_output_format_args(parser_datasets_list)
    parser_datasets_list.add_argument(
        "--max-size", dest="max_size", required=False, type=int, help=Help.param_dataset_maxsize
    )
    parser_datasets_list.add_argument(
        "--min-size", dest="min_size", required=False, type=int, help=Help.param_dataset_minsize
    )
    parser_datasets_list._action_groups.append(parser_datasets_list_optional)
    parser_datasets_list.set_defaults(func=api.dataset_list_cli)

    # Datasets file list
    parser_datasets_files = subparsers_datasets.add_parser(
        "files", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_datasets_files
    )
    parser_datasets_files_optional = parser_datasets_files._action_groups.pop()
    parser_datasets_files_optional.add_argument("dataset", nargs="?", default=None, help=Help.param_dataset)
    parser_datasets_files_optional.add_argument(
        "-d", "--dataset", dest="dataset_opt", required=False, help=argparse.SUPPRESS
    )
    _add_output_format_args(parser_datasets_files_optional)
    parser_datasets_files_optional.add_argument(
        "--page-token", dest="page_token", required=False, help=Help.param_page_token
    )
    parser_datasets_files_optional.add_argument(
        "--page-size", dest="page_size", required=False, default=20, type=int, help=Help.param_page_size
    )
    parser_datasets_files._action_groups.append(parser_datasets_files_optional)
    parser_datasets_files.set_defaults(func=api.dataset_list_files_cli)

    # Datasets download
    parser_datasets_download = subparsers_datasets.add_parser(
        "download", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_datasets_download
    )
    parser_datasets_download_optional = parser_datasets_download._action_groups.pop()
    parser_datasets_download_optional.add_argument("dataset", nargs="?", default=None, help=Help.param_dataset)
    parser_datasets_download_optional.add_argument(
        "-d", "--dataset", dest="dataset_opt", required=False, help=argparse.SUPPRESS
    )
    parser_datasets_download_optional.add_argument(
        "-f", "--file", dest="file_name", required=False, help=Help.param_dataset_file
    )
    parser_datasets_download_optional.add_argument(
        "-p", "--path", dest="path", required=False, help=Help.param_downfolder
    )
    parser_datasets_download_optional.add_argument(
        "-w", "--wp", dest="path", action="store_const", const=".", required=False, help=Help.param_wp
    )
    parser_datasets_download_optional.add_argument("--unzip", dest="unzip", action="store_true", help=Help.param_unzip)
    parser_datasets_download_optional.add_argument(
        "-o", "--force", dest="force", action="store_true", help=Help.param_force
    )
    parser_datasets_download_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_datasets_download._action_groups.append(parser_datasets_download_optional)
    parser_datasets_download.set_defaults(func=api.dataset_download_cli)

    # Datasets create
    parser_datasets_create = subparsers_datasets.add_parser(
        "create", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_datasets_new
    )
    parser_datasets_create_optional = parser_datasets_create._action_groups.pop()
    parser_datasets_create_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_dataset_upfile
    )
    parser_datasets_create_optional.add_argument(
        "-u", "--public", dest="public", action="store_true", help=Help.param_public
    )
    parser_datasets_create_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_datasets_create_optional.add_argument(
        "-t", "--keep-tabular", dest="convert_to_csv", action="store_false", help=Help.param_keep_tabular
    )
    parser_datasets_create_optional.add_argument(
        "-r", "--dir-mode", dest="dir_mode", choices=["skip", "zip", "tar"], default="skip", help=Help.param_dir_mode
    )
    parser_datasets_create._action_groups.append(parser_datasets_create_optional)
    parser_datasets_create.set_defaults(func=api.dataset_create_new_cli)

    # Datasets update
    parser_datasets_version = subparsers_datasets.add_parser(
        "version", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_datasets_new_version
    )
    parser_datasets_version_optional = parser_datasets_version._action_groups.pop()
    parser_datasets_version_required = parser_datasets_version.add_argument_group("required arguments")
    parser_datasets_version_required.add_argument(
        "-m", "--message", dest="version_notes", required=True, help=Help.param_dataset_version_notes
    )
    parser_datasets_version_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_dataset_upfile
    )
    parser_datasets_version_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_datasets_version_optional.add_argument(
        "-t", "--keep-tabular", dest="convert_to_csv", action="store_false", help=Help.param_keep_tabular
    )
    parser_datasets_version_optional.add_argument(
        "-r", "--dir-mode", dest="dir_mode", choices=["skip", "zip", "tar"], default="skip", help=Help.param_dir_mode
    )
    parser_datasets_version_optional.add_argument(
        "-d",
        "--delete-old-versions",
        dest="delete_old_versions",
        action="store_true",
        help=Help.param_delete_old_version,
    )
    parser_datasets_version._action_groups.append(parser_datasets_version_optional)
    parser_datasets_version.set_defaults(func=api.dataset_create_version_cli)

    # Datasets init
    parser_datasets_init = subparsers_datasets.add_parser(
        "init", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_datasets_init
    )
    parser_datasets_init_optional = parser_datasets_init._action_groups.pop()
    parser_datasets_init_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_dataset_upfile
    )
    parser_datasets_init._action_groups.append(parser_datasets_init_optional)
    parser_datasets_init.set_defaults(func=api.dataset_initialize_cli)

    # Datasets metadata
    parser_datasets_metadata = subparsers_datasets.add_parser(
        "metadata", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_datasets_metadata
    )
    parser_datasets_metadata_optional = parser_datasets_metadata._action_groups.pop()
    parser_datasets_metadata_optional.add_argument("dataset", nargs="?", default=None, help=Help.param_dataset)
    parser_datasets_metadata_optional.add_argument(
        "-d", "--dataset", dest="dataset_opt", required=False, help=argparse.SUPPRESS
    )
    parser_datasets_metadata_optional.add_argument(
        "--update", dest="update", action="store_true", help=Help.param_dataset_metadata_update
    )
    parser_datasets_metadata_optional.add_argument("-p", "--path", dest="path", help=Help.param_dataset_metadata_dir)
    parser_datasets_metadata._action_groups.append(parser_datasets_metadata_optional)
    parser_datasets_metadata.set_defaults(func=api.dataset_metadata_cli)

    # Datasets status
    parser_datasets_status = subparsers_datasets.add_parser(
        "status", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_datasets_status
    )
    parser_datasets_status_optional = parser_datasets_status._action_groups.pop()
    parser_datasets_status_optional.add_argument("dataset", nargs="?", default=None, help=Help.param_dataset)
    parser_datasets_status_optional.add_argument(
        "-d", "--dataset", dest="dataset_opt", required=False, help=argparse.SUPPRESS
    )
    parser_datasets_status_optional.add_argument(
        "--format",
        dest="format",
        required=False,
        default=None,
        help=Help.param_dataset_status_format,
    )
    parser_datasets_status._action_groups.append(parser_datasets_status_optional)
    parser_datasets_status.set_defaults(func=api.dataset_status_cli)

    shared_topics = _get_shared_topics_parser()

    # Datasets discussion topics
    parser_datasets_topics = subparsers_datasets.add_parser(
        "topics",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_datasets_topics,
        parents=[shared_topics],
    )
    subparsers_datasets_topics = parser_datasets_topics.add_subparsers(title="commands", dest="command")
    subparsers_datasets_topics.choices = Help.entity_topics_choices

    # Default action: list topics (when no subcommand given)
    parser_datasets_topics.set_defaults(func=api.dataset_list_topics_cli)

    # Datasets topics list (explicit)
    parser_datasets_topics_list = subparsers_datasets_topics.add_parser(
        "list",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_datasets_topics,
        parents=[shared_topics],
    )
    parser_datasets_topics_list_optional = parser_datasets_topics_list._action_groups.pop()
    parser_datasets_topics_list_optional.add_argument(
        "entity_ref", metavar="dataset", nargs="?", default=None, help=Help.param_dataset
    )
    parser_datasets_topics_list_optional.add_argument(
        "--sort-by",
        dest="sort_by",
        required=False,
        help="Sort order. One of: " + ", ".join(KaggleApi.valid_forum_topic_sort_by),
    )
    parser_datasets_topics_list_optional.add_argument(
        "-s", "--search", dest="search", required=False, help=Help.param_search
    )
    parser_datasets_topics_list._action_groups.append(parser_datasets_topics_list_optional)
    parser_datasets_topics_list.set_defaults(func=api.dataset_list_topics_cli)

    # Datasets topics show
    parser_datasets_topics_show = subparsers_datasets_topics.add_parser(
        "show",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_entity_topics_show,
        parents=[shared_topics],
    )
    parser_datasets_topics_show_optional = parser_datasets_topics_show._action_groups.pop()
    parser_datasets_topics_show_optional.add_argument("topic_ref", help=Help.param_topic_ref)
    parser_datasets_topics_show_optional.add_argument(
        "topic_id_arg",
        nargs="?",
        default=None,
        type=int,
        help="Topic ID (when using two-arg form: <dataset> <topic-id>)",
    )
    parser_datasets_topics_show._action_groups.append(parser_datasets_topics_show_optional)
    parser_datasets_topics_show.set_defaults(func=api.forums_topic_show_cli)

