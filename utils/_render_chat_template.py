
def _render_chat_template(
    env, chat_template: str, bos_token: str, eos_token: str, messages: list
) -> str:
    """
    Shared template rendering logic for both sync and async hf_chat_template

    Args:
        env: Jinja2 environment
        chat_template: Chat template string
        bos_token: Beginning of sequence token
        eos_token: End of sequence token
        messages: Messages to render

    Returns:
        Rendered template string
    """
    try:
        template = env.from_string(chat_template)  # type: ignore
    except Exception as e:
        raise e

    def _is_system_in_template():
        try:
            # Try rendering the template with a system message
            template.render(
                messages=[{"role": "system", "content": "test"}],
                eos_token="<eos>",
                bos_token="<bos>",
            )
            return True
        # This will be raised if Jinja attempts to render the system message and it can't
        except Exception:
            return False

    try:
        rendered_text = ""
        # Render the template with the provided values
        if _is_system_in_template():
            rendered_text = template.render(
                bos_token=bos_token,
                eos_token=eos_token,
                messages=messages,
                add_generation_prompt=True,
            )
        else:
            # treat a system message as a user message, if system not in template
            reformatted_messages = []
            try:
                for message in messages:
                    if message["role"] == "system":
                        reformatted_messages.append(
                            {"role": "user", "content": message["content"]}
                        )
                    else:
                        reformatted_messages.append(message)
                rendered_text = template.render(
                    bos_token=bos_token,
                    eos_token=eos_token,
                    messages=reformatted_messages,
                    add_generation_prompt=True,
                )
            except Exception as e:
                if "Conversation roles must alternate user/assistant" in str(e):
                    # reformat messages to ensure user/assistant are alternating
                    new_messages = []
                    for i in range(len(reformatted_messages) - 1):
                        new_messages.append(reformatted_messages[i])
                        if (
                            reformatted_messages[i]["role"]
                            == reformatted_messages[i + 1]["role"]
                        ):
                            if reformatted_messages[i]["role"] == "user":
                                new_messages.append(
                                    {"role": "assistant", "content": ""}
                                )
                            else:
                                new_messages.append({"role": "user", "content": ""})
                    new_messages.append(reformatted_messages[-1])
                    rendered_text = template.render(
                        bos_token=bos_token, eos_token=eos_token, messages=new_messages
                    )

        return rendered_text
    except Exception as e:
        raise Exception(
            f"Error rendering template - {str(e)}"
        )  # don't use verbose_logger.exception, if exception is raised

