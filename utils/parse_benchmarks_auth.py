
def parse_benchmarks_auth(subparsers) -> None:
    parser_auth = subparsers.add_parser(
        "auth", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_benchmarks_auth
    )
    parser_auth_optional = parser_auth._action_groups.pop()
    parser_auth_optional.add_argument("-y", "--yes", dest="no_confirm", action="store_true", help=Help.param_yes)
    parser_auth_optional.add_argument(
        "--env-file", dest="env_file", default=".env", help=Help.param_benchmarks_env_file
    )
    parser_auth._action_groups.append(parser_auth_optional)
    parser_auth.set_defaults(func=api.benchmarks_auth_cli)

