import sys
import os
import json
import subprocess
from pathlib import Path

def auto_submit_if_ready():
    from kaggle.api.kaggle_api_extended import KaggleApi
    from datetime import datetime, timezone

    api = None
    subs = None
    print("[Auto-Submit] Auditing submission budget...")
    try:
        api = KaggleApi()
        api.authenticate()
        subs = api.competition_submissions("pokemon-tcg-ai-battle")
    except Exception as e:
        print(f"[Auto-Submit] Failed to authenticate or query Kaggle: {e}")
        return

    if api is None or subs is None:
        return

    now_utc = datetime.now(timezone.utc)
    today_subs = 0
    last_sub_time = None
    for s in subs:
        if s is not None:
            s_date = s.date.replace(tzinfo=timezone.utc)
            if s_date.date() == now_utc.date():
                today_subs += 1
            if last_sub_time is None or s_date > last_sub_time:
                last_sub_time = s_date

    print(f"[Auto-Submit] Submissions today (UTC): {today_subs}/5")
    if last_sub_time:
        elapsed_hours = (now_utc - last_sub_time).total_seconds() / 3600.0
        print(f"[Auto-Submit] Hours elapsed since last submission: {elapsed_hours:.2f}h")
    else:
        elapsed_hours = 999.0

    best_fit_path = Path("logs/best_fitness.json")
    last_submitted_fit_path = Path("logs/last_submitted_fitness.json")
    current_best_fit = -9999.0
    if best_fit_path.exists():
        try:
            current_best_fit = float(json.loads(best_fit_path.read_text(encoding="utf-8")).get("best_fitness", -9999.0))
        except Exception:
            pass
    last_submitted_fit = -9999.0
    if last_submitted_fit_path.exists():
        try:
            last_submitted_fit = float(json.loads(last_submitted_fit_path.read_text(encoding="utf-8")).get("last_submitted_fitness", -9999.0))
        except Exception:
            pass
    is_new_best = current_best_fit > last_submitted_fit + 0.1

    should_submit = False
    reason = ""
    if today_subs < 5:
        if is_new_best:
            if elapsed_hours >= 1.0:
                should_submit = True
                reason = f"Breakthrough! Fitness improved from {last_submitted_fit:.2f} to {current_best_fit:.2f}."
            else:
                print(f"[Auto-Submit] Breakthrough detected, but waiting 1.0 hour to space submissions. ({elapsed_hours:.2f}h elapsed)")
        elif elapsed_hours >= 4.5:
            should_submit = True
            reason = f"Spacing trigger: {elapsed_hours:.1f} hours elapsed since last submission."

    if should_submit:
        print(f"[Auto-Submit] TRIGGERING SUBMISSION: {reason}")
        try:
            print("[Auto-Submit] Packaging submission...")
            subprocess.run([sys.executable, "build_submission.py"], check=True)
            print("[Auto-Submit] Uploading to Kaggle...")
            desc = f"Apex Automated: GA Deck + MCTS. Fitness: {current_best_fit:.2f}. Reason: {reason}"
            api.competition_submit("submission.tar.gz", desc, "pokemon-tcg-ai-battle")
            last_submitted_fit_path.write_text(json.dumps({"last_submitted_fitness": current_best_fit}), encoding="utf-8")
            print("[Auto-Submit] Submission successful.")
        except Exception as e:
            print(f"[Auto-Submit] Submission failed with error: {e}")
    else:
        print("[Auto-Submit] No submission triggered.")
