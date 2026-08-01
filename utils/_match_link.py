
def _match_link(link: Link, candidate: Candidate) -> bool:
    if candidate.source_link:
        return links_equivalent(link, candidate.source_link)
    return False

