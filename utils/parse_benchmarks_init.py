
def parse_benchmarks_init(subparsers) -> None:
    parser_init = subparsers.add_parser(
        "init", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_benchmarks_init
    )
    parser_init_optional = parser_init._action_groups.pop()
    parser_init_optional.add_argument("-y", "--yes", dest="no_confirm", action="store_true", help=Help.param_yes)
    parser_init_optional.add_argument(
        "--env-file", dest="env_file", default=".env", help=Help.param_benchmarks_env_file
    )
    parser_init_optional.add_argument(
        "--example-file", dest="example_file", default="example_task.py", help=Help.param_benchmarks_example_file
    )
    parser_init._action_groups.append(parser_init_optional)
    parser_init.set_defaults(func=api.benchmarks_init_cli)

