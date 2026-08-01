
def process_results(profile_file, args):
    profile_records = load_profile_json(profile_file)

    lines = parse_kernel_results(profile_records, args.threshold)

    lines += parse_node_results(profile_records, args.kernel_time_only, args.threshold)

    lines += group_node_results(profile_records)

    return lines

