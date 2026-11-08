"""CLI for agent-capability-token-granter."""
import sys
import argparse
import time
from .granter import AgentCapabilityTokenGranter


def main():
    parser = argparse.ArgumentParser(description="Agent Capability Token Granter CLI")
    parser.add_argument("--demo", action="store_true", help="Run capability token demo")
    args = parser.parse_args()

    if args.demo:
        granter = AgentCapabilityTokenGranter(b"secret_master_key_123")
        token = granter.mint_token("tok-01", "read_file", [
            {"type": "path_prefix", "value": "/safe/workspace"},
            {"type": "expires_before", "value": time.time() + 60.0}
        ])

        v1 = granter.verify_and_authorize(token, "read_file", {"path": "/safe/workspace/main.py"})
        v2 = granter.verify_and_authorize(token, "read_file", {"path": "/etc/shadow"})
        print(f"[+] Authorized call within prefix: {v1}")
        print(f"[*] Unauthorized call outside prefix: {v2} (Correctly rejected!)")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
