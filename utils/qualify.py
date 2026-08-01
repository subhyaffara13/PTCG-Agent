
def qualify(quals, replace_with):
    if quals & Q_CONST:
        replace_with = ' const ' + replace_with.lstrip()
    if quals & Q_VOLATILE:
        replace_with = ' volatile ' + replace_with.lstrip()
    if quals & Q_RESTRICT:
        # It seems that __restrict is supported by gcc and msvc.
        # If you hit some different compiler, add a #define in
        # _cffi_include.h for it (and in its copies, documented there)
        replace_with = ' __restrict ' + replace_with.lstrip()
    return replace_with

