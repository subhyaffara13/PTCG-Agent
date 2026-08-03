from typing import Any

def __list_episodes(body: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(list_url, json=body)
    return response.json()

