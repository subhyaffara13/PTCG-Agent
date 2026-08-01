
def collect_cost_summary(env) -> CostSummary:
    cost_summary = CostSummary()

    for agent_config in env.configuration.agents:
        player_id = agent_config["id"]
        agent_id = agent_config["agent_id"]

        agent_cost_summary = AgentCostSummary(agent_config=agent_config)

        if isinstance(agents.get(agent_id), AgentFactoryWrapper) and issubclass(
            agents[agent_id].agent_class, LLMWerewolfAgent
        ):
            agent_instance = agents[agent_id].get_instance(player_id)
            if agent_instance:
                cost_tracker = agent_instance.cost_tracker
                agent_cost = AgentCost(
                    total_cost=cost_tracker.query_token_cost.total_costs_usd,
                    prompt_tokens=cost_tracker.prompt_token_cost.total_tokens,
                    completion_tokens=cost_tracker.completion_token_cost.total_tokens,
                )
                agent_cost_summary.costs = agent_cost
                agent_cost_summary.data = cost_tracker

                cost_summary.total_cost += agent_cost.total_cost
                cost_summary.total_prompt_tokens += agent_cost.prompt_tokens
                cost_summary.total_completion_tokens += agent_cost.completion_tokens

        cost_summary.cost_per_agent.append(agent_cost_summary)

    cost_summary.total_tokens = cost_summary.total_prompt_tokens + cost_summary.total_completion_tokens
    return cost_summary

