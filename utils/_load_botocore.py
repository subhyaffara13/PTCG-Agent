from typing import Any

def _load_botocore() -> tuple[Any, Any, Any, Any]:
    try:
        from botocore.auth import SigV4Auth  # type: ignore[import-untyped]
        from botocore.session import Session  # type: ignore[import-untyped]
        from botocore.awsrequest import AWSRequest  # type: ignore[import-untyped]
        from botocore.credentials import Credentials  # type: ignore[import-untyped]
    except ImportError as exc:
        raise OpenAIError(
            "Bedrock AWS authentication requires optional AWS dependencies. "
            "Install them with `pip install openai[bedrock]` and try again."
        ) from exc

    return SigV4Auth, AWSRequest, Credentials, Session

