
def test_plot_html_code_caption(tmp_path):
    # Test that :code-caption: option adds caption to code block
    shutil.copyfile(tinypages / 'conf.py', tmp_path / 'conf.py')
    shutil.copytree(tinypages / '_static', tmp_path / '_static')
    doctree_dir = tmp_path / 'doctrees'
    (tmp_path / 'index.rst').write_text("""
.. plot::
    :include-source:
    :code-caption: Example plotting code

    import matplotlib.pyplot as plt
    plt.plot([1, 2, 3], [1, 4, 9])
""")
    html_dir = tmp_path / '_build' / 'html'
    build_sphinx_html(tmp_path, doctree_dir, html_dir)

    # Check that the HTML contains the code caption
    html_content = (html_dir / 'index.html').read_text(encoding='utf-8')
    assert 'Example plotting code' in html_content
    # Verify the caption is associated with the code block
    # (appears in a caption element)
    assert '<p class="caption"' in html_content or 'caption' in html_content.lower()

