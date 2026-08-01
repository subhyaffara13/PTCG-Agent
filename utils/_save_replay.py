
def _save_replay(env: Any, replay_path: str) -> None:
    os.makedirs(os.path.dirname(replay_path), exist_ok=True)
    with open(replay_path, "w") as f:
        json.dump(env.toJSON(), f)
    print(f"\nReplay saved to {replay_path}")

