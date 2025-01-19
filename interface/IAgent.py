
from abc import ABC, abstractmethod
from src.AgentRole import AgentRole


class IAgent(ABC):
    @abstractmethod
    def role(self) -> AgentRole:
        raise NotImplementedError

    @abstractmethod
    def value(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def has_required_permissions(self, required_role: AgentRole) -> bool:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def gen_agent_id() -> str:
        raise NotImplementedError
