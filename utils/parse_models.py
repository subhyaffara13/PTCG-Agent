
def parse_models(subparsers) -> None:
    parser_models = subparsers.add_parser(
        "models", formatter_class=argparse.RawTextHelpFormatter, help=Help.group_models, aliases=["m"]
    )

    subparsers_models = parser_models.add_subparsers(title="commands", dest="command")
    subparsers_models.required = True
    subparsers_models.choices = Help.models_choices

    # Models Instances.
    parse_model_instances(subparsers_models)

    # Models get
    parser_models_get = subparsers_models.add_parser(
        "get", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_models_get
    )
    parser_models_get_optional = parser_models_get._action_groups.pop()
    parser_models_get_optional.add_argument("model", help=Help.param_model)
    parser_models_get_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_model_downfile
    )
    parser_models_get._action_groups.append(parser_models_get_optional)
    parser_models_get.set_defaults(func=api.model_get_cli)

    # Models list
    parser_models_list = subparsers_models.add_parser(
        "list", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_models_list
    )
    parser_models_list_optional = parser_models_list._action_groups.pop()
    parser_models_list.add_argument("--sort-by", dest="sort_by", required=False, help=Help.param_model_sort_by)
    parser_models_list.add_argument("-s", "--search", dest="search", required=False, help=Help.param_search)
    parser_models_list.add_argument("--owner", dest="owner", required=False, help=Help.param_model_owner)
    parser_models_list.add_argument("--page-size", dest="page_size", default=20, type=int, help=Help.param_page_size)
    parser_models_list.add_argument("--page-token", dest="page_token", required=False, help=Help.param_page_token)
    _add_output_format_args(parser_models_list)
    parser_models_list._action_groups.append(parser_models_list_optional)
    parser_models_list.set_defaults(func=api.model_list_cli)

    # Models init
    parser_models_init = subparsers_models.add_parser(
        "init", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_models_init
    )
    parser_models_init_optional = parser_models_init._action_groups.pop()
    parser_models_init_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_model_upfile
    )
    parser_models_init._action_groups.append(parser_models_init_optional)
    parser_models_init.set_defaults(func=api.model_initialize_cli)

    # Models create
    parser_models_create = subparsers_models.add_parser(
        "create", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_models_new
    )
    parser_models_create_optional = parser_models_create._action_groups.pop()
    parser_models_create_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_model_upfile
    )
    parser_models_create._action_groups.append(parser_models_create_optional)
    parser_models_create.set_defaults(func=api.model_create_new_cli)

    # Models delete
    parser_models_delete = subparsers_models.add_parser(
        "delete", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_models_delete
    )
    parser_models_delete_optional = parser_models_delete._action_groups.pop()
    parser_models_delete_optional.add_argument("model", help=Help.param_model)
    parser_models_delete_optional.add_argument(
        "-y", "--yes", dest="no_confirm", action="store_true", help=Help.param_yes
    )
    parser_models_delete._action_groups.append(parser_models_delete_optional)
    parser_models_delete.set_defaults(func=api.model_delete_cli)

    # Models update
    parser_models_update = subparsers_models.add_parser(
        "update", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_models_update
    )
    parser_models_update_optional = parser_models_update._action_groups.pop()
    parser_models_update_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_model_upfile
    )
    parser_models_update._action_groups.append(parser_models_update_optional)
    parser_models_update.set_defaults(func=api.model_update_cli)

    shared_topics = _get_shared_topics_parser()

    # Models discussion topics
    parser_models_topics = subparsers_models.add_parser(
        "topics",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_models_topics,
        parents=[shared_topics],
    )
    subparsers_models_topics = parser_models_topics.add_subparsers(title="commands", dest="command")
    subparsers_models_topics.choices = Help.entity_topics_choices

    # Default action: list topics (when no subcommand given)
    parser_models_topics.set_defaults(func=api.model_list_topics_cli)

    # Models topics list (explicit)
    parser_models_topics_list = subparsers_models_topics.add_parser(
        "list",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_models_topics,
        parents=[shared_topics],
    )
    parser_models_topics_list_optional = parser_models_topics_list._action_groups.pop()
    parser_models_topics_list_optional.add_argument(
        "entity_ref", metavar="model", nargs="?", default=None, help=Help.param_model
    )
    parser_models_topics_list_optional.add_argument(
        "--sort-by",
        dest="sort_by",
        required=False,
        help="Sort order. One of: " + ", ".join(KaggleApi.valid_forum_topic_sort_by),
    )
    parser_models_topics_list_optional.add_argument(
        "-s", "--search", dest="search", required=False, help=Help.param_search
    )
    parser_models_topics_list._action_groups.append(parser_models_topics_list_optional)
    parser_models_topics_list.set_defaults(func=api.model_list_topics_cli)

    # Models topics show
    parser_models_topics_show = subparsers_models_topics.add_parser(
        "show",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_entity_topics_show,
        parents=[shared_topics],
    )
    parser_models_topics_show_optional = parser_models_topics_show._action_groups.pop()
    parser_models_topics_show_optional.add_argument("topic_ref", help=Help.param_topic_ref)
    parser_models_topics_show_optional.add_argument(
        "topic_id_arg",
        nargs="?",
        default=None,
        type=int,
        help="Topic ID (when using two-arg form: <model> <topic-id>)",
    )
    parser_models_topics_show._action_groups.append(parser_models_topics_show_optional)
    parser_models_topics_show.set_defaults(func=api.forums_topic_show_cli)

