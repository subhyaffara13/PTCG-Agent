
def agent_1_architect(code_chunk):
    """Architecture & Dependencies Subagent"""
    prompt = (
        "You are Subagent 1: Architectural Lead for a PTCG (Pokémon Trading Card Game) AI.\n"
        "Your task is to review the following code and look specifically for:\n"
        "1. Circular imports or dependencies.\n"
        "2. Improper exports or redundant definitions (e.g. C++ Pybind modules).\n"
        "3. Anything that isn't up to par with a 'perfect' system architecture.\n"
        "Be concise. If you find nothing critical, just say 'No major architectural issues found.'\n\n"
        f"CODE:\n{code_chunk}"
    )
    if not client:
        return "Agent 1 Error: OPENAI_API_KEY environment variable is not set."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Agent 1 Error: {e}"

