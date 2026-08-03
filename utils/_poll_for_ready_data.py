import time
from typing import Any, Dict, Optional

def _poll_for_ready_data(
    url: str,
    *,
    headers: Optional[Dict[str, str]] = None,
    total_timeout: int = 300,
    poll_interval: int = 2,
    request_timeout: int = 10,
    pending_message: Optional[str] = None,
    pending_log_every: int = 10,
    other_status_message: Optional[str] = None,
    other_status_log_every: int = 10,
    http_error_log_every: int = 10,
    connection_error_log_every: int = 10,
) -> Optional[Dict[str, Any]]:
    for attempt in range(total_timeout // poll_interval):
        try:
            request_kwargs: Dict[str, Any] = {"timeout": request_timeout}
            if headers is not None:
                request_kwargs["headers"] = headers
            response = requests.get(url, **request_kwargs)
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")
                if status == "ready":
                    return data
                if status == "pending":
                    if (
                        pending_message
                        and pending_log_every > 0
                        and attempt % pending_log_every == 0
                    ):
                        click.echo(pending_message)
                elif (
                    other_status_message
                    and other_status_log_every > 0
                    and attempt % other_status_log_every == 0
                ):
                    click.echo(other_status_message)
            elif http_error_log_every > 0 and attempt % http_error_log_every == 0:
                click.echo(f"Polling error: HTTP {response.status_code}")
        except requests.RequestException as e:
            if (
                connection_error_log_every > 0
                and attempt % connection_error_log_every == 0
            ):
                click.echo(f"Connection error (will retry): {e}")
        time.sleep(poll_interval)
    return None

