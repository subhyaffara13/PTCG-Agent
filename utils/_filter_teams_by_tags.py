
def _filter_teams_by_tags(teams: list, tag_patterns: list) -> tuple:
    """Filter pre-fetched team rows whose metadata.tags match any patterns.

    Returns (named_aliases, unnamed_count).
    """

    affected: list = []
    unnamed_count = 0
    for team in teams:
        team_alias = team.team_alias or ""
        team_tags = _get_tags_from_metadata(team.metadata)
        if team_tags and any(
            RouteChecks._route_matches_wildcard_pattern(route=tag, pattern=pat)
            for tag in team_tags
            for pat in tag_patterns
        ):
            if team_alias:
                affected.append(team_alias)
            else:
                unnamed_count += 1
    return affected, unnamed_count

