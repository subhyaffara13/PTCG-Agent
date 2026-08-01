
def patch_graphviz() -> None:
  """Fix `graphviz` display on Colab.

  By default, graphviz object raises an error when displayed on Colab:

  ```
  ExecutableNotFound: failed to execute ['dot', '-Tsvg'], make sure the
  Graphviz executables are on your systems' PATH
  ```

  Calling this function fix the behavior.
  """
  # pylint: disable=g-import-not-at-top
  # pytype: disable=import-error
  from colabtools import proto
  from colabtools import publish
  from colabtools import stubby

  import graphviz
  # pytype: enable=import-error
  # pylint: enable=g-import-not-at-top

  request_proto_cls = proto.GetProtoClass('graphviz_server.RenderRequest')
  graph_proto_cls = proto.GetProtoClass('graphviz_server.Graph')

  def _ipython_display_(self):
    graph = graph_proto_cls()
    graph.dot = self.source
    response = stubby.Call(
        'blade:graphviz-server',
        'RenderServer.Render',
        request_proto_cls(graph=graph),
    )
    publish.html(response.rendered_graph.rendered_bytes)

  graphviz.Digraph._ipython_display_ = _ipython_display_  # pylint: disable=protected-access

