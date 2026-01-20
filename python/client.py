#!/usr/bin/env python3
"""
Python client for the Spring‑Boot post‑box server.

Features
--------
* generate a fresh RSA key pair (or load an existing one)
* register a user (POST /auth/register)
* authenticate:
    - GET /auth/nonce?username=…
    - sign the nonce with the private key
    - POST /auth/token → receive a JWT
* optional helper to call a protected endpoint with the JWT

Adjust BASE_URL to point at your running server.
"""

import base64
import json
import sys
from pathlib import Path
from typing import Tuple

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec, utils
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

# ----------------------------------------------------------------------
# Configuration ---------------------------------------------------------
# ----------------------------------------------------------------------
USER_ID=102
BASE_URL = "http://localhost:8080"          # change if your server runs elsewhere
REGISTER_ENDPOINT = f"{BASE_URL}/user/create"
#NONCE_ENDPOINT = f"{BASE_URL}/auth/nonce"
NONCE_ENDPOINT_TEMPLATE =f"{BASE_URL}/auth/nonce/{{user_id}}"
TOKEN_ENDPOINT = f"{BASE_URL}/auth/token"

# Where to keep the generated key pair (PEM files).  Feel free to change.
KEY_DIR = Path("./keys")
PRIVATE_KEY_FILE = KEY_DIR / "private_key.pem"
PUBLIC_KEY_FILE = KEY_DIR / "public_key.pem"


# ----------------------------------------------------------------------
# Helper functions ------------------------------------------------------
# ----------------------------------------------------------------------
def ensure_key_dir():
    """Create the directory that will hold the PEM files."""
    KEY_DIR.mkdir(parents=True, exist_ok=True)


