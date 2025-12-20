#!/usr/bin/env python3
"""
Demo client for the Spring‑Boot User API.

Endpoints (as defined in the Java controller):
    POST  /user/add?name=<name>&bio=<bio>
    GET   /users
"""

import json
import sys
from typing import Any, Dict, List

import requests

# ----------------------------------------------------------------------
# Configuration – change these if your server runs elsewhere
# ----------------------------------------------------------------------
BASE_URL = "http://localhost:8080"   # <-- adjust host/port if needed
TIMEOUT = 5                         # seconds for each request


def _handle_response(resp: requests.Response) -> Any:
    """
    Helper that raises for HTTP errors and returns JSON (or text) payload.
    """
    try:
        resp.raise_for_status()
    except requests.HTTPError as exc:
        print(f"❌ HTTP error {resp.status_code}: {resp.text}", file=sys.stderr)
        raise exc

    # Try to decode JSON; fall back to raw text if not JSON.
    try:
        return resp.json()
    except ValueError:
        return resp.text
def send_message(message: Dict[str, Any]) -> Dict[str, Any]:
    """
    POST a Message JSON to /msg.

    Parameters
    ----------
    message: dict
        Must contain the fields expected by your `Message` entity.
        Typical example (feel free to adjust):
        {
            "sender": "alice@example.com",
            "rec": 42,
            "content": "Hello, world!",
            "timestamp": "2025-12-17T12:00:00Z"
        }

    Returns
    -------
    dict
        The deserialized `MessageResponse` returned by the server,
        e.g. {"status":200,"message":"saved"}.
    """
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    resp = requests.post(
        f"{BASE_URL}/msg",
        headers=headers,
        json=message,
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()

def create_user(name: str, bio: str) -> str:
    """
    Calls POST /user/add?name=…&bio=…
    Returns the plain‑text response from the server (e.g. "saved").
    """
    url = f"{BASE_URL}/user/add"
    params = {"name": name, "bio": bio}
    print(f"▶️  Creating user '{name}' …")
    resp = requests.post(url, params=params, timeout=TIMEOUT)
    return _handle_response(resp)


def get_all_users() -> List[Dict[str, Any]]:
    """
    Calls GET /users and returns the list of user objects.
    Each object is whatever fields your `User` entity exposes
    (typically id, name, bio, …).
    """
    url = f"{BASE_URL}/users"
    print("▶️  Fetching all users …")
    resp = requests.get(url, timeout=TIMEOUT)
    return _handle_response(resp)


def pretty_print_json(data: Any) -> None:
    """Print JSON data with indentation."""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main() -> None:
    # ------------------------------------------------------------------
    # Example workflow – feel free to modify / extend
    # ------------------------------------------------------------------
    try:
        # 1️⃣ Create a new user (change the values as you like)
        payload = {
            "rec": 2,
            "msg": "another test message"

        }
        result = send_message(payload)
        print(f"✅ Server response: {result}")

        # 2️⃣ Retrieve the full list of users
        users = get_all_users()
        print("\n📋 Current users in the system:")
        pretty_print_json(users)

    except Exception as e:
        print(f"\n🚨 Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()