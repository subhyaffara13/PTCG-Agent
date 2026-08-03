from typing import Dict, Optional

def add_known_models(model_cost_map: Optional[Dict] = None):
    _map = model_cost_map if model_cost_map is not None else model_cost
    for key, value in _map.items():
        if value.get("litellm_provider") == "openai" and not is_openai_finetune_model(
            key
        ):
            open_ai_chat_completion_models.add(key)
        elif value.get("litellm_provider") == "text-completion-openai":
            open_ai_text_completion_models.add(key)
        elif value.get("litellm_provider") == "azure_text":
            azure_text_models.add(key)
        elif value.get("litellm_provider") == "cohere":
            cohere_models.add(key)
        elif value.get("litellm_provider") == "cohere_chat":
            cohere_chat_models.add(key)
        elif value.get("litellm_provider") == "mistral":
            mistral_chat_models.add(key)
        elif value.get("litellm_provider") == "anthropic":
            anthropic_models.add(key)
        elif value.get("litellm_provider") == "empower":
            empower_models.add(key)
        elif value.get("litellm_provider") == "openrouter":
            openrouter_models.add(key)
        elif value.get("litellm_provider") == "vercel_ai_gateway":
            vercel_ai_gateway_models.add(key)
        elif value.get("litellm_provider") == "datarobot":
            datarobot_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-text-models":
            vertex_text_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-code-text-models":
            vertex_code_text_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-language-models":
            vertex_language_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-vision-models":
            vertex_vision_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-chat-models":
            vertex_chat_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-code-chat-models":
            vertex_code_chat_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-embedding-models":
            vertex_embedding_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-anthropic_models":
            key = key.replace("vertex_ai/", "")
            vertex_anthropic_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-llama_models":
            key = key.replace("vertex_ai/", "")
            vertex_llama3_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-deepseek_models":
            key = key.replace("vertex_ai/", "")
            vertex_deepseek_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-mistral_models":
            key = key.replace("vertex_ai/", "")
            vertex_mistral_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-ai21_models":
            key = key.replace("vertex_ai/", "")
            vertex_ai_ai21_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-image-models":
            key = key.replace("vertex_ai/", "")
            vertex_ai_image_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-video-models":
            key = key.replace("vertex_ai/", "")
            vertex_ai_video_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-openai_models":
            key = key.replace("vertex_ai/", "")
            vertex_openai_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-minimax_models":
            key = key.replace("vertex_ai/", "")
            vertex_minimax_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-moonshot_models":
            key = key.replace("vertex_ai/", "")
            vertex_moonshot_models.add(key)
        elif value.get("litellm_provider") == "vertex_ai-zai_models":
            key = key.replace("vertex_ai/", "")
            vertex_zai_models.add(key)
        elif value.get("litellm_provider") == "ai21":
            if value.get("mode") == "chat":
                ai21_chat_models.add(key)
            else:
                ai21_models.add(key)
        elif value.get("litellm_provider") == "nlp_cloud":
            nlp_cloud_models.add(key)
        elif value.get("litellm_provider") == "aleph_alpha":
            aleph_alpha_models.add(key)
        elif value.get(
            "litellm_provider"
        ) == "bedrock" and not is_bedrock_pricing_only_model(key):
            bedrock_models.add(key)
        elif value.get("litellm_provider") == "bedrock_converse":
            bedrock_converse_models.add(key)
        elif value.get("litellm_provider") == "deepinfra":
            deepinfra_models.add(key)
        elif value.get("litellm_provider") == "perplexity":
            perplexity_models.add(key)
        elif value.get("litellm_provider") == "watsonx":
            watsonx_models.add(key)
        elif value.get("litellm_provider") == "gemini":
            gemini_models.add(key)
        elif value.get("litellm_provider") == "fireworks_ai":
            # ignore the 'up-to', '-to-' model names -> not real models. just for cost tracking based on model params.
            if "-to-" not in key and "fireworks-ai-default" not in key:
                fireworks_ai_models.add(key)
        elif value.get("litellm_provider") == "fireworks_ai-embedding-models":
            # ignore the 'up-to', '-to-' model names -> not real models. just for cost tracking based on model params.
            if "-to-" not in key:
                fireworks_ai_embedding_models.add(key)
        elif value.get("litellm_provider") == "text-completion-codestral":
            text_completion_codestral_models.add(key)
        elif value.get("litellm_provider") == "text-completion-inception":
            text_completion_inception_models.add(key)
        elif value.get("litellm_provider") == "xai":
            xai_models.add(key)
        elif value.get("litellm_provider") == "zai":
            zai_models.add(key)
        elif value.get("litellm_provider") == "fal_ai":
            fal_ai_models.add(key)
        elif value.get("litellm_provider") == "deepseek":
            deepseek_models.add(key)
        elif value.get("litellm_provider") == "runwayml":
            runwayml_models.add(key)
        elif value.get("litellm_provider") == "meta_llama":
            llama_models.add(key)
        elif value.get("litellm_provider") == "nscale":
            nscale_models.add(key)
        elif value.get("litellm_provider") == "azure_ai":
            azure_ai_models.add(key)
        elif value.get("litellm_provider") == "voyage":
            voyage_models.add(key)
        elif value.get("litellm_provider") == "infinity":
            infinity_models.add(key)
        elif value.get("litellm_provider") == "databricks":
            databricks_models.add(key)
        elif value.get("litellm_provider") == "cloudflare":
            cloudflare_models.add(key)
        elif value.get("litellm_provider") == "codestral":
            codestral_models.add(key)
        elif value.get("litellm_provider") == "friendliai":
            friendliai_models.add(key)
        elif value.get("litellm_provider") == "palm":
            palm_models.add(key)
        elif value.get("litellm_provider") == "groq":
            groq_models.add(key)
        elif value.get("litellm_provider") == "azure":
            azure_models.add(key)
        elif value.get("litellm_provider") == "azure_anthropic":
            azure_anthropic_models.add(key)
        elif value.get("litellm_provider") == "anyscale":
            anyscale_models.add(key)
        elif value.get("litellm_provider") == "cerebras":
            cerebras_models.add(key)
        elif value.get("litellm_provider") == "galadriel":
            galadriel_models.add(key)
        elif value.get("litellm_provider") == "nvidia_nim":
            nvidia_nim_models.add(key)
        elif value.get("litellm_provider") == "nvidia_riva":
            nvidia_riva_models.add(key)
        elif value.get("litellm_provider") == "soniox":
            soniox_models.add(key)
        elif value.get("litellm_provider") == "sambanova":
            sambanova_models.add(key)
        elif value.get("litellm_provider") == "sambanova-embedding-models":
            sambanova_embedding_models.add(key)
        elif value.get("litellm_provider") == "novita":
            novita_models.add(key)
        elif value.get("litellm_provider") == "nebius-chat-models":
            nebius_models.add(key)
        elif value.get("litellm_provider") == "nebius-embedding-models":
            nebius_embedding_models.add(key)
        elif value.get("litellm_provider") == "aiml":
            aiml_models.add(key)
        elif value.get("litellm_provider") == "assemblyai":
            assemblyai_models.add(key)
        elif value.get("litellm_provider") == "jina_ai":
            jina_ai_models.add(key)
        elif value.get("litellm_provider") == "snowflake":
            snowflake_models.add(key)
        elif value.get("litellm_provider") == "gradient_ai":
            gradient_ai_models.add(key)
        elif value.get("litellm_provider") == "featherless_ai":
            featherless_ai_models.add(key)
        elif value.get("litellm_provider") == "deepgram":
            deepgram_models.add(key)
        elif value.get("litellm_provider") == "elevenlabs":
            elevenlabs_models.add(key)
        elif value.get("litellm_provider") == "heroku":
            heroku_models.add(key)
        elif value.get("litellm_provider") == "dashscope":
            dashscope_models.add(key)
        elif value.get("litellm_provider") == "modelscope":
            modelscope_models.add(key)
        elif value.get("litellm_provider") == "moonshot":
            moonshot_models.add(key)
        elif value.get("litellm_provider") == "publicai":
            publicai_models.add(key)
        elif value.get("litellm_provider") == "v0":
            v0_models.add(key)
        elif value.get("litellm_provider") == "morph":
            morph_models.add(key)
        elif value.get("litellm_provider") == "lambda_ai":
            lambda_ai_models.add(key)
        elif value.get("litellm_provider") == "inception":
            inception_models.add(key)
        elif value.get("litellm_provider") == "hyperbolic":
            hyperbolic_models.add(key)
        elif value.get("litellm_provider") == "black_forest_labs":
            black_forest_labs_models.add(key)
        elif value.get("litellm_provider") == "recraft":
            recraft_models.add(key)
        elif value.get("litellm_provider") == "cometapi":
            cometapi_models.add(key)
        elif value.get("litellm_provider") == "oci":
            oci_models.add(key)
        elif value.get("litellm_provider") == "volcengine":
            volcengine_models.add(key)
        elif value.get("litellm_provider") == "wandb":
            wandb_models.add(key)
        elif value.get("litellm_provider") == "ovhcloud":
            ovhcloud_models.add(key)
        elif value.get("litellm_provider") == "ovhcloud-embedding-models":
            ovhcloud_embedding_models.add(key)
        elif value.get("litellm_provider") == "lemonade":
            lemonade_models.add(key)
        elif value.get("litellm_provider") == "docker_model_runner":
            docker_model_runner_models.add(key)
        elif value.get("litellm_provider") == "amazon_nova":
            amazon_nova_models.add(key)
        elif value.get("litellm_provider") == "stability":
            stability_models.add(key)
        elif value.get("litellm_provider") == "github_copilot":
            github_copilot_models.add(key)
        elif value.get("litellm_provider") == "chatgpt":
            chatgpt_models.add(key)
        elif value.get("litellm_provider") == "minimax":
            minimax_models.add(key)
        elif value.get("litellm_provider") == "aws_polly":
            aws_polly_models.add(key)
        elif value.get("litellm_provider") == "gigachat":
            gigachat_models.add(key)
        elif value.get("litellm_provider") == "llamagate":
            llamagate_models.add(key)
        elif value.get("litellm_provider") == "reducto":
            reducto_models.add(key)
        elif value.get("litellm_provider") == "bedrock_mantle":
            bedrock_mantle_models.add(key)

