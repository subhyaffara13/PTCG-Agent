
def _force_ep_signature_match(ep_guards_code: list[str], input_paths):
    # TODO (tmanlaibaatar)
    # This is band-aid solution to export new tracer replacing
    # shape env sources to flat_args. The real fix should be replacing
    # shape env sources to original user sources but this is quite
    # involved because you need to carefully construct new sources using
    # dynamo and replace all instances of it inside shape env. But it is
    # lot easier to manipulate after we turn them into strings and only
    # time we use these guards is during retracing or running exported program,
    # so it is probably ok to have "not useful" guards on ep for now.
    name_mapping = {}
    for idx, path in enumerate(input_paths):
        name_mapping[f"L['flat_args'][{idx}]"] = f"L{pytree.keystr(path)}"

    new_guards_code = []
    for guard in ep_guards_code:
        for old_name, new_name in name_mapping.items():
            guard = guard.replace(old_name, new_name)
        new_guards_code.append(guard)

    return new_guards_code

