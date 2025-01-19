from interface.IAgent import IAgent
from src.AgentRole import AgentRole
from src.GloballyUniqueIdentifier import GloballyUniqueIdentifier
import uuid
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass(frozen=True)
class Agent(IAgent):
    """
    Represents a given agent (user, service account) in the system
    Attributes:
        agent_role (CodeScheme): The scheme associated with the code.
        agent_id (str): The globally unique identifier of the agent.
        agent_name (str): The name of the agent.
    Methods:
        role() -> AgentRole: Returns the role of the agent.
        value() -> str: Returns the name of the agent.
        id() -> str: Returns the ID of the agent.
    Static Methods:
        gen_agent_id() -> str: Generates a new globally unique agent ID.
    Static Methods:
        gen_base_code_value() -> str: Generates a new globally unique base code.
    """
    agent_role: AgentRole
    agent_id: str
    agent_name: str

    def __post_init__(self):
        if not isinstance(self.agent_role, AgentRole):
            raise ValueError(
                "Invalid role: must be an instance of AgentRole")
        if not isinstance(self.agent_name, str) or not self.agent_name:
            raise ValueError(
                "Invalid agent_name: must be a non-empty string")
        if not self.agent_id:
            raise ValueError(
                "Invalid agent_id: must be a non GUID")
        try:
            uuid.UUID(self.agent_id)
        except ValueError:
            raise ValueError("Invalid agent_id: must be a valid GUID")

    def role(self) -> AgentRole:
        return self.agent_role

    def value(self) -> str:
        return self.agent_name

    def id(self) -> str:
        return self.agent_id

    def has_required_permissions(self,
                                 required_role: AgentRole) -> bool:
        if not isinstance(required_role, AgentRole) or required_role is None:
            raise ValueError(
                f"Invalid {required_role}: must be an instance of AgentRole")
        return self.agent_role == required_role

    @staticmethod
    def gen_agent_id() -> str:
        return str(GloballyUniqueIdentifier())

    def __str__(self) -> str:
        return f"Name: {self.agent_name} : Id: {self.agent_id} : Role: {self.agent_role}"
