
def retrieve_video_link(dumps):
    for entry in dumps:
        if entry["name"] == "episode_done":
            print("Received video link.")
            return entry["video"]
    return None

