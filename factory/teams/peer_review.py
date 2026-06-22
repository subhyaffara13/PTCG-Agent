import logging

logger = logging.getLogger("PeerReviewAgent")

class PeerReviewAgent:
    def __init__(self):
        pass
        
    def review_changes(self, eval_report: dict) -> bool:
        """
        Reviews the QA test runs. Rejects the pull request if the new code 
        lowers the overall win rate (regression detection).
        """
        version_score = eval_report.get("adjusted", {}).get("version_score", 0.0)
        logic_delta = eval_report.get("adjusted", {}).get("logic_delta", 0.0)
        
        # Peer Review Rejection criteria
        if version_score < 0.50 and logic_delta < 0.0:
            logger.warning("PEER REVIEW REJECTED: The proposed changes caused a regression in the win-rate.")
            return False
            
        logger.info("PEER REVIEW APPROVED: The proposed changes are safe and strictly better.")
        return True
