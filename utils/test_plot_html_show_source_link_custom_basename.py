
def test_plot_html_show_source_link_custom_basename(tmp_path):
    # Test that source link filename includes .py extension when using custom basename
    shutil.copyfile(tinypages / 'conf.py', tmp_path / 'conf.py')
    shutil.copytree(tinypages / '_static', tmp_path / '_static')
    doctree_dir = tmp_path / 'doctrees'
    (tmp_path / 'index.rst').write_text("""
.. plot::
    :filename-prefix: custom-name

    plt.plot(range(2))
""")
    html_dir = tmp_path / '_build' / 'html'
    build_sphinx_html(tmp_path, doctree_dir, html_dir)

    # Check that source file with .py extension is generated
    assert len(list(html_dir.glob("**/custom-name.py"))) == 1

    # Check that the HTML contains the correct link with .py extension
    html_content = (html_dir / 'index.html').read_text()
    assert 'custom-name.py' in html_content

