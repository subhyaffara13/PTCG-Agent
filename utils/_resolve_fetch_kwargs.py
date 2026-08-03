from typing import Any, Dict, Optional

def _resolve_fetch_kwargs(
    fn_name: str,
    fn_args: Dict[str, str],
    user_id: Optional[str],
    is_admin: bool,
) -> Dict[str, Any]:
    """Build keyword arguments for a tool's fetch function."""
    start_date = fn_args.get("start_date", "")
    end_date = fn_args.get("end_date", "")
    if not start_date or not end_date:
        raise ValueError("Missing required start_date or end_date from tool arguments")
    kwargs: Dict[str, Any] = {"start_date": start_date, "end_date": end_date}
    if fn_name == "get_usage_data":
        if not is_admin:
            if user_id is None:
                # Defense-in-depth: the endpoint guard in usage_endpoints/endpoints.py
                # should have already rejected this. If we ever reach here it means
                # a future caller invoked the helper without scoping — fail loudly
                # rather than issuing an unfiltered global query.
                raise ValueError(
                    "Non-admin caller has user_id=None; refusing to issue an "
                    "unscoped query. Endpoint-level guard missing."
                )
            kwargs["user_id"] = user_id
        elif fn_args.get("user_id"):
            kwargs["user_id"] = fn_args["user_id"]
    elif fn_name == "get_team_usage_data" and fn_args.get("team_ids"):
        kwargs["team_ids"] = fn_args["team_ids"]
    elif fn_name == "get_tag_usage_data" and fn_args.get("tags"):
        kwargs["tags"] = fn_args["tags"]
    return kwargs

