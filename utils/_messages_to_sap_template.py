from typing import Dict, List

def _messages_to_sap_template(messages: List[Dict[str, str]]) -> list:  # type: ignore[type-arg]
    template = []
    for message in messages:
        if message["role"] == "user":
            template.append(validate_dict(message, SAPUserMessage))
        elif message["role"] == "assistant":
            template.append(validate_dict(message, SAPAssistantMessage))
        elif message["role"] == "tool":
            template.append(validate_dict(message, SAPToolChatMessage))
        else:
            template.append(validate_dict(message, SAPMessage))
    return template

