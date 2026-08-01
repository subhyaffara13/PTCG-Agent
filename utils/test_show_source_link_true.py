
def test_show_source_link_true(tmp_path, plot_html_show_source_link):
    # Test that a source link is generated if :show-source-link: is true,
    # whether or not plot_html_show_source_link is true.
    shutil.copyfile(tinypages / 'conf.py', tmp_path / 'conf.py')
    shutil.copytree(tinypages / '_static', tmp_path / '_static')
    doctree_dir = tmp_path / 'doctrees'
    (tmp_path / 'index.rst').write_text("""
.. plot::
    :show-source-link: true

    plt.plot(range(2))
""")
    html_dir = tmp_path / '_build' / 'html'
    build_sphinx_html(tmp_path, doctree_dir, html_dir, extra_args=[
        '-D', f'plot_html_show_source_link={plot_html_show_source_link}'])
    assert len(list(html_dir.glob("**/index-1.py"))) == 1

