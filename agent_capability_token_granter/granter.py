"""Core Agent Capability Token Granter implementation."""
import hmac
import hashlib
import time
from typing import List, Dict, Any, Optional


class CapabilityToken:
    def __init__(self, token_id: str, tool_name: str, caveats: List[Dict[str, Any]], signature: str):
        self.token_id = token_id
        self.tool_name = tool_name
        self.caveats = caveats
        self.signature = signature


class AgentCapabilityTokenGranter:
    def __init__(self, root_secret: bytes):
        self.root_secret = root_secret

    def _sign(self, data: str) -> str:
        return hmac.new(self.root_secret, data.encode("utf-8"), hashlib.sha256).hexdigest()

    def mint_token(self, token_id: str, tool_name: str, caveats: Optional[List[Dict[str, Any]]] = None) -> CapabilityToken:
        cvs = list(caveats or [])
        serialized = f"{token_id}:{tool_name}:{cvs}"
        sig = self._sign(serialized)
        return CapabilityToken(token_id, tool_name, cvs, sig)

    def verify_and_authorize(self, token: CapabilityToken, requested_tool: str, context: Dict[str, Any]) -> bool:
        # 1. Signature validity
        serialized = f"{token.token_id}:{token.tool_name}:{token.caveats}"
        if not hmac.compare_digest(self._sign(serialized), token.signature):
            return False

        # 2. Tool match
        if token.tool_name != requested_tool and token.tool_name != "*":
            return False

        # 3. Check caveats
        now = time.time()
        for c in token.caveats:
            if c.get("type") == "expires_before" and now >= c.get("value", 0):
                return False
            if c.get("type") == "path_prefix":
                req_path = context.get("path", "")
                if not req_path.startswith(c.get("value", "")):
                    return False

        return True
