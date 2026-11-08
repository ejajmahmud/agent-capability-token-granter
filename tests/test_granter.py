"""Unit tests for agent-capability-token-granter."""
import unittest
import time
from agent_capability_token_granter.granter import AgentCapabilityTokenGranter


class TestAgentCapabilityTokenGranter(unittest.TestCase):
    def setUp(self):
        self.granter = AgentCapabilityTokenGranter(b"test_key")

    def test_valid_authorization(self):
        token = self.granter.mint_token("t1", "query_db", [
            {"type": "path_prefix", "value": "public."}
        ])
        auth = self.granter.verify_and_authorize(token, "query_db", {"path": "public.users"})
        self.assertTrue(auth)

    def test_prefix_violation(self):
        token = self.granter.mint_token("t1", "query_db", [
            {"type": "path_prefix", "value": "public."}
        ])
        auth = self.granter.verify_and_authorize(token, "query_db", {"path": "private.secrets"})
        self.assertFalse(auth)
