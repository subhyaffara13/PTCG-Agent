
def test_dist_fetch_build_egg(tmpdir, setuptools_wheel):
    """
    Check multiple calls to `Distribution.fetch_build_egg` work as expected.
    """
    index = tmpdir.mkdir('index')
    index_url = urllib.parse.urljoin('file://', urllib.request.pathname2url(str(index)))

    def sdist_with_index(distname, version):
        dist_dir = index.mkdir(distname)
        dist_sdist = f'{distname}-{version}.tar.gz'
        make_trivial_sdist(
            str(dist_dir.join(dist_sdist)), distname, version, setuptools_wheel
        )
        with dist_dir.join('index.html').open('w') as fp:
            fp.write(
                DALS(
                    """
                <!DOCTYPE html><html><body>
                <a href="{dist_sdist}" rel="internal">{dist_sdist}</a><br/>
                </body></html>
                """
                ).format(dist_sdist=dist_sdist)
            )

    sdist_with_index('barbazquux', '3.2.0')
    sdist_with_index('barbazquux-runner', '2.11.1')
    with tmpdir.join('setup.cfg').open('w') as fp:
        fp.write(
            DALS(
                """
            [easy_install]
            index_url = {index_url}
            """
            ).format(index_url=index_url)
        )
    reqs = """
    barbazquux-runner
    barbazquux
    """.split()
    with tmpdir.as_cwd():
        dist = Distribution()
        dist.parse_config_files()
        resolved_dists = [dist.fetch_build_egg(r) for r in reqs]
    assert [dist.name for dist in resolved_dists if dist] == reqs

