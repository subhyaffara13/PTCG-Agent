"""
cb_agents/base_agent.py

Defines the BaseAgent class that all Player and Opponent modeling agents inherit from.
This ensures a unified interface structure across the entire codebase.
"""

from typing import Any

class BaseAgent:
    def __init__(self, perspective_flag: str):
        """
        Initializes the agent.
        
        Parameters
        ----------
        perspective_flag : str
            Either 'player' or 'opponent' to mark state ownership.
        """
        self.perspective_flag = perspective_flag

    def receive(self, packet: Any) -> Any:
        """
        Processes an incoming packet and returns a response.
        Must be implemented by child classes.
        """
        raise NotImplementedError("Subclasses must implement receive()")
