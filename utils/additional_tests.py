import os

def additional_tests(suite=None, project_dir=None):
    import simplejson
    import simplejson.encoder
    import simplejson.decoder

    if suite is None:
        suite = unittest.TestSuite()
    import doctest
    for mod in (simplejson, simplejson.encoder, simplejson.decoder):
        suite.addTest(doctest.DocTestSuite(mod))
    if project_dir is not None:
        suite.addTest(
            doctest.DocFileSuite(
                os.path.join(project_dir, "index.rst"), module_relative=False
            )
        )
    return suite

