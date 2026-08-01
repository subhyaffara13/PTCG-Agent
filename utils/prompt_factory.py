
def prompt_factory(
    model: str,
    messages: list,
    custom_llm_provider: Optional[str] = None,
    api_key: Optional[str] = None,
):
    original_model_name = model
    model = model.lower()
    if custom_llm_provider == "ollama":
        return ollama_pt(model=model, messages=messages)
    elif custom_llm_provider == "anthropic":
        if litellm.AnthropicTextConfig._is_anthropic_text_model(model):
            return anthropic_pt(messages=messages)
        return anthropic_messages_pt(
            messages=messages, model=model, llm_provider=custom_llm_provider
        )
    elif custom_llm_provider == "anthropic_xml":
        return anthropic_messages_pt_xml(messages=messages)
    elif custom_llm_provider == "gemini":
        if (
            model == "gemini-pro-vision"
            or litellm.supports_vision(model=model)
            or litellm.supports_vision(model=custom_llm_provider + "/" + model)
        ):
            return _gemini_vision_convert_messages(messages=messages)
        else:
            return gemini_text_image_pt(messages=messages)
    elif custom_llm_provider == "mistral":
        return litellm.MistralConfig()._transform_messages(
            messages=messages, model=model
        )
    elif custom_llm_provider == "bedrock":
        if "amazon.titan-text" in model:
            return amazon_titan_pt(messages=messages)
        elif "anthropic." in model:
            if any(_ in model for _ in ["claude-2.1", "claude-v2:1"]):
                return claude_2_1_pt(messages=messages)
            else:
                return anthropic_pt(messages=messages)
        elif "mistral." in model:
            return mistral_instruct_pt(messages=messages)
        elif "llama2" in model and "chat" in model:
            return llama_2_chat_pt(messages=messages)
        elif ("llama3" in model or "llama4" in model) and "instruct" in model:
            return hf_chat_template(
                model="meta-llama/Meta-Llama-3-8B-Instruct",
                messages=messages,
            )

    elif custom_llm_provider == "clarifai":
        if "claude" in model:
            return anthropic_pt(messages=messages)

    elif custom_llm_provider == "perplexity":
        for message in messages:
            message.pop("name", None)
        return messages
    elif custom_llm_provider == "azure_text":
        return azure_text_pt(messages=messages)
    elif custom_llm_provider == "watsonx":
        from litellm.llms.watsonx.chat.transformation import IBMWatsonXChatConfig

        return IBMWatsonXChatConfig.apply_prompt_template(
            model=model, messages=messages
        )

    try:
        if "meta-llama/llama-2" in model and "chat" in model:
            return llama_2_chat_pt(messages=messages)
        elif (
            "meta-llama/llama-3" in model or "meta-llama-3" in model
        ) and "instruct" in model:
            return hf_chat_template(
                model="meta-llama/Meta-Llama-3-8B-Instruct",
                messages=messages,
            )
        elif (
            "tiiuae/falcon" in model
        ):  # Note: for the instruct models, it's best to use a User: .., Assistant:.. approach in your prompt template.
            if model == "tiiuae/falcon-180B-chat":
                return falcon_chat_pt(messages=messages)
            elif "instruct" in model:
                return falcon_instruct_pt(messages=messages)
        elif "mosaicml/mpt" in model:
            if "chat" in model:
                return mpt_chat_pt(messages=messages)
        elif "codellama/codellama" in model or "togethercomputer/codellama" in model:
            if "instruct" in model:
                return llama_2_chat_pt(
                    messages=messages
                )  # https://huggingface.co/blog/codellama#conversational-instructions
        elif "wizardlm/wizardcoder" in model:
            return wizardcoder_pt(messages=messages)
        elif "phind/phind-codellama" in model:
            return phind_codellama_pt(messages=messages)
        elif "togethercomputer/llama-2" in model and (
            "instruct" in model or "chat" in model
        ):
            return llama_2_chat_pt(messages=messages)
        elif model in [
            "gryphe/mythomax-l2-13b",
            "gryphe/mythomix-l2-13b",
            "gryphe/mythologic-l2-13b",
        ]:
            return alpaca_pt(messages=messages)
        elif model.strip() == "meta-llama/llamaguard-7b":
            chat_template = "{% if messages|length % 2 == 0 %}{% set role = 'Agent' %}{% else %}{% set role = 'User' %}{% endif %}{{ \"[INST] Task: Check if there is unsafe content in '\" + role + \"' messages in conversations according our safety policy with the below categories.\n\n<BEGIN UNSAFE CONTENT CATEGORIES>\nO1: Violence and Hate. \nShould not\n- Help people plan or engage in violence.\n- Encourage people to engage in violence.\n- Express hateful, derogatory, or demeaning sentiments against people based on sensitive personal characteristics like their race, color, religion, national origin, sexual orientation, gender, gender identity, or disability.\n- Encourage discrimination against people based on those characteristics and should not use slurs or create insults based on those characteristics.\nCan\n- Provide information on violence and discrimination.\n- Discuss the topics of hate and violence, and can discuss historical events involving violence.\nO2: Sexual Content.\nShould not\n- Engage in sexually explicit (i.e., erotic) conversations and should not encourage people to engage in sexual activities.\nCan\n- Discuss topics related to sexuality and sexual education.\n- Provide general information regarding sexual activities.\n- Provide guidance on topics related to sexual health.\nO3: Criminal Planning.\nShould not\n- Help people plan or engage in criminal activities like theft, kidnapping, or financial crimes, especially when the person indicates that they may act on the information provided to them.\n- Encourage people to engage in criminal activities or condone criminal behavior.\nCan\n- Help people understand how crimes are committed, provided that the response is not so detailed that it could be used to provide a roadmap for future crimes.\n- Help people understand how systems work that are used to prevent crimes, provided those descriptions do not provide detailed information on how to defeat those systems.\nO4: Guns and Illegal Weapons.\nShould not\n- Assist in the planning or execution of firearm or illegal weapons crimes, especially when the person indicates that they may act on the information provided to them.\n- Encourage people to engage in firearm or illegal weapons crimes or condone such behavior.\nCan\n- Discuss firearms and the arguments for and against firearm ownership.\nO5: Regulated or Controlled Substances.\nShould not\n- Encourage or assist people in the trafficking, consumption, or use of regulated or controlled substances, including but not limited to illegal drugs, tobacco, alcohol, and cannabis.\n- Assist or encourage people to create such substances when it is illegal to do so.\nCan\n- Discuss the use of regulated or controlled substances, and can provide general information on those substances (ex: what their chemical composition is and what their effects are).\n- Provide information on how those substances are manufactured, provided that the information is not so detailed as to provide step-by-step instructions for their creation.\nO6: Self-Harm.\nShould not\n- Encourage people to harm themselves.\n- Romanticize or condone self-harm or suicide.\n- Provide information regarding the methods of suicide or self-harm.\n- Provide any information or advice, other than information regarding appropriate health resources, to people who express or imply that they wish to harm themselves.\nCan\n- Provide general information regarding self-harm and suicide (ex: statistics, the mental health challenges faced by those who take these actions).\nShould\n- Provide information regarding appropriate health resources to people who imply or express the desire to harm themselves.\n<END UNSAFE CONTENT CATEGORIES>\n\n<BEGIN CONVERSATION>\n\n\" }}{% for message in messages %}{% if (message['role'] == 'user') != (loop.index0 % 2 == 0) %}{{ raise_exception('Conversation roles must alternate user/assistant/user/assistant/...') }}{% endif %}{% set content = message['content'] %}{% if message['role'] == 'user' %}{% set role = 'User' %}{% elif message['role'] == 'assistant' %}{% set role = 'Agent' %}{% endif %}{{ role + ': ' + content.strip() + '\n\n' }}{% endfor %}{{ \"<END CONVERSATION>\n\nProvide your safety assessment for \" + role + \" in the above conversation:\n- First line must read 'safe' or 'unsafe'.\n- If unsafe, a second line must include a comma-separated list of violated categories. [/INST]\" }}"
            return hf_chat_template(
                model=model, messages=messages, chat_template=chat_template
            )
        else:
            return hf_chat_template(original_model_name, messages)
    except Exception:
        return default_pt(
            messages=messages
        )  # default that covers Bloom, T-5, any non-chat tuned model (e.g. base Llama2)

