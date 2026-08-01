
def list_episodes_for_submission(submission_id: int) -> dict[str, Any]:
    return __list_episodes({"SubmissionId": submission_id})

