
def parse_kernels(subparsers) -> None:
    parser_kernels = subparsers.add_parser(
        "kernels", formatter_class=argparse.RawTextHelpFormatter, help=Help.group_kernels, aliases=["k"]
    )
    subparsers_kernels = parser_kernels.add_subparsers(title="commands", dest="command")
    subparsers_kernels.required = True
    subparsers_kernels.choices = Help.kernels_choices

    # Kernels list/search
    parser_kernels_list = subparsers_kernels.add_parser(
        "list", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_kernels_list
    )
    parser_kernels_list_optional = parser_kernels_list._action_groups.pop()
    parser_kernels_list_optional.add_argument("-m", "--mine", dest="mine", action="store_true", help=Help.param_mine)
    parser_kernels_list_optional.add_argument("-p", "--page", dest="page", default=1, type=int, help=Help.param_page)
    parser_kernels_list_optional.add_argument(
        "--page-size", dest="page_size", default=20, type=int, help=Help.param_page_size
    )
    parser_kernels_list_optional.add_argument("-s", "--search", dest="search", help=Help.param_search)
    _add_output_format_args(parser_kernels_list_optional)
    parser_kernels_list_optional.add_argument("--parent", dest="parent", required=False, help=Help.param_kernel_parent)
    parser_kernels_list_optional.add_argument(
        "--competition", dest="competition", required=False, help=Help.param_kernel_competition
    )
    parser_kernels_list_optional.add_argument(
        "--dataset", dest="dataset", required=False, help=Help.param_kernel_dataset
    )
    parser_kernels_list_optional.add_argument("--user", dest="user", required=False, help=Help.param_kernel_user)
    parser_kernels_list_optional.add_argument(
        "--language", dest="language", required=False, help=Help.param_kernel_language
    )
    parser_kernels_list_optional.add_argument(
        "--kernel-type", dest="kernel_type", required=False, help=Help.param_kernel_type
    )
    parser_kernels_list_optional.add_argument(
        "--output-type", dest="output_type", required=False, help=Help.param_kernel_output_type
    )
    parser_kernels_list_optional.add_argument(
        "--sort-by", dest="sort_by", required=False, help=Help.param_kernel_sort_by
    )
    parser_kernels_list._action_groups.append(parser_kernels_list_optional)
    parser_kernels_list.set_defaults(func=api.kernels_list_cli)

    # Kernels file list
    parser_kernels_files = subparsers_kernels.add_parser(
        "files", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_kernels_files
    )
    parser_kernels_files_optional = parser_kernels_files._action_groups.pop()
    parser_kernels_files_optional.add_argument("kernel", nargs="?", default=None, help=Help.param_kernel)
    parser_kernels_files_optional.add_argument(
        "-k", "--kernel", dest="kernel_opt", required=False, help=argparse.SUPPRESS
    )
    _add_output_format_args(parser_kernels_files_optional)
    parser_kernels_files_optional.add_argument("--page-token", dest="page_token", help=Help.param_page_token)
    parser_kernels_files_optional.add_argument(
        "--page-size", dest="page_size", default=20, type=int, help=Help.param_page_size
    )
    parser_kernels_files._action_groups.append(parser_kernels_files_optional)
    parser_kernels_files.set_defaults(func=api.kernels_list_files_cli)

    # Kernels init
    parser_kernels_init = subparsers_kernels.add_parser(
        "init", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_kernels_init
    )
    parser_kernels_init_optional = parser_kernels_init._action_groups.pop()
    parser_kernels_init_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_kernel_upfile
    )
    parser_kernels_init._action_groups.append(parser_kernels_init_optional)
    parser_kernels_init.set_defaults(func=api.kernels_initialize_cli)

    # Kernels push
    parser_kernels_push = subparsers_kernels.add_parser(
        "push", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_kernels_push, aliases=["update"]
    )
    parser_kernels_push_optional = parser_kernels_push._action_groups.pop()
    parser_kernels_push_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_kernel_upfile
    )
    parser_kernels_push_optional.add_argument(
        "-t", "--timeout", type=int, dest="timeout", help=Help.param_kernel_timeout
    )
    parser_kernels_push_optional.add_argument("--accelerator", dest="acc", help=Help.param_kernel_acc)
    parser_kernels_push._action_groups.append(parser_kernels_push_optional)
    parser_kernels_push.set_defaults(func=api.kernels_push_cli)

    # Kernels pull
    parser_kernels_pull = subparsers_kernels.add_parser(
        "pull",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_kernels_pull,
        aliases=["get"],
    )
    parser_kernels_pull_optional = parser_kernels_pull._action_groups.pop()
    parser_kernels_pull_optional.add_argument("kernel", nargs="?", default=None, help=Help.param_kernel)
    parser_kernels_pull_optional.add_argument("-k", "--kernel", dest="kernel", required=False, help=argparse.SUPPRESS)
    parser_kernels_pull_optional.add_argument("-p", "--path", dest="path", required=False, help=Help.param_downfolder)
    parser_kernels_pull_optional.add_argument(
        "-w", "--wp", dest="path", action="store_const", const=".", required=False, help=Help.param_wp
    )
    parser_kernels_pull_optional.add_argument(
        "-m", "--metadata", dest="metadata", action="store_true", help=Help.param_kernel_pull_metadata
    )
    parser_kernels_pull._action_groups.append(parser_kernels_pull_optional)
    parser_kernels_pull.set_defaults(func=api.kernels_pull_cli)

    # Kernels output
    parser_kernels_output = subparsers_kernels.add_parser(
        "output", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_kernels_output
    )
    parser_kernels_output_optional = parser_kernels_output._action_groups.pop()
    parser_kernels_output_optional.add_argument("kernel", nargs="?", default=None, help=Help.param_kernel)
    parser_kernels_output_optional.add_argument(
        "-k", "--kernel", dest="kernel_opt", required=False, help=argparse.SUPPRESS
    )
    parser_kernels_output_optional.add_argument("-p", "--path", dest="path", required=False, help=Help.param_downfolder)
    parser_kernels_output_optional.add_argument(
        "-w", "--wp", dest="path", action="store_const", const=".", required=False, help=Help.param_wp
    )
    parser_kernels_output_optional.add_argument(
        "-o", "--force", dest="force", action="store_true", required=False, help=Help.param_force
    )
    parser_kernels_output_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", required=False, help=Help.param_quiet
    )
    parser_kernels_output_optional.add_argument(
        "--file-pattern", dest="file_pattern", required=False, help=Help.param_kernel_output_file_pattern
    )
    parser_kernels_output_optional.add_argument(
        "--page-size", dest="page_size", default=20, type=int, required=False, help=Help.param_page_size
    )
    parser_kernels_output_optional.add_argument(
        "--page-token", dest="page_token", required=False, help=Help.param_page_token
    )
    parser_kernels_output._action_groups.append(parser_kernels_output_optional)
    parser_kernels_output.set_defaults(func=api.kernels_output_cli)

    # Kernels status
    parser_kernels_status = subparsers_kernels.add_parser(
        "status", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_kernels_status
    )
    parser_kernels_status_optional = parser_kernels_status._action_groups.pop()
    parser_kernels_status_optional.add_argument("kernel", nargs="?", default=None, help=Help.param_kernel)
    parser_kernels_status_optional.add_argument(
        "-k", "--kernel", dest="kernel_opt", required=False, help=argparse.SUPPRESS
    )
    parser_kernels_status._action_groups.append(parser_kernels_status_optional)
    parser_kernels_status.set_defaults(func=api.kernels_status_cli)

    # Kernels logs
    parser_kernels_logs = subparsers_kernels.add_parser(
        "logs", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_kernels_logs
    )
    parser_kernels_logs_optional = parser_kernels_logs._action_groups.pop()
    parser_kernels_logs_optional.add_argument("kernel", nargs="?", default=None, help=Help.param_kernel)
    parser_kernels_logs_optional.add_argument(
        "-k", "--kernel", dest="kernel_opt", required=False, help=argparse.SUPPRESS
    )
    parser_kernels_logs_optional.add_argument(
        "-f", "--follow", dest="follow", action="store_true", required=False, help=Help.param_kernel_logs_follow
    )
    parser_kernels_logs_optional.add_argument(
        "--interval", dest="interval", default=5, type=int, required=False, help=Help.param_kernel_logs_interval
    )
    parser_kernels_logs._action_groups.append(parser_kernels_logs_optional)
    parser_kernels_logs.set_defaults(func=api.kernels_logs_cli)

    # Kernels delete
    parser_kernels_delete = subparsers_kernels.add_parser(
        "delete", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_kernels_delete
    )
    parser_kernels_delete_optional = parser_kernels_delete._action_groups.pop()
    parser_kernels_delete_optional.add_argument("kernel", help=Help.param_kernel)
    parser_kernels_delete_optional.add_argument(
        "-y", "--yes", dest="no_confirm", action="store_true", help=Help.param_yes
    )
    parser_kernels_delete._action_groups.append(parser_kernels_delete_optional)
    parser_kernels_delete.set_defaults(func=api.kernels_delete_cli)

    shared_topics = _get_shared_topics_parser()

    # Kernels discussion topics
    parser_kernels_topics = subparsers_kernels.add_parser(
        "topics",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_kernels_topics,
        parents=[shared_topics],
    )
    subparsers_kernels_topics = parser_kernels_topics.add_subparsers(title="commands", dest="command")
    subparsers_kernels_topics.choices = Help.entity_topics_choices

    # Default action: list topics (when no subcommand given)
    parser_kernels_topics.set_defaults(func=api.kernel_list_topics_cli)

    # Kernels topics list (explicit)
    parser_kernels_topics_list = subparsers_kernels_topics.add_parser(
        "list",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_kernels_topics,
        parents=[shared_topics],
    )
    parser_kernels_topics_list_optional = parser_kernels_topics_list._action_groups.pop()
    parser_kernels_topics_list_optional.add_argument(
        "entity_ref", metavar="kernel", nargs="?", default=None, help=Help.param_kernel
    )
    parser_kernels_topics_list_optional.add_argument(
        "--sort-by",
        dest="sort_by",
        required=False,
        help="Sort order. One of: " + ", ".join(KaggleApi.valid_forum_topic_sort_by),
    )
    parser_kernels_topics_list_optional.add_argument(
        "-s", "--search", dest="search", required=False, help=Help.param_search
    )
    parser_kernels_topics_list._action_groups.append(parser_kernels_topics_list_optional)
    parser_kernels_topics_list.set_defaults(func=api.kernel_list_topics_cli)

    # Kernels topics show
    parser_kernels_topics_show = subparsers_kernels_topics.add_parser(
        "show",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_entity_topics_show,
        parents=[shared_topics],
    )
    parser_kernels_topics_show_optional = parser_kernels_topics_show._action_groups.pop()
    parser_kernels_topics_show_optional.add_argument("topic_ref", help=Help.param_topic_ref)
    parser_kernels_topics_show_optional.add_argument(
        "topic_id_arg",
        nargs="?",
        default=None,
        type=int,
        help="Topic ID (when using two-arg form: <kernel> <topic-id>)",
    )
    parser_kernels_topics_show._action_groups.append(parser_kernels_topics_show_optional)
    parser_kernels_topics_show.set_defaults(func=api.forums_topic_show_cli)

