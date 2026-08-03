from typing import Any, List, Optional

def _routing_selector_matches_claim(
    selector_value: Optional[Any],
    claim_value: Optional[Any],
    *,
    split_space_delimited: bool = False,
) -> bool:
    if selector_value is None:
        return True

    selector_list: List[str] = (
        [str(v) for v in selector_value]
        if isinstance(selector_value, list)
        else [str(selector_value)]
    )

    if claim_value is None:
        return False

    if isinstance(claim_value, list):
        claim_list = [str(v) for v in claim_value]
    elif (
        split_space_delimited
        and isinstance(claim_value, str)
        and " " in claim_value.strip()
    ):
        # OAuth/OIDC often sends scope as a single space-delimited string. Only split
        # for the scope selector: iss/aud/client_id must stay exact full-string match
        # on unverified claims (see routing override security review). The elif guard
        # (`" " in claim_value.strip()`) ensures at least two non-empty tokens survive.
        claim_list = [v for v in claim_value.strip().split(" ") if v]
    else:
        claim_list = [str(claim_value)]

    def _selector_matches_claim(selector: str, claim: str) -> bool:
        # NOTE: wildcard matching is case-sensitive (fnmatch.fnmatchcase).
        if "*" in selector or "?" in selector:
            # Without scope splitting, do not let `*` span whitespace: a malformed
            # iss like "trusted.example.com evil.com" must not match "trusted.*".
            # Scope uses split_space_delimited so each claim token is checked separately.
            if not split_space_delimited and any(ch.isspace() for ch in claim):
                return False
            return fnmatch.fnmatchcase(claim, selector)
        return selector == claim

    return any(
        _selector_matches_claim(selector=s, claim=c)
        for s in selector_list
        for c in claim_list
    )

