
def _createBitmapPlusMetricsMixin(metricsClass):
    # Both metrics names are listed here to make meaningful error messages.
    metricStrings = [BigGlyphMetrics.__name__, SmallGlyphMetrics.__name__]
    curMetricsName = metricsClass.__name__
    # Find which metrics this is for and determine the opposite name.
    metricsId = metricStrings.index(curMetricsName)
    oppositeMetricsName = metricStrings[1 - metricsId]

    class BitmapPlusMetricsMixin(object):
        def writeMetrics(self, writer, ttFont):
            self.metrics.toXML(writer, ttFont)

        def readMetrics(self, name, attrs, content, ttFont):
            for element in content:
                if not isinstance(element, tuple):
                    continue
                name, attrs, content = element
                if name == curMetricsName:
                    self.metrics = metricsClass()
                    self.metrics.fromXML(name, attrs, content, ttFont)
                elif name == oppositeMetricsName:
                    log.warning(
                        "Warning: %s being ignored in format %d.",
                        oppositeMetricsName,
                        self.getFormat(),
                    )

    return BitmapPlusMetricsMixin

