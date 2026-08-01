
def get_verbose_details(manager):
    bits = []
    bits.append(header("Files in scope (%i):", len(manager.files_list)))
    tpl = "\t%s (score: {SEVERITY: %i, CONFIDENCE: %i})"
    bits.extend(
        [
            tpl % (item, sum(score["SEVERITY"]), sum(score["CONFIDENCE"]))
            for (item, score) in zip(manager.files_list, manager.scores)
        ]
    )
    bits.append(header("Files excluded (%i):", len(manager.excluded_files)))
    bits.extend([f"\t{fname}" for fname in manager.excluded_files])
    return "\n".join([str(bit) for bit in bits])


def get_verbose_details(manager):
    bits = []
    bits.append(f"Files in scope ({len(manager.files_list)}):")
    tpl = "\t%s (score: {SEVERITY: %i, CONFIDENCE: %i})"
    bits.extend(
        [
            tpl % (item, sum(score["SEVERITY"]), sum(score["CONFIDENCE"]))
            for (item, score) in zip(manager.files_list, manager.scores)
        ]
    )
    bits.append(f"Files excluded ({len(manager.excluded_files)}):")
    bits.extend([f"\t{fname}" for fname in manager.excluded_files])
    return "\n".join([bit for bit in bits])

