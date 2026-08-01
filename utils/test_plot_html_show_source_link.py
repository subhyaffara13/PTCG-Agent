
def test_plot_html_show_source_link(tmp_path):
    shutil.copyfile(tinypages / 'conf.py', tmp_path / 'conf.py')
    shutil.copytree(tinypages / '_static', tmp_path / '_static')
    doctree_dir = tmp_path / 'doctrees'
    (tmp_path / 'index.rst').write_text("""
.. plot::

    plt.plot(range(2))
""")
    # Make sure source scripts are created by default
    html_dir1 = tmp_path / '_build' / 'html1'
    build_sphinx_html(tmp_path, doctree_dir, html_dir1)
    assert len(list(html_dir1.glob("**/index-1.py"))) == 1
    # Make sure source scripts are NOT created when
    # plot_html_show_source_link` is False
    html_dir2 = tmp_path / '_build' / 'html2'
    build_sphinx_html(tmp_path, doctree_dir, html_dir2,
                      extra_args=['-D', 'plot_html_show_source_link=0'])
    assert len(list(html_dir2.glob("**/index-1.py"))) == 0

