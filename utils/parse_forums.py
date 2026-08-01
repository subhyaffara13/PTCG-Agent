
def parse_forums(subparsers) -> None:
    parser_forums = subparsers.add_parser(
        "forums", formatter_class=argparse.RawTextHelpFormatter, help=Help.group_forums, aliases=["f"]
    )
    subparsers_forums = parser_forums.add_subparsers(title="commands", dest="command")
    subparsers_forums.choices = Help.forums_choices

    # Default action: list forums (when no subcommand given)
    parser_forums.set_defaults(func=api.forums_list_cli)

    # Forums list (explicit)
    parser_forums_list = subparsers_forums.add_parser(
        "list", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_forums_list
    )
    parser_forums_list_optional = parser_forums_list._action_groups.pop()
    _add_output_format_args(parser_forums_list_optional)
    parser_forums_list_optional.add_argument("-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet)
    parser_forums_list._action_groups.append(parser_forums_list_optional)
    parser_forums_list.set_defaults(func=api.forums_list_cli)

    shared_topics = _get_shared_topics_parser()

    # Forums topics
    parser_forums_topics = subparsers_forums.add_parser(
        "topics",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_forums_topics,
        parents=[shared_topics],
    )
    subparsers_forums_topics = parser_forums_topics.add_subparsers(title="commands", dest="command")
    subparsers_forums_topics.choices = Help.forums_topics_choices

    # Default action: list topics (when no subcommand given)
    parser_forums_topics.set_defaults(func=api.forums_list_topics_cli)

    # Forums topics list (explicit)
    parser_forums_topics_list = subparsers_forums_topics.add_parser(
        "list",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_forums_topics,
        parents=[shared_topics],
    )
    parser_forums_topics_list_optional = parser_forums_topics_list._action_groups.pop()
    parser_forums_topics_list_optional.add_argument("forum", nargs="?", default=None, help=Help.param_forum)
    parser_forums_topics_list_optional.add_argument(
        "--sort-by",
        dest="sort_by",
        required=False,
        help="Sort order. One of: " + ", ".join(KaggleApi.valid_forum_topic_sort_by),
    )
    parser_forums_topics_list_optional.add_argument(
        "-s", "--search", dest="search", required=False, help=Help.param_search
    )
    parser_forums_topics_list_optional.add_argument(
        "--category",
        dest="category",
        required=False,
        help="Filter by category. One of: " + ", ".join(KaggleApi.valid_forum_topic_categories),
    )
    parser_forums_topics_list_optional.add_argument(
        "--group",
        dest="group",
        required=False,
        help="Filter by group. One of: " + ", ".join(KaggleApi.valid_forum_topic_groups),
    )
    parser_forums_topics_list._action_groups.append(parser_forums_topics_list_optional)
    parser_forums_topics_list.set_defaults(func=api.forums_list_topics_cli)

    # Forums topics show
    parser_forums_topics_show = subparsers_forums_topics.add_parser(
        "show",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_forums_topics_show,
        parents=[shared_topics],
    )
    parser_forums_topics_show_optional = parser_forums_topics_show._action_groups.pop()
    parser_forums_topics_show_optional.add_argument("topic_ref", help=Help.param_topic_ref)
    parser_forums_topics_show_optional.add_argument(
        "topic_id_arg",
        nargs="?",
        default=None,
        type=int,
        help="Topic ID (when using two-arg form: <forum-name> <topic-id>)",
    )
    parser_forums_topics_show._action_groups.append(parser_forums_topics_show_optional)
    parser_forums_topics_show.set_defaults(func=api.forums_topic_show_cli)

