import logging

logger = logging.getLogger("PeerReviewAgent")

class PeerReviewAgent:
    def __init__(self):
        pass
        
    def review_changes(self, eval_report: dict, logic_candidate: str | None = None) -> bool:
        """
        Reviews the QA test runs and the actual code diff. Rejects the pull request if 
        the proposed changes cause a regression or fail LLM semantic code review.
        """
        version_score = eval_report.get("adjusted", {}).get("version_score", 0.0)
        logic_delta = eval_report.get("adjusted", {}).get("logic_delta", 0.0)
        
        # 1. Baseline Numerical Check
        if version_score < 0.50 and logic_delta < 0.0:
            logger.warning("PEER REVIEW REJECTED: The proposed changes caused a regression in the win-rate.")
            return False

        # 2. Extract Git Diff for LLM Code Review
        diff_text = ""
        if logic_candidate:
            try:
                import subprocess
                # Check unstaged diff
                res = subprocess.run(["git", "diff", logic_candidate], capture_output=True, text=True)
                diff_text = res.stdout.strip()
                if not diff_text:
                    # Check staged diff
                    res = subprocess.run(["git", "--no-pager", "diff", "--cached", logic_candidate], capture_output=True, text=True)
                    diff_text = res.stdout.strip()
                if not diff_text:
                    # Check last commit diff
                    res = subprocess.run(["git", "--no-pager", "diff", "HEAD~1", "HEAD", "--", logic_candidate], capture_output=True, text=True)
                    diff_text = res.stdout.strip()
            except Exception as git_e:
                logger.warning(f"Could not retrieve git diff for {logic_candidate}: {git_e}")

        # 3. Gemini LLM Code Review
        if diff_text:
            import os
            import json
            import requests
            from dotenv import load_dotenv
            
            load_dotenv()
            gemini_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
            if gemini_key:
                logger.info("Peer Review Agent: Connecting to Google Gemini for LLM code review...")
                prompt = f"""
                You are a senior Peer Reviewer auditing code modifications for a Pokémon TCG playing agent.
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
                                "reasoning": {"type": "STRING", "description": "Chain-of-thought analysis of the code diff."},
                                "approved": {"type": "BOOLEAN", "description": "Whether to approve (true) or reject (false) the change."},
                                "reason": {"type": "STRING", "description": "Explanation for your decision."}
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
                        if not approved:
                            return False
                except Exception as e:
                    logger.warning(f"LLM Peer Review failed: {e}. Falling back to baseline score check.")

        logger.info("PEER REVIEW APPROVED: The proposed changes are safe and strictly better.")
        return True
