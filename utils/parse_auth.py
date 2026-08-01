
def parse_auth(subparsers) -> None:
    parser_auth = subparsers.add_parser("auth", formatter_class=argparse.RawTextHelpFormatter, help=Help.group_auth)
    subparsers_auth = parser_auth.add_subparsers(title="commands", dest="command")
    subparsers_auth.required = True
    subparsers_auth.choices = Help.auth_choices

    parser_auth_login = subparsers_auth.add_parser(
        "login", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_auth_login
    )
    parser_auth_login.add_argument(
        "--no-launch-browser",
        dest="no_launch_browser",
        action="store_true",
        help="Do not launch a browser for authentication",
    )
    parser_auth_login.add_argument(
        "--force",
        dest="force",
        action="store_true",
        help="Re-run the login flow even if the current account is already logged-in",
    )
    parser_auth_login.set_defaults(func=api.auth_login_cli)

    parser_auth_print_access_token = subparsers_auth.add_parser(
        "print-access-token", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_auth_print_access_token
    )
    parser_auth_print_access_token.add_argument(
        "--expiration",
        dest="expiration_duration",
        required=False,
        help="Override the default expiration duration. Example: 6h for 6 hours, 2:30 for 2 hours and 30 minutes.",
    )
    parser_auth_print_access_token.set_defaults(func=api.auth_print_access_token)

    parser_auth_revoke_token = subparsers_auth.add_parser(
        "revoke", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_auth_revoke_token
    )
    parser_auth_revoke_token.add_argument(
        "--reason",
        dest="reason",
        required=False,
        help="Reason for revoking the token. If not specified, the default reason will be used.",
    )
    parser_auth_revoke_token.set_defaults(func=api.auth_revoke_token)

