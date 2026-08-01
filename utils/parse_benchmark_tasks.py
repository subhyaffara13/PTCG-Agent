
def parse_benchmark_tasks(subparsers) -> None:
    parser_tasks = subparsers.add_parser(
        "tasks", formatter_class=argparse.RawTextHelpFormatter, help=Help.group_benchmarks_tasks, aliases=["t"]
    )
    subparsers_tasks = parser_tasks.add_subparsers(title="commands", dest="command")
    subparsers_tasks.required = True
    subparsers_tasks.choices = Help.benchmarks_tasks_choices

    # push
    parser_push = subparsers_tasks.add_parser(
        "push",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_benchmarks_tasks_push,
        usage="%(prog)s [-h] task -f FILE [--wait [WAIT]] [--poll-interval POLL_INTERVAL] [-v] [-d DATASET]",
    )
    parser_push_optional = parser_push._action_groups.pop()
    parser_push_required = parser_push.add_argument_group("required arguments")
    parser_push_required.add_argument("task", help=Help.param_benchmarks_task)
    parser_push_required.add_argument("-f", "--file", dest="file", required=True, help=Help.param_benchmarks_file)
    parser_push_optional.add_argument(
        "--wait",
        dest="wait",
        type=int,
        nargs="?",
        const=0,
        default=None,
        required=False,
        help=Help.param_benchmarks_wait,
    )
    parser_push_optional.add_argument(
        "--poll-interval",
        dest="poll_interval",
        type=int,
        default=60,
        required=False,
        help=Help.param_benchmarks_poll_interval,
    )
    parser_push_optional.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help=Help.param_benchmarks_verbose,
    )
    parser_push_optional.add_argument(
        "-d",
        "--kaggle-dataset",
        dest="kaggle_datasets",
        action="append",
        required=False,
        help=Help.param_benchmarks_kaggle_dataset,
    )
    parser_push._action_groups.append(parser_push_optional)
    parser_push.set_defaults(func=api.benchmarks_tasks_push_cli)

    # run
    parser_run = subparsers_tasks.add_parser(
        "run",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_benchmarks_tasks_run,
        usage="%(prog)s [-h] task [-m MODEL] [--wait [WAIT]] [--poll-interval POLL_INTERVAL] [-v]",
    )
    parser_run_optional = parser_run._action_groups.pop()
    parser_run_required = parser_run.add_argument_group("required arguments")
    parser_run_required.add_argument("task", help=Help.param_benchmarks_task)
    parser_run_optional.add_argument(
        "-m", "--model", dest="model", action="append", required=False, help=Help.param_benchmarks_model
    )
    parser_run_optional.add_argument(
        "--wait",
        dest="wait",
        type=int,
        nargs="?",
        const=0,
        default=None,
        required=False,
        help=Help.param_benchmarks_wait,
    )
    parser_run_optional.add_argument(
        "--poll-interval",
        dest="poll_interval",
        type=int,
        default=60,
        required=False,
        help=Help.param_benchmarks_poll_interval,
    )
    parser_run_optional.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        help=Help.param_benchmarks_verbose,
    )
    parser_run._action_groups.append(parser_run_optional)
    parser_run.set_defaults(func=api.benchmarks_tasks_run_cli)

    # list
    parser_list = subparsers_tasks.add_parser(
        "list", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_benchmarks_tasks_list
    )
    parser_list_optional = parser_list._action_groups.pop()
    parser_list_optional.add_argument(
        "--name-regex", dest="name_regex", required=False, help=Help.param_benchmarks_name_regex
    )
    parser_list_optional.add_argument("--status", dest="status", required=False, help=Help.param_benchmarks_status)
    parser_list_optional.add_argument(
        "--page-size", dest="page_size", required=False, type=int, help=Help.param_benchmarks_list_page_size
    )
    parser_list_optional.add_argument(
        "--all", dest="show_all", required=False, action="store_true", help=Help.param_benchmarks_list_all
    )
    parser_list._action_groups.append(parser_list_optional)
    parser_list.set_defaults(func=api.benchmarks_tasks_list_cli)

    # status
    parser_status = subparsers_tasks.add_parser(
        "status", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_benchmarks_tasks_status
    )
    parser_status_optional = parser_status._action_groups.pop()
    parser_status_optional.add_argument("task", help=Help.param_benchmarks_task)
    parser_status_optional.add_argument(
        "-m", "--model", dest="model", action="append", required=False, help=Help.param_benchmarks_model
    )
    parser_status._action_groups.append(parser_status_optional)
    parser_status.set_defaults(func=api.benchmarks_tasks_status_cli)

    # download
    parser_download = subparsers_tasks.add_parser(
        "download", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_benchmarks_tasks_download
    )
    parser_download_optional = parser_download._action_groups.pop()
    parser_download_optional.add_argument("task", help=Help.param_benchmarks_task)
    parser_download_optional.add_argument(
        "-m", "--model", dest="model", action="append", required=False, help=Help.param_benchmarks_model
    )
    parser_download_optional.add_argument(
        "-o", "--output", dest="output", required=False, help=Help.param_benchmarks_output
    )
    parser_download_optional.add_argument(
        "-s",
        "--include-source",
        dest="include_source",
        action="store_true",
        required=False,
        help=Help.param_benchmarks_include_source,
    )
    parser_download_optional.add_argument(
        "-f",
        "--force",
        dest="force",
        action="store_true",
        required=False,
        help=Help.param_benchmarks_force,
    )
    parser_download._action_groups.append(parser_download_optional)
    parser_download.set_defaults(func=api.benchmarks_tasks_download_cli)

    # log / logs
    parser_log = subparsers_tasks.add_parser(
        "log",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_benchmarks_tasks_log,
        aliases=["logs"],
    )
    parser_log_optional = parser_log._action_groups.pop()
    parser_log_optional.add_argument("task", help=Help.param_benchmarks_task)
    parser_log_optional.add_argument(
        "-m",
        "--model",
        dest="model",
        action="append",
        required=False,
        help=Help.param_benchmarks_model,
    )
    parser_log._action_groups.append(parser_log_optional)
    parser_log.set_defaults(func=api.benchmarks_tasks_log_cli)

    # models
    parser_models = subparsers_tasks.add_parser(
        "models", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_benchmarks_tasks_models
    )
    parser_models.set_defaults(func=api.benchmarks_tasks_models_cli)

    # delete
    parser_delete = subparsers_tasks.add_parser(
        "delete", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_benchmarks_tasks_delete
    )
    parser_delete_optional = parser_delete._action_groups.pop()
    parser_delete_optional.add_argument("task", help=Help.param_benchmarks_task)
    parser_delete_optional.add_argument(
        "-y", "--yes", dest="no_confirm", action="store_true", required=False, help=Help.param_yes
    )
    parser_delete._action_groups.append(parser_delete_optional)
    parser_delete.set_defaults(func=api.benchmarks_tasks_delete_cli)

    # publish
    parser_publish = subparsers_tasks.add_parser(
        "publish",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_benchmarks_tasks_publish,
    )
    parser_publish_optional = parser_publish._action_groups.pop()
    parser_publish_optional.add_argument("task", help=Help.param_benchmarks_task)
    parser_publish_optional.add_argument(
        "--no-publish-backing-notebook",
        dest="publish_backing_notebook",
        action="store_false",
        required=False,
        help=Help.param_benchmarks_no_publish_backing_notebook,
    )
    parser_publish._action_groups.append(parser_publish_optional)
    parser_publish.set_defaults(func=api.benchmarks_tasks_publish_cli)

