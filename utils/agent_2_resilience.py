
def agent_2_resilience(code_chunk):
    """Resilience & Logic Subagent"""
    prompt = (
        "You are Subagent 2: Resilience & Logic Lead for a PTCG AI.\n"
        "Your task is to review the following code and look specifically for:\n"
        "1. Missing error catches (e.g., bare try-except, missing try-except on IO/network).\n"
        "2. Circular loops or logic that might cause crashes.\n"
        "3. Anything that isn't up to par with a 'perfect' robust system.\n"
        "Be concise. If you find nothing critical, just say 'No major logic/resilience issues found.'\n\n"
        f"CODE:\n{code_chunk}"
    )
    if not client:
        return "Agent 2 Error: OPENAI_API_KEY environment variable is not set."
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Agent 2 Error: {e}"