def generate_rsa_keypair(key_size: int = 2048) -> Tuple[bytes, bytes]:
    """
    Generate a fresh RSA key pair and return (private_pem, public_pem).

    The PEM strings are ready to be sent to the server (the server expects a
    PEM‑encoded *SubjectPublicKeyInfo* block, i.e. the classic
    -----BEGIN PUBLIC KEY----- format).
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    private_pem = private_key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
    )
    public_pem = private_key.public_key().public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def save_keys(private_pem: bytes, public_pem: bytes):
    """Write PEM files to disk (chmod 600 for the private key)."""
    ensure_key_dir()
    PRIVATE_KEY_FILE.write_bytes(private_pem)
    PUBLIC_KEY_FILE.write_bytes(public_pem)
    PRIVATE_KEY_FILE.chmod(0o600)  # restrict permissions


def load_private_key() -> rsa.RSAPrivateKey:
    """Load the RSA private key from the PEM file."""
    pem_data = PRIVATE_KEY_FILE.read_bytes()
    return serialization.load_pem_private_key(pem_data, password=None)


def load_public_key_pem() -> str:
    """Read the PEM‑encoded public key as a UTF‑8 string (to send to the server)."""
    return PUBLIC_KEY_FILE.read_text(encoding="utf-8")


def b64url_encode(data: bytes) -> str:
    """Base64‑URL‑encode without padding (the format the server expects)."""
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def b64url_decode(data_str: str) -> bytes:
    """Decode a Base64‑URL string that may be missing padding."""
    padding_needed = (4 - len(data_str) % 4) % 4
    data_str += "=" * padding_needed
    return base64.urlsafe_b64decode(data_str)


# ----------------------------------------------------------------------
# API interactions ------------------------------------------------------
# ----------------------------------------------------------------------
def register_user(username: str) -> bool:
    """
    Register a new user with the server.

    The request body expected by the server (according to the Java controller) is:
        { "username": "...", "password": "...", "publicKey": "-----BEGIN PUBLIC KEY-----\n..." }

    The password field is optional for a pure‑public‑key flow; we send an empty string.
    """
    payload = {
        "name": username,
        "bio": "default bio",                     # not used in the public‑key flow
        "publicKey": load_public_key_pem(),
    }
    print(payload)
    resp = requests.post(REGISTER_ENDPOINT, json=payload)
    if resp.status_code == 200:
        print(f"[+] User '{username}' registered successfully.")
        return True
    else:
        print(f"[!] Registration failed ({resp.status_code}): {resp.text}")
        return False


def get_nonce(userId:int) -> str:
    """GET /auth/nonce?username=… → returns the raw nonce string."""

    resp = requests.get(NONCE_ENDPOINT_TEMPLATE.format(user_id=userId))
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to obtain nonce: {resp.status_code} {resp.text}")

    data = resp.json()
    nonce = data.get("nonce")
    if not nonce:
        raise RuntimeError("Server response did not contain a 'nonce' field")
    print(f"[+] Received nonce: {nonce}")
    return nonce


def sign_nonce(private_key: rsa.RSAPrivateKey, nonce_b64url: str) -> str:
    """
    Sign the *raw* nonce bytes (the Base64‑URL string decoded) with RSA‑PKCS1‑v1_5 + SHA‑256.
    The server’s verification routine expects exactly this algorithm.
    """
    nonce_bytes = b64url_decode(nonce_b64url)

    signature = private_key.sign(
        data=nonce_bytes,
        padding=padding.PKCS1v15(),
        algorithm=hashes.SHA256(),
    )
    # Encode the signature the same way the server expects (Base64‑URL, no padding)
    sig_b64url = b64url_encode(signature)
    print(f"[+] Generated signature (Base64‑URL): {sig_b64url}")
    return sig_b64url


def exchange_token(userId: int, nonce: str, signature_b64url: str) -> str:
    """
    POST /auth/token with the three fields required by the server.
    On success the server returns a JSON object containing the JWT:
        { "accessToken": "<jwt>" }
    """
    payload = {
        "userId": userId,
        "nonce": nonce,
        "signature": signature_b64url,
    }
    resp = requests.post(TOKEN_ENDPOINT, json=payload)
    print("\n\n")
    print(payload)
    if resp.status_code != 200:
        raise RuntimeError(f"Token exchange failed ({resp.status_code}): {resp.text}")

    data = resp.json()
    token = data.get("accessToken")
    if not token:
        raise RuntimeError("Server response missing 'accessToken'")
    print(f"[+] Received JWT (truncated): {token[:40]}...")
    return token


def call_protected_endpoint(jwt: str, path: str = "/api/messages"):
    """
    Example of using the JWT to call a protected endpoint.
    Adjust the path to whatever your server exposes.
    """
    url = f"{BASE_URL}{path}"
    headers = {"Authorization": f"Bearer {jwt}"}
    resp = requests.get(url, headers=headers)
    print(f"[+] GET {path} → {resp.status_code}")
    print(resp.text)


# ----------------------------------------------------------------------
# Main workflow ---------------------------------------------------------
# ----------------------------------------------------------------------
def main():
    if len(sys.argv) < 3:
        print("Usage: python client_old.py <username> <action>")
        print("  actions: generate-keys | register | login | test")
        sys.exit(1)

    username = sys.argv[1]
    action = sys.argv[2]

    # --------------------------------------------------------------
    # 1️⃣ Generate a fresh RSA key pair (if needed)
    # --------------------------------------------------------------
    if action == "generate-keys":
        priv_pem, pub_pem = generate_rsa_keypair()
        save_keys(priv_pem, pub_pem)
        print("[+] RSA key pair generated and saved:")
        print(f"    private → {PRIVATE_KEY_FILE}")
        print(f"    public  → {PUBLIC_KEY_FILE}")
        return

    # --------------------------------------------------------------
    # 2️⃣ Register the user (must have a key pair already)
    # --------------------------------------------------------------
    if action == "register":
        if not PUBLIC_KEY_FILE.is_file():
            print("[!] No public key found – run 'generate-keys' first.")
            sys.exit(1)
        register_user(username)
        return

    # --------------------------------------------------------------
    # 3️⃣ Full login flow → obtain JWT
    # --------------------------------------------------------------
    if action == "login":
        if not PRIVATE_KEY_FILE.is_file():
            print("[!] No private key found – run 'generate-keys' first.")
            sys.exit(1)

        private_key = load_private_key()

        # a) ask server for a nonce
        nonce = get_nonce(USER_ID)

        # b) sign the nonce with our private key
        signature = sign_nonce(private_key, nonce)

        # c) exchange the signed nonce for a JWT
        jwt = exchange_token(USER_ID, nonce, signature)
        print(jwt)
        # d) store the JWT locally for later reuse (optional)
        token_path = KEY_DIR / f"{username}_jwt.txt"
        token_path.write_text(jwt, encoding="utf-8")
        print(f"[+] JWT saved to {token_path}")
        return

    # --------------------------------------------------------------
    # 4️⃣ Use the JWT to call a protected endpoint (demo)
    # --------------------------------------------------------------
    if action == "test":
        token_path = KEY_DIR / f"{username}_jwt.txt"
        if not token_path.is_file():
            print("[!] No saved JWT found – run 'login' first.")
            sys.exit(1)
        jwt = token_path.read_text(encoding="utf-8").strip()
        call_protected_endpoint(jwt)
        return

    print(f"[!] Unknown action: {action}")
    sys.exit(1)


if __name__ == "__main__":
    main()