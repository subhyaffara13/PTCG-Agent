from typing import Any

def get_episode_replay(episode_id: int) -> dict[str, Any]:
    body = {"EpisodeId": episode_id}

    response = requests.post(get_url, json=body)
    return response.json()

