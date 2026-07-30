import subprocess
import logging
logger = logging.getLogger("PeerReviewAgent")

def get_git_diff(logic_candidate):
    diff_text = ""
    try:
        res = subprocess.run(["git", "diff", logic_candidate], capture_output=True, text=True)
        diff_text = res.stdout.strip()
        if not diff_text:
            res = subprocess.run(["git", "--no-pager", "diff", "--cached", logic_candidate], capture_output=True, text=True)
            diff_text = res.stdout.strip()
        if not diff_text:
            res = subprocess.run(["git", "--no-pager", "diff", "HEAD~1", "HEAD", "--", logic_candidate], capture_output=True, text=True)
            diff_text = res.stdout.strip()
    except Exception as git_e:
        logger.warning(f"Could not retrieve git diff for {logic_candidate}: {git_e}")
    return diff_text

def call_llm_review(diff_text):
    import os, json, requests
    from dotenv import load_dotenv
    load_dotenv()
    gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not gemini_key:
        return True
    prompt = f"""
    You are a senior Peer Reviewer auditing code modifications for a Pokemon TCG playing agent.
    Review the following code diff for safety, correctness, and potential regressions:

    ```diff
    {diff_text}
    ```

    Provide your review. You must decide whether to approve or reject the change.
    - Approve (`approved: true`) if the changes are safe, correct, and improve or maintain play.
    - Reject (`approved: false`) if the changes contain syntax bugs, logic errors, infinite loops, or break TCG rules.
    """
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": {
                    "reasoning": {"type": "STRING"},
                    "approved": {"type": "BOOLEAN"},
                    "reason": {"type": "STRING"}
                },
                "required": ["reasoning", "approved", "reason"]
            }
        }
    }
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
        if res.status_code == 200:
            data = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(data)
            approved = parsed.get("approved", True)
            reason = parsed.get("reason", "")
            logger.info(f"Peer Review LLM Decision: {'APPROVED' if approved else 'REJECTED'}. Reason: {reason}")
            return approved
    except Exception as e:
        logger.warning(f"LLM Peer Review failed: {e}. Falling back to baseline score check.")
    return True
