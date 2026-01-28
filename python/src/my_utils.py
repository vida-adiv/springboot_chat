from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
from typing import Tuple
import os

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
    print("keys generated")
    return private_pem, public_pem

def generate_user_dir(name:str):
    if not os.path.exists(name):
        os.makedirs(name)

def save_keys(path:Path,private_pem: bytes, public_pem: bytes):
        generate_user_dir(path)
        private_key_file=path/"private_key.pem"
        public_key_file=path/"public_key.pem"
        private_key_file.write_bytes(private_pem)
        public_key_file.write_bytes(public_pem)
