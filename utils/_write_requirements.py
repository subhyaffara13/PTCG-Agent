
def _write_requirements(self, file):
    for req in _reqs.parse(self.install_requires):
        file.write(f"Requires-Dist: {req}\n")

    processed_extras = {}
    for augmented_extra, reqs in self.extras_require.items():
        # Historically, setuptools allows "augmented extras": `<extra>:<condition>`
        unsafe_extra, _, condition = augmented_extra.partition(":")
        unsafe_extra = unsafe_extra.strip()
        extra = _normalization.safe_extra(unsafe_extra)

        if extra:
            _write_provides_extra(file, processed_extras, extra, unsafe_extra)
        for req in _reqs.parse_strings(reqs):
            r = _include_extra(req, extra, condition.strip())
            file.write(f"Requires-Dist: {r}\n")

    return processed_extras


def _write_requirements(stream, reqs):
    lines = yield_lines(reqs or ())

    def append_cr(line):
        return line + '\n'

    lines = map(append_cr, lines)
    stream.writelines(lines)

