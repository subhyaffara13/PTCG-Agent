import json
import logging
import subprocess
from pathlib import Path

from kaggle.api.kaggle_api_extended import KaggleApi

from scratch.kaggle_reader import parse_episode_csv, download_episode_replay, parse_episode_replay, load_replay

logger = logging.getLogger(__name__)


def main():
    api = KaggleApi()
    api.authenticate()
    replays_dir = Path("logs/kaggle_replays")
    replays_dir.mkdir(parents=True, exist_ok=True)
    summary_dir = Path("logs/kaggle_summary")
    summary_dir.mkdir(parents=True, exist_ok=True)
    subs = api.competition_submissions("pokemon-tcg-ai-battle")
    complete = [s for s in subs if str(s.status) in ("SubmissionStatus.COMPLETE", "complete")]
    print(f"Fetching submissions... Found {len(complete)} completed.")
    all_results = []
    for s in complete[:5]:
        sub_id = s.ref
        print(f"\nProcessing Submission {sub_id} ({s.date})...")
        cmd = ["kaggle", "competitions", "episodes", str(sub_id), "--csv"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = res.stdout.strip()
            if not output:
                print(f"No episodes for submission {sub_id}.")
                continue
            episodes = parse_episode_csv(output)
            print(f"Found {len(episodes)} episodes.")
            for ep in episodes:
                ep_id = int(ep['id'])
                replay_file = replays_dir / f"episode-{ep_id}-replay.json"
                if not replay_file.exists():
                    print(f"  Downloading replay for episode {ep_id}...")
                    download_episode_replay(ep_id, replays_dir)
                if replay_file.exists():
                    try:
                        data = load_replay(replay_file)
                        if data is None:
                            continue
                        info = parse_episode_replay(data)
                        all_results.append({"submission_id": sub_id, "submission_date": str(s.date), "episode_id": ep_id, **info})
                        print(f"    Episode {ep_id}: {info['result']} vs {info['opponent']} ({info['turns']} turns)")
                    except Exception as parse_err:
                        print(f"    Failed to parse episode {ep_id}: {parse_err}")
        except Exception as e:
            print(f"Failed to get episodes for submission {sub_id}: {e}")
    summary_file = summary_dir / "kaggle_results_summary.json"
    summary_file.write_text(json.dumps(all_results, indent=2), encoding="utf-8")
    print(f"\nSaved consolidated summary to {summary_file.resolve()}")
    print("\n### SUMMARY OF KAGGLE ONLINE EPISODES")
    print("| Submission ID | Date | Episode ID | Opponent | Result | Turns |")
    print("|---|---|---|---|---|---|")
    for r in all_results[:50]:
        print(f"| {r['submission_id']} | {r['submission_date'][:10]} | {r['episode_id']} | {r['opponent']} | {r['result']} | {r['turns']} |")


if __name__ == "__main__":
    main()


__all__ = [
    "parse_episode_csv", "load_replay", "download_episode_replay",
    "determine_result", "find_my_index", "parse_episode_replay", "main",
]
