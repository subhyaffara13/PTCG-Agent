
def parse_model_instances(subparsers) -> None:
    parser_model_instances = subparsers.add_parser(
        "instances",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.group_model_instances,
        aliases=[
            "i",
            "variations",
            "v",
        ],  # Is 'kaggle m v v ...' too confusing? kaggle m v n ... ? No backcompat since the old alias didn't work.
    )

    subparsers_model_instances = parser_model_instances.add_subparsers(title="commands", dest="command")
    subparsers_model_instances.required = True
    subparsers_model_instances.choices = Help.model_instances_choices

    # Models Instances Versions.
    parse_model_instance_versions(subparsers_model_instances)

    # Models Instances get
    parser_model_instance_get = subparsers_model_instances.add_parser(
        "get", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instances_get
    )
    parser_model_instance_get_optional = parser_model_instance_get._action_groups.pop()
    parser_model_instance_get_optional.add_argument("model_instance", help=Help.param_model_instance)
    parser_model_instance_get_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_model_instance_downfile
    )
    parser_model_instance_get._action_groups.append(parser_model_instance_get_optional)
    parser_model_instance_get.set_defaults(func=api.model_instance_get_cli)

    # Model Instances init
    parser_model_instances_init = subparsers_model_instances.add_parser(
        "init", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instances_init
    )
    parser_model_instances_init_optional = parser_model_instances_init._action_groups.pop()
    parser_model_instances_init_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_model_instance_upfile
    )
    parser_model_instances_init._action_groups.append(parser_model_instances_init_optional)
    parser_model_instances_init.set_defaults(func=api.model_instance_initialize_cli)

    # Model Instances create
    parser_model_instances_create = subparsers_model_instances.add_parser(
        "create", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instances_new
    )
    parser_model_instances_create_optional = parser_model_instances_create._action_groups.pop()
    parser_model_instances_create_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_model_instance_upfile
    )
    parser_model_instances_create_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_model_instances_create_optional.add_argument(
        "-r", "--dir-mode", dest="dir_mode", choices=["skip", "zip", "tar"], default="skip", help=Help.param_dir_mode
    )
    parser_model_instances_create._action_groups.append(parser_model_instances_create_optional)
    parser_model_instances_create.set_defaults(func=api.model_instance_create_cli)

    # Model Instances files
    parser_model_instances_files = subparsers_model_instances.add_parser(
        "files", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instances_files
    )
    parser_model_instances_files_optional = parser_model_instances_files._action_groups.pop()
    parser_model_instances_files_optional.add_argument("model_instance", help=Help.param_model_instance)
    _add_output_format_args(parser_model_instances_files_optional)
    parser_model_instances_files_optional.add_argument(
        "--page-size", dest="page_size", default=20, type=int, help=Help.param_page_size
    )
    parser_model_instances_files_optional.add_argument(
        "--page-token", dest="page_token", required=False, help=Help.param_page_token
    )
    parser_model_instances_files._action_groups.append(parser_model_instances_files_optional)
    parser_model_instances_files.set_defaults(func=api.model_instance_files_cli)

    # Model Instances list
    parser_model_instances_list = subparsers_model_instances.add_parser(
        "list", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instances_list
    )
    parser_model_instances_list_optional = parser_model_instances_list._action_groups.pop()
    parser_model_instances_list_optional.add_argument("model_instance", help=Help.param_model_instance)
    _add_output_format_args(parser_model_instances_list_optional)
    parser_model_instances_list_optional.add_argument(
        "--page-size", dest="page_size", default=20, type=int, help=Help.param_page_size
    )
    parser_model_instances_list_optional.add_argument(
        "--page-token", dest="page_token", required=False, help=Help.param_page_token
    )
    parser_model_instances_list._action_groups.append(parser_model_instances_list_optional)
    parser_model_instances_list.set_defaults(func=api.model_instances_list_cli)

    # Models Instances delete
    parser_model_instances_delete = subparsers_model_instances.add_parser(
        "delete", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instances_delete
    )
    parser_model_instances_delete_optional = parser_model_instances_delete._action_groups.pop()
    parser_model_instances_delete_optional.add_argument("model_instance", help=Help.param_model_instance)
    parser_model_instances_delete_optional.add_argument(
        "-y", "--yes", dest="no_confirm", action="store_true", help=Help.param_yes
    )
    parser_model_instances_delete._action_groups.append(parser_model_instances_delete_optional)
    parser_model_instances_delete.set_defaults(func=api.model_instance_delete_cli)

    # Models Instances update
    parser_model_instances_update = subparsers_model_instances.add_parser(
        "update", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_model_instances_update
    )
    parser_model_instances_update_optional = parser_model_instances_update._action_groups.pop()
    parser_model_instances_update_optional.add_argument(
        "-p", "--path", dest="folder", required=False, help=Help.param_model_instance_upfile
    )
    parser_model_instances_update._action_groups.append(parser_model_instances_update_optional)
    parser_model_instances_update.set_defaults(func=api.model_instance_update_cli)

