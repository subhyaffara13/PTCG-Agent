
def _parse_llm_results(results):
    if isinstance(results, dict) and "anti_patterns" in results:
        return results["anti_patterns"]
    elif isinstance(results, list): return results
    return [{"issue_name": "Parsing Error", "description": "LLM did not return a list."}]

