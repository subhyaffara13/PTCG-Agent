
def parse_competitions(subparsers) -> None:
    parser_competitions = subparsers.add_parser(
        "competitions", formatter_class=argparse.RawTextHelpFormatter, help=Help.group_competitions, aliases=["c"]
    )
    subparsers_competitions = parser_competitions.add_subparsers(title="commands", dest="command")
    subparsers_competitions.required = True
    subparsers_competitions.choices = Help.competitions_choices

    # Competitions list
    parser_competitions_list = subparsers_competitions.add_parser(
        "list", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_competitions_list
    )
    parser_competitions_list_optional = parser_competitions_list._action_groups.pop()
    parser_competitions_list_optional.add_argument(
        "--group", dest="group", required=False, help=Help.param_competition_group
    )
    parser_competitions_list_optional.add_argument(
        "--category", dest="category", required=False, help=Help.param_competition_category
    )
    parser_competitions_list_optional.add_argument(
        "--sort-by", dest="sort_by", required=False, help=Help.param_competition_sort_by
    )
    parser_competitions_list_optional.add_argument(
        "-p", "--page", dest="page", default=-1, type=int, required=False, help=Help.param_page
    )
    parser_competitions_list_optional.add_argument(
        "-s", "--search", dest="search", required=False, help=Help.param_search
    )
    _add_output_format_args(parser_competitions_list_optional)
    parser_competitions_list_optional.add_argument(
        "--page-size", dest="page_size", required=False, type=int, help=Help.param_page_size
    )
    parser_competitions_list_optional.add_argument(
        "--page-token", dest="page_token", required=False, help=Help.param_page_token
    )
    parser_competitions_list._action_groups.append(parser_competitions_list_optional)
    parser_competitions_list.set_defaults(func=api.competitions_list_cli)

    # Competitions list files
    parser_competitions_files = subparsers_competitions.add_parser(
        "files", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_competitions_files
    )
    parser_competitions_files_optional = parser_competitions_files._action_groups.pop()
    parser_competitions_files_optional.add_argument("competition", nargs="?", default=None, help=Help.param_competition)
    parser_competitions_files_optional.add_argument(
        "-c", "--competition", dest="competition_opt", required=False, help=argparse.SUPPRESS
    )
    _add_output_format_args(parser_competitions_files_optional)
    parser_competitions_files_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_competitions_files_optional.add_argument(
        "--page-token", dest="page_token", required=False, help=Help.param_page_token
    )
    parser_competitions_files_optional.add_argument(
        "--page-size", dest="page_size", required=False, default=20, type=int, help=Help.param_page_size
    )
    parser_competitions_files._action_groups.append(parser_competitions_files_optional)
    parser_competitions_files.set_defaults(func=api.competition_list_files_cli)

    # Competitions download
    parser_competitions_download = subparsers_competitions.add_parser(
        "download", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_competitions_download
    )
    parser_competitions_download_optional = parser_competitions_download._action_groups.pop()
    parser_competitions_download_optional.add_argument(
        "competition", nargs="?", default=None, help=Help.param_competition
    )
    parser_competitions_download_optional.add_argument(
        "-c", "--competition", dest="competition_opt", required=False, help=argparse.SUPPRESS
    )
    parser_competitions_download_optional.add_argument(
        "-f", "--file", dest="file_name", required=False, help=Help.param_competition_file
    )
    parser_competitions_download_optional.add_argument(
        "-p", "--path", dest="path", required=False, help=Help.param_downfolder
    )
    parser_competitions_download_optional.add_argument(
        "-w", "--wp", dest="path", action="store_const", const=".", required=False, help=Help.param_wp
    )
    parser_competitions_download_optional.add_argument(
        "-o", "--force", dest="force", action="store_true", help=Help.param_force
    )
    parser_competitions_download_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_competitions_download._action_groups.append(parser_competitions_download_optional)
    parser_competitions_download.set_defaults(func=api.competition_download_cli)

    # Competitions submit
    parser_competitions_submit = subparsers_competitions.add_parser(
        "submit", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_competitions_submit
    )
    parser_competitions_submit_optional = parser_competitions_submit._action_groups.pop()
    parser_competitions_submit_optional.add_argument(
        "competition", nargs="?", default=None, help=Help.param_competition
    )
    parser_competitions_submit_optional.add_argument(
        "-c", "--competition", dest="competition_opt", required=False, help=argparse.SUPPRESS
    )
    parser_competitions_submit_optional.add_argument("-f", "--file", dest="file_name", help=Help.param_upfile)
    parser_competitions_submit_optional.add_argument("-k", "--kernel", dest="kernel", help=Help.param_code_kernel)
    parser_competitions_submit_optional.add_argument(
        "-m", "--message", dest="message", required=True, help=Help.param_competition_message
    )
    parser_competitions_submit_optional.add_argument("-v", "--version", dest="version", help=Help.param_code_version)
    parser_competitions_submit_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_competitions_submit_optional.add_argument(
        "--sandbox", dest="sandbox", action="store_true", help=Help.param_sandbox
    )
    parser_competitions_submit._action_groups.append(parser_competitions_submit_optional)
    parser_competitions_submit.set_defaults(func=api.competition_submit_cli)

    # Competitions list submissions
    parser_competitions_submissions = subparsers_competitions.add_parser(
        "submissions", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_competitions_submissions
    )
    parser_competitions_submissions_optional = parser_competitions_submissions._action_groups.pop()
    parser_competitions_submissions_optional.add_argument(
        "competition", nargs="?", default=None, help=Help.param_competition
    )
    parser_competitions_submissions_optional.add_argument(
        "-c", "--competition", dest="competition_opt", required=False, help=argparse.SUPPRESS
    )
    _add_output_format_args(parser_competitions_submissions_optional)
    parser_competitions_submissions_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_competitions_submissions_optional.add_argument(
        "--page-size", dest="page_size", required=False, type=int, help=Help.param_page_size
    )
    parser_competitions_submissions_optional.add_argument(
        "--page-token", dest="page_token", required=False, help=Help.param_page_token
    )
    parser_competitions_submissions._action_groups.append(parser_competitions_submissions_optional)
    parser_competitions_submissions.set_defaults(func=api.competition_submissions_cli)

    # Competitions leaderboard
    parser_competitions_leaderboard = subparsers_competitions.add_parser(
        "leaderboard", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_competitions_leaderboard
    )
    parser_competitions_leaderboard_optional = parser_competitions_leaderboard._action_groups.pop()
    parser_competitions_leaderboard_optional.add_argument(
        "competition", nargs="?", default=None, help=Help.param_competition
    )
    parser_competitions_leaderboard_optional.add_argument(
        "-c", "--competition", dest="competition_opt", required=False, help=argparse.SUPPRESS
    )
    parser_competitions_leaderboard_optional.add_argument(
        "-s", "--show", dest="view", action="store_true", help=Help.param_competition_leaderboard_view
    )
    parser_competitions_leaderboard_optional.add_argument(
        "-d", "--download", dest="download", action="store_true", help=Help.param_competition_leaderboard_download
    )
    parser_competitions_leaderboard_optional.add_argument("-p", "--path", dest="path", help=Help.param_downfolder)
    _add_output_format_args(parser_competitions_leaderboard_optional)
    parser_competitions_leaderboard_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_competitions_leaderboard_optional.add_argument(
        "--page-size", dest="page_size", required=False, type=int, help=Help.param_page_size
    )
    parser_competitions_leaderboard_optional.add_argument(
        "--page-token", dest="page_token", required=False, help=Help.param_page_token
    )
    parser_competitions_leaderboard._action_groups.append(parser_competitions_leaderboard_optional)
    parser_competitions_leaderboard.set_defaults(func=api.competition_leaderboard_cli)

    # Competitions list team public submissions
    parser_competitions_team_submissions = subparsers_competitions.add_parser(
        "team-submissions",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_competitions_team_submissions,
    )
    parser_competitions_team_submissions_optional = parser_competitions_team_submissions._action_groups.pop()
    parser_competitions_team_submissions_optional.add_argument(
        "team_id",
        type=int,
        help='Team ID (find these with "kaggle competitions leaderboard <competition> --show")',
    )
    _add_output_format_args(parser_competitions_team_submissions_optional)
    parser_competitions_team_submissions_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_competitions_team_submissions._action_groups.append(parser_competitions_team_submissions_optional)
    parser_competitions_team_submissions.set_defaults(func=api.competition_team_submissions_cli)

    # Competitions list episodes
    parser_competitions_episodes = subparsers_competitions.add_parser(
        "episodes", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_competitions_episodes
    )
    parser_competitions_episodes_optional = parser_competitions_episodes._action_groups.pop()
    parser_competitions_episodes_optional.add_argument(
        "submission_id",
        type=int,
        help='Submission ID (find yours with "kaggle competitions submissions <competition>")',
    )
    _add_output_format_args(parser_competitions_episodes_optional)
    parser_competitions_episodes_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_competitions_episodes._action_groups.append(parser_competitions_episodes_optional)
    parser_competitions_episodes.set_defaults(func=api.competition_list_episodes_cli)

    # Competitions episode replay
    parser_competitions_episode_replay = subparsers_competitions.add_parser(
        "replay", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_competitions_episode_replay
    )
    parser_competitions_episode_replay_optional = parser_competitions_episode_replay._action_groups.pop()
    parser_competitions_episode_replay_optional.add_argument(
        "episode_id", type=int, help='Episode ID (find these with "kaggle competitions episodes <submission_id>")'
    )
    parser_competitions_episode_replay_optional.add_argument(
        "-p", "--path", dest="path", required=False, help=Help.param_downfolder
    )
    parser_competitions_episode_replay_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_competitions_episode_replay._action_groups.append(parser_competitions_episode_replay_optional)
    parser_competitions_episode_replay.set_defaults(func=api.competition_episode_replay_cli)

    # Competitions episode agent logs
    parser_competitions_episode_logs = subparsers_competitions.add_parser(
        "logs", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_competitions_episode_logs
    )
    parser_competitions_episode_logs_optional = parser_competitions_episode_logs._action_groups.pop()
    parser_competitions_episode_logs_optional.add_argument(
        "episode_id", type=int, help='Episode ID (find these with "kaggle competitions episodes <submission_id>")'
    )
    parser_competitions_episode_logs_optional.add_argument(
        "agent_index", type=int, help="Agent index (0-based position of the agent in the episode)"
    )
    parser_competitions_episode_logs_optional.add_argument(
        "-p", "--path", dest="path", required=False, help=Help.param_downfolder
    )
    parser_competitions_episode_logs_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_competitions_episode_logs._action_groups.append(parser_competitions_episode_logs_optional)
    parser_competitions_episode_logs.set_defaults(func=api.competition_episode_agent_logs_cli)

    # Competitions list pages
    parser_competitions_pages = subparsers_competitions.add_parser(
        "pages", formatter_class=argparse.RawTextHelpFormatter, help=Help.command_competitions_pages
    )
    parser_competitions_pages_optional = parser_competitions_pages._action_groups.pop()
    parser_competitions_pages_optional.add_argument("competition", nargs="?", default=None, help=Help.param_competition)
    parser_competitions_pages_optional.add_argument(
        "-c", "--competition", dest="competition_opt", required=False, help=argparse.SUPPRESS
    )
    _add_output_format_args(parser_competitions_pages_optional)
    parser_competitions_pages_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_competitions_pages_optional.add_argument(
        "--content", dest="content", action="store_true", help="Show full page content"
    )
    parser_competitions_pages_optional.add_argument(
        "--page-name",
        dest="page_name",
        required=False,
        help='Filter to a specific page (e.g. "description", "rules", "evaluation")',
    )
    parser_competitions_pages._action_groups.append(parser_competitions_pages_optional)
    parser_competitions_pages.set_defaults(func=api.competition_list_pages_cli)

    shared_topics = _get_shared_topics_parser()
    shared_competition_topics = _get_shared_competition_topics_parser()

    # Competitions list discussion topics (with 'show' and 'list' subcommands)
    parser_competitions_topics = subparsers_competitions.add_parser(
        "topics",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_competitions_topics,
        parents=[shared_competition_topics],
    )
    subparsers_competitions_topics = parser_competitions_topics.add_subparsers(title="commands", dest="command")
    subparsers_competitions_topics.choices = Help.entity_topics_choices

    # Default action: list topics (when no subcommand given)
    parser_competitions_topics.set_defaults(func=api.competition_list_topics_cli)

    # Competitions topics list (explicit)
    parser_competitions_topics_list = subparsers_competitions_topics.add_parser(
        "list",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_competitions_topics,
        parents=[shared_competition_topics],
    )
    parser_competitions_topics_list_optional = parser_competitions_topics_list._action_groups.pop()
    parser_competitions_topics_list_optional.add_argument(
        "competition", nargs="?", default=None, help=Help.param_competition
    )
    parser_competitions_topics_list_optional.add_argument(
        "-c", "--competition", dest="competition_opt", required=False, help=argparse.SUPPRESS
    )
    parser_competitions_topics_list_optional.add_argument(
        "-s",
        "--sort-by",
        dest="sort_by",
        required=False,
        help="Sort order. One of: " + ", ".join(KaggleApi.valid_forum_topic_sort_by),
    )
    parser_competitions_topics_list._action_groups.append(parser_competitions_topics_list_optional)
    parser_competitions_topics_list.set_defaults(func=api.competition_list_topics_cli)

    # Competitions topics show
    parser_competitions_topics_show = subparsers_competitions_topics.add_parser(
        "show",
        formatter_class=argparse.RawTextHelpFormatter,
        help=Help.command_entity_topics_show,
        parents=[shared_topics],
    )
    parser_competitions_topics_show_optional = parser_competitions_topics_show._action_groups.pop()
    parser_competitions_topics_show_optional.add_argument("topic_ref", help=Help.param_topic_ref)
    parser_competitions_topics_show_optional.add_argument(
        "topic_id_arg",
        nargs="?",
        default=None,
        type=int,
        help="Topic ID (when using two-arg form: <competition> <topic-id>)",
    )
    parser_competitions_topics_show._action_groups.append(parser_competitions_topics_show_optional)
    parser_competitions_topics_show.set_defaults(func=api.forums_topic_show_cli)

    # Competitions list messages within a topic (DEPRECATED — hidden alias)
    parser_competitions_topic_messages = subparsers_competitions.add_parser(
        "topic-messages",
        formatter_class=argparse.RawTextHelpFormatter,
        help=argparse.SUPPRESS,
    )
    parser_competitions_topic_messages_optional = parser_competitions_topic_messages._action_groups.pop()
    parser_competitions_topic_messages_optional.add_argument(
        "competition", nargs="?", default=None, help=Help.param_competition
    )
    parser_competitions_topic_messages_optional.add_argument(
        "topic_id", nargs="?", default=None, type=int, help="The discussion topic id"
    )
    parser_competitions_topic_messages_optional.add_argument(
        "-c", "--competition", dest="competition_opt", required=False, help=argparse.SUPPRESS
    )
    parser_competitions_topic_messages_optional.add_argument(
        "-s",
        "--sort-by",
        dest="sort_by",
        required=False,
        help="Sort order. One of: " + ", ".join(KaggleApi.valid_comment_sort_by),
    )
    parser_competitions_topic_messages_optional.add_argument(
        "-n",
        "--page-size",
        dest="page_size",
        type=int,
        required=False,
        help="Max top-level messages to return; -1 for all",
    )
    _add_output_format_args(parser_competitions_topic_messages_optional)
    parser_competitions_topic_messages_optional.add_argument(
        "-q", "--quiet", dest="quiet", action="store_true", help=Help.param_quiet
    )
    parser_competitions_topic_messages._action_groups.append(parser_competitions_topic_messages_optional)
    parser_competitions_topic_messages.set_defaults(func=api.competition_list_topic_messages_cli)

