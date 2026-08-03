import json
import os
from typing import Any

def _model_proxy_send(module: str, **kwargs: Any) -> None:
    """Default exporter that POSTs to the Kaggle Model Proxy /telemetry/logs."""
    token = os.environ.get("MODEL_PROXY_KEY")
    url = os.environ.get("MODEL_PROXY_URL")
    if not token or not url or url == "dummy_url":
        _log.info("[telemetry] %s %s", module, json.dumps(kwargs, default=str))
        return
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc or parsed.path.split("/", 1)[0]
    endpoint = f"https://{host}/telemetry/logs"
    payload = json.dumps({module: kwargs}).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=5).close()
    except Exception as exc:  # noqa: BLE001 - never let telemetry break play
        _log.warning("Failed to post telemetry to Kaggle Model Proxy: %s", exc)

