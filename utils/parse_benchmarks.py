
def parse_benchmarks(subparsers) -> None:
    parser_benchmarks = subparsers.add_parser(
        "benchmarks", formatter_class=argparse.RawTextHelpFormatter, help=Help.group_benchmarks, aliases=["b"]
    )
    subparsers_benchmarks = parser_benchmarks.add_subparsers(title="commands", dest="command")
    subparsers_benchmarks.required = True
    subparsers_benchmarks.choices = Help.benchmarks_choices

    parse_benchmark_tasks(subparsers_benchmarks)
    parse_benchmarks_auth(subparsers_benchmarks)
    parse_benchmarks_init(subparsers_benchmarks)

    shared_topics = _get_shared_topics_parser()

    # Benchmarks discussion topics
    parser_benchmarks_topics = subparsers_benchmarks.add_parser(
        "topics",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_benchmarks_topics,
        parents=[shared_topics],
    )
    subparsers_benchmarks_topics = parser_benchmarks_topics.add_subparsers(title="commands", dest="command")
    subparsers_benchmarks_topics.choices = Help.entity_topics_choices

    # Default action: list topics (when no subcommand given)
    parser_benchmarks_topics.set_defaults(func=api.benchmark_list_topics_cli)

    # Benchmarks topics list (explicit)
    parser_benchmarks_topics_list = subparsers_benchmarks_topics.add_parser(
        "list",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_benchmarks_topics,
        parents=[shared_topics],
    )
    parser_benchmarks_topics_list_optional = parser_benchmarks_topics_list._action_groups.pop()
    parser_benchmarks_topics_list_optional.add_argument(
        "entity_ref", metavar="benchmark", nargs="?", default=None, help=Help.param_benchmark
    )
    parser_benchmarks_topics_list_optional.add_argument(
        "--sort-by",
        dest="sort_by",
        required=False,
        help="Sort order. One of: " + ", ".join(KaggleApi.valid_forum_topic_sort_by),
    )
    parser_benchmarks_topics_list_optional.add_argument(
        "-s", "--search", dest="search", required=False, help=Help.param_search
    )
    parser_benchmarks_topics_list._action_groups.append(parser_benchmarks_topics_list_optional)
    parser_benchmarks_topics_list.set_defaults(func=api.benchmark_list_topics_cli)

    # Benchmarks topics show
    parser_benchmarks_topics_show = subparsers_benchmarks_topics.add_parser(
        "show",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_entity_topics_show,
        parents=[shared_topics],
    )
    parser_benchmarks_topics_show_optional = parser_benchmarks_topics_show._action_groups.pop()
    parser_benchmarks_topics_show_optional.add_argument("topic_ref", help=Help.param_topic_ref)
    parser_benchmarks_topics_show_optional.add_argument(
        "topic_id_arg",
        nargs="?",
        default=None,
        type=int,
        help="Topic ID (when using two-arg form: <benchmark> <topic-id>)",
    )
    parser_benchmarks_topics_show._action_groups.append(parser_benchmarks_topics_show_optional)
    parser_benchmarks_topics_show.set_defaults(func=api.forums_topic_show_cli)

