import os
import subprocess
import sys

def _fetch_build_egg_no_warn(dist, req):  # noqa: C901  # is too complex (16)  # FIXME
    # Ignore environment markers; if supplied, it is required.
    req = strip_marker(req)
    # Take easy_install options into account, but do not override relevant
    # pip environment variables (like PIP_INDEX_URL or PIP_QUIET); they'll
    # take precedence.
    opts = dist.get_option_dict('easy_install')
    if 'allow_hosts' in opts:
        raise DistutilsError(
            'the `allow-hosts` option is not supported '
            'when using pip to install requirements.'
        )
    quiet = 'PIP_QUIET' not in os.environ and 'PIP_VERBOSE' not in os.environ
    if 'PIP_INDEX_URL' in os.environ:
        index_url = None
    elif 'index_url' in opts:
        index_url = opts['index_url'][1]
    else:
        index_url = None
    find_links = (
        _fixup_find_links(opts['find_links'][1])[:] if 'find_links' in opts else []
    )
    if dist.dependency_links:
        find_links.extend(dist.dependency_links)
    eggs_dir = os.path.realpath(dist.get_egg_cache_dir())
    cached_dists = metadata.Distribution.discover(path=glob.glob(f'{eggs_dir}/*.egg'))
    for egg_dist in cached_dists:
        if _dist_matches_req(egg_dist, req):
            return egg_dist
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            sys.executable,
            '-m',
            'pip',
            '--disable-pip-version-check',
            'wheel',
            '--no-deps',
            '-w',
            tmpdir,
        ]
        if quiet:
            cmd.append('--quiet')
        if index_url is not None:
            cmd.extend(('--index-url', index_url))
        for link in find_links or []:
            cmd.extend(('--find-links', link))
        # If requirement is a PEP 508 direct URL, directly pass
        # the URL to pip, as `req @ url` does not work on the
        # command line.
        cmd.append(req.url or str(req))
        try:
            subprocess.check_call(cmd)
        except subprocess.CalledProcessError as e:
            raise DistutilsError(str(e)) from e
        wheel = Wheel(glob.glob(os.path.join(tmpdir, '*.whl'))[0])
        dist_location = os.path.join(eggs_dir, wheel.egg_name())
        wheel.install_as_egg(dist_location)
        return metadata.Distribution.at(dist_location + '/EGG-INFO')

