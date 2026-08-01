
def method_decorator_metaclass(function):
    class Decorated(type):
        def __new__(meta, classname, bases, classDict):
            for attributeName, attribute in classDict.items():
                if isinstance(attribute, types.FunctionType):
                    attribute = function(attribute)

                classDict[attributeName] = attribute
            return type.__new__(meta, classname, bases, classDict)
    return Decorated

