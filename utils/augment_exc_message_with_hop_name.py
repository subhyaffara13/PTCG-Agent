
def augment_exc_message_with_hop_name(exc: Exception, msg: str) -> str:
    # Add HOP context right after before the explanation if present;
    # otherwise after the message
    if hasattr(exc, "_hop_name"):
        lines = msg.partition("\n  Explanation:")
        msg = (
            f"{lines[0]}\n  Higher Order Operator: {exc._hop_name}{lines[1]}{lines[2]}"  # type: ignore[attr-defined]
        )

    return msg

