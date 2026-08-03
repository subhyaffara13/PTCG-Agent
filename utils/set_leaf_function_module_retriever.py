from typing import Any, Callable

def set_leaf_function_module_retriever(retriever: Callable[[int], Any]) -> None:
    global _leaf_function_module_retriever
    _leaf_function_module_retriever = retriever

