
def parse_quota(subparsers) -> None:
    parser_quota = subparsers.add_parser("quota", formatter_class=argparse.RawTextHelpFormatter, help=Help.group_quota)
    _add_output_format_args(parser_quota)
    parser_quota.set_defaults(func=api.quota_view_cli)

