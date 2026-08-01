
def test_edge_views_inherit_from_EdgeViewABC():
    all_edge_view_classes = (v for v in dir(nx.reportviews) if "Edge" in v)
    for eview_class in all_edge_view_classes:
        assert issubclass(
            getattr(nx.reportviews, eview_class), nx.reportviews.EdgeViewABC
        )

