import unittest
from src.Agent import Agent
from src.AgentRole import AgentRole


class TestAgent(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.agent_maint = Agent(agent_id=Agent.gen_agent_id(),
                                agent_name="Test Maint Agent",
                                agent_role=AgentRole.MAINTAINER)
        cls.agent_reader = Agent(agent_id=Agent.gen_agent_id(),
                                 agent_name="Test Reader Agent",
                                 agent_role=AgentRole.READER)

    def test_create_fail(self):
        with self.assertRaises(ValueError):
            _ = Agent(agent_id=None,
                      agent_name="TestAgent",
                      agent_role=AgentRole.READER)
        with self.assertRaises(ValueError):
            _ = Agent(agent_id=Agent.gen_agent_id(),
                      agent_name=None,
                      agent_role=AgentRole.READER)
        with self.assertRaises(ValueError):
            _ = Agent(agent_id=Agent,
                      agent_name="TestAgent",
                      agent_role=None)
        with self.assertRaises(ValueError):
            _ = Agent(agent_id="xr5h7wewerer-sdfsd-sdf-sdf-sdf",  # Invalid GUID
                      agent_name="TestAgent",
                      agent_role=AgentRole.READER)
        with self.assertRaises(ValueError):
            _ = Agent(agent_id=Agent.gen_agent_id(),
                      agent_name=int(5),  # Invalid name
                      agent_role=AgentRole.READER)
        with self.assertRaises(ValueError):
            _ = Agent(agent_id=Agent,
                      agent_name="TestAgent",
                      agent_role=str("BadRoleTypeAsNotTypeAgentRole"),
                      )

    def test_create(self):
        self.assertEqual(self.agent_maint.id(), self.agent_maint.agent_id)
        self.assertEqual(self.agent_maint.value(), self.agent_maint.agent_name)
        self.assertEqual(self.agent_maint.role(), self.agent_maint.agent_role)

    def test_equality(self):
        self.assertEqual(self.agent_reader, self.agent_reader)
        self.assertNotEqual(self.agent_reader, self.agent_maint)

    def test_has_required_permissions(self):
        self.assertTrue(self.agent_reader.has_required_permissions(AgentRole.READER))
        self.assertFalse(
            self.agent_reader.has_required_permissions(AgentRole.MAINTAINER))
        with self.assertRaises(ValueError):
            self.assertFalse(self.agent_maint.has_required_permissions(None))
        with self.assertRaises(ValueError):
            self.assertFalse(
                self.agent_maint.has_required_permissions(str("NotAgentRole")))
