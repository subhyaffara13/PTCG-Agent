import itertools
import json
import os
import re
from typing import Optional
from pathlib import Path


def get_model_info(
    model: str,
    custom_llm_provider: Optional[str] = None,
    api_base: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ModelInfo:
    """
    Get a dict for the maximum tokens (context window), input_cost_per_token, output_cost_per_token  for a given model.

    Parameters:
    - model (str): The name of the model.
    - custom_llm_provider (str | null): the provider used for the model. If provided, used to check if the litellm model info is for that provider.

    Returns:
        dict: A dictionary containing the following information:
            key: Required[str] # the key in litellm.model_cost which is returned
            max_tokens: Required[Optional[int]]
            max_input_tokens: Required[Optional[int]]
            max_output_tokens: Required[Optional[int]]
            input_cost_per_token: Required[float]
            input_cost_per_character: Optional[float]  # only for vertex ai models
            input_cost_per_token_above_128k_tokens: Optional[float]  # only for vertex ai models
            input_cost_per_character_above_128k_tokens: Optional[
                float
            ]  # only for vertex ai models
            input_cost_per_query: Optional[float] # only for rerank models
            input_cost_per_image: Optional[float]  # only for vertex ai models
            input_cost_per_audio_token: Optional[float]
            input_cost_per_audio_per_second: Optional[float]  # only for vertex ai models
            input_cost_per_video_per_second: Optional[float]  # only for vertex ai models
            output_cost_per_token: Required[float]
            output_cost_per_audio_token: Optional[float]
            output_cost_per_character: Optional[float]  # only for vertex ai models
            output_cost_per_token_above_128k_tokens: Optional[
                float
            ]  # only for vertex ai models
            output_cost_per_character_above_128k_tokens: Optional[
                float
            ]  # only for vertex ai models
            output_cost_per_image: Optional[float]
            output_vector_size: Optional[int]
            output_cost_per_video_per_second: Optional[float]  # only for vertex ai models
            output_cost_per_audio_per_second: Optional[float]  # only for vertex ai models
            litellm_provider: Required[str]
            mode: Required[
                Literal[
                    "completion", "embedding", "image_generation", "chat", "audio_transcription"
                ]
            ]
            supported_openai_params: Required[Optional[List[str]]]
            supports_system_messages: Optional[bool]
            supports_response_schema: Optional[bool]
            supports_vision: Optional[bool]
            supports_function_calling: Optional[bool]
            supports_tool_choice: Optional[bool]
            supports_prompt_caching: Optional[bool]
            supports_audio_input: Optional[bool]
            supports_audio_output: Optional[bool]
            supports_pdf_input: Optional[bool]
            supports_web_search: Optional[bool]
            supports_url_context: Optional[bool]
            supports_reasoning: Optional[bool]
    Raises:
        Exception: If the model is not mapped yet.

    Example:
        >>> get_model_info("gpt-4")
        {
            "max_tokens": 8192,
            "input_cost_per_token": 0.00003,
            "output_cost_per_token": 0.00006,
            "litellm_provider": "openai",
            "mode": "chat",
            "supported_openai_params": ["temperature", "max_tokens", "top_p", "frequency_penalty", "presence_penalty"]
        }
    """
    # api_key is a per-caller credential, not part of the model identity, so it is
    # kept out of the cache key; explicit keys are resolved without the cache.
    if api_key is not None:
        return _build_model_info(model, custom_llm_provider, api_base, api_key)
    return _cached_get_model_info(model, custom_llm_provider, api_base)


def get_model_info(
        path_or_file,
        title=None,
        extra_file_size_limit=DEFAULT_EXTRA_FILE_SIZE_LIMIT):
    """Get JSON-friendly information about a model.

    The result is suitable for being saved as model_info.json,
    or passed to burn_in_info.
    """

    if isinstance(path_or_file, os.PathLike):
        default_title = os.fspath(path_or_file)
        file_size = path_or_file.stat().st_size  # type: ignore[attr-defined]
    elif isinstance(path_or_file, str):
        default_title = path_or_file
        file_size = Path(path_or_file).stat().st_size
    else:
        default_title = "buffer"
        path_or_file.seek(0, io.SEEK_END)
        file_size = path_or_file.tell()
        path_or_file.seek(0)

    title = title or default_title

    with zipfile.ZipFile(path_or_file) as zf:
        path_prefix = None
        zip_files = []
        # pyrefly: ignore [bad-assignment]
        for zi in zf.infolist():
            prefix = re.sub("/.*", "", zi.filename)
            if path_prefix is None:
                path_prefix = prefix
            elif prefix != path_prefix:
                raise Exception(f"Mismatched prefixes: {path_prefix} != {prefix}")  # noqa: TRY002
            zip_files.append(
                {
                    "filename": zi.filename,
                    "compression": zi.compress_type,
                    "compressed_size": zi.compress_size,
                    "file_size": zi.file_size,
                }
            )
        if path_prefix is None:
            raise AssertionError("path_prefix is None")
        version = zf.read(path_prefix + "/version").decode("utf-8").strip()

        def get_pickle(name):
            if path_prefix is None:
                raise AssertionError("path_prefix is None")
            with zf.open(path_prefix + f"/{name}.pkl") as handle:
                raw = torch.utils.show_pickle.DumpUnpickler(handle, catch_invalid_utf8=True).load()
                return hierarchical_pickle(raw)

        model_data = get_pickle("data")
        constants = get_pickle("constants")

        # Intern strings that are likely to be reused.
        # Pickle automatically detects shared structure,
        # so reused strings are stored efficiently.
        # However, JSON has no way of representing this,
        # so we have to do it manually.
        interned_strings : dict[str, int] = {}

        def intern(s):
            if s not in interned_strings:
                interned_strings[s] = len(interned_strings)
            return interned_strings[s]

        code_files = {}
        for zi in zf.infolist():
            if not zi.filename.endswith(".py"):
                continue
            with zf.open(zi) as handle:
                raw_code = handle.read()
            with zf.open(zi.filename + ".debug_pkl") as handle:
                raw_debug = handle.read()

            # Parse debug info and add begin/end markers if not present
            # to ensure that we cover the entire source code.
            debug_info_t = pickle.loads(raw_debug)
            text_table = None

            if (len(debug_info_t) == 3 and
                    isinstance(debug_info_t[0], str) and
                    debug_info_t[0] == 'FORMAT_WITH_STRING_TABLE'):
                _, text_table, content = debug_info_t

                def parse_new_format(line):
                    # (0, (('', '', 0), 0, 0))
                    num, ((text_indexes, fname_idx, offset), start, end), tag = line
                    text = ''.join(text_table[x] for x in text_indexes)  # type: ignore[index]
                    fname = text_table[fname_idx]  # type: ignore[index]
                    return num, ((text, fname, offset), start, end), tag

                debug_info_t = map(parse_new_format, content)

            debug_info = list(debug_info_t)
            if not debug_info:
                debug_info.append((0, (('', '', 0), 0, 0)))
            if debug_info[-1][0] != len(raw_code):
                debug_info.append((len(raw_code), (('', '', 0), 0, 0)))

            code_parts = []
            for di, di_next in itertools.pairwise(debug_info):
                start, source_range, *_ = di
                end = di_next[0]
                if end <= start:
                    raise AssertionError("end is not greater than start")
                source, s_start, s_end = source_range
                s_text, s_file, s_line = source
                # TODO: Handle this case better.  TorchScript ranges are in bytes,
                # but JS doesn't really handle byte strings.
                # if bytes and chars are not equivalent for this string,
                # zero out the ranges so we don't highlight the wrong thing.
                if len(s_text) != len(s_text.encode("utf-8")):
                    s_start = 0
                    s_end = 0
                text = raw_code[start:end]
                code_parts.append([text.decode("utf-8"), intern(s_file), s_line, intern(s_text), s_start, s_end])
            code_files[zi.filename] = code_parts

        extra_files_json_pattern = re.compile(re.escape(path_prefix) + "/extra/.*\\.json")
        extra_files_jsons = {}
        for zi in zf.infolist():
            if not extra_files_json_pattern.fullmatch(zi.filename):
                continue
            if zi.file_size > extra_file_size_limit:
                continue
            with zf.open(zi) as handle:
                try:
                    json_content = json.load(handle)
                    extra_files_jsons[zi.filename] = json_content
                except json.JSONDecodeError:
                    extra_files_jsons[zi.filename] = "INVALID JSON"

        always_render_pickles = {
            "bytecode.pkl",
        }
        extra_pickles = {}
        for zi in zf.infolist():
            if not zi.filename.endswith(".pkl"):
                continue
            with zf.open(zi) as handle:
                # TODO: handle errors here and just ignore the file?
                # NOTE: For a lot of these files (like bytecode),
                # we could get away with just unpickling, but this should be safer.
                obj = torch.utils.show_pickle.DumpUnpickler(handle, catch_invalid_utf8=True).load()
            buf = io.StringIO()
            pprint.pprint(obj, buf)
            contents = buf.getvalue()
            # Checked the rendered length instead of the file size
            # because pickles with shared structure can explode in size during rendering.
            if os.path.basename(zi.filename) not in always_render_pickles and \
                    len(contents) > extra_file_size_limit:
                continue
            extra_pickles[zi.filename] = contents

    return {
        "model": {
            "title": title,
            "file_size": file_size,
            "version": version,
            "zip_files": zip_files,
            "interned_strings": list(interned_strings),
            "code_files": code_files,
            "model_data": model_data,
            "constants": constants,
            "extra_files_jsons": extra_files_jsons,
            "extra_pickles": extra_pickles,
        }
    }


def get_model_info(token, model):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        client = HTTPHandler(concurrent_limit=1)
        response = client.get("https://api.together.xyz/models/info", headers=headers)
        if response.status_code == 200:
            model_info = response.json()
            for m in model_info:
                if m["name"].lower().strip() == model.strip():
                    return m["config"].get("prompt_format", None), m["config"].get(
                        "chat_template", None
                    )
            return None, None
        else:
            return None, None
    except Exception:  # safely fail a prompt template request
        return None, None

