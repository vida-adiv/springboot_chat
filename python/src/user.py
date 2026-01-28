import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa, ec, utils
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption

from typing import Tuple
from pathlib import Path
import yaml

class User:
       
    def __init__(self, userdir: str):
        self.userdir = userdir
        self.private_key_file = Path(userdir) / "private_key.pem"
        self.public_key_file = Path(userdir)/ "public_key.pem"

        # Load user data from YAML file
        yaml_path = Path(userdir) / "user_data.yaml"
        with open(yaml_path, 'r') as file:
            user_data = yaml.safe_load(file)

        self.id = user_data.get('id')
        self.name = user_data.get('name')
        self.bio = user_data.get('bio')

    
    def save_user_data(self):
        """Saves the user data to the user_data.yaml file."""
        yaml_path = Path(self.userdir) / "user_data.yaml"
        user_data = {
            'id': self.id,
            'name': self.name,
            'bio': self.bio
        }
        with open(yaml_path, 'w') as file:
            yaml.dump(user_data, file, default_flow_style=False)
    
    def save_keys(self, private_pem: bytes, public_pem: bytes):
        self.private_key_file.write_bytes(private_pem)
        self.public_key_file.write_bytes(public_pem)