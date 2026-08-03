import json
import os

def process_replay_file(input_path, output_dir, config_path, tts_provider, prompt_path, cache_path, disable_llm,
                        debug_audio=False, tqdm_kwargs=None):
    """Helper to process a single replay file programmatically."""
    tqdm_kwargs = tqdm_kwargs or {}

    with open(input_path, "r", encoding="utf-8") as f:
        replay_data = json.load(f)

    # Setup Components
    config = AudioConfig(config_path)

    # LLM Enhancer
    api_key = os.getenv("GEMINI_API_KEY")
    enhancer = LLMEnhancer(api_key, prompt_path, cache_path, disabled=disable_llm)

    # TTS Generator
    if tts_provider == "gemini":
        tts = GeminiTTSGenerator(api_key, regions=config.vertex_ai_regions)
    else:
        model_name = config.get_vertex_model()
        regions = config.vertex_ai_regions
        tts = VertexTTSGenerator(model_name, regions=regions)

    manager = AudioManager(config, enhancer, tts, output_dir, tqdm_kwargs=tqdm_kwargs)

    setup_logger(output_dir=output_dir, base_name="add_audio")  # Ensure logger is setup for this process?
    # Actually, running in thread might share logger. 
    # But AudioManager uses logger.

    if debug_audio:
        manager.generate_debug_audio()
    else:
        manager.process_replay(replay_data)

    # Save cache if needed
    enhancer.save_cache()

