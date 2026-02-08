import requests
import yaml
import os
import my_utils
from pathlib import Path

class registrator:
    def __init__(self):
            print(1)
            with open("config.yaml", "r") as f:
                config = yaml.safe_load(f)
                self.base_url = config.get("base_url")

    def generate_user_dir(self, name:str):
        if not os.path.exists(name):
            os.makedirs(name)
        else:
            raise FileExistsError('Path already exists.')

    def load_keys_from_file(self, path: Path) -> tuple[str, str]:
        private_key_path = path / "private_key.pem"
        public_key_path = path / "public_key.pem"

        with open(private_key_path, 'r') as private_file:
            private_pem = private_file.read()

        with open(public_key_path, 'r') as public_file:
            public_pem = public_file.read()

        return private_pem, public_pem

    def register_user(self,name:str):
        path = Path("user/"+name)
        # Load keys from file
        private_pem, public_pem = self.load_keys_from_file(path)
        payload={
            "name": name,
            "bio" : "default bio",
            "publicKey": public_pem
        }
        resp = requests.post(self.base_url + "/user/create", json=payload, timeout=3)
        if resp.status_code == 200:
            print(f"[+] User '{name}' registered successfully.")
            user_data = resp.json()
            # Save the user data to a YAML file
            yaml_path = path / "user_data.yaml"
            with open(yaml_path, 'w') as f:
                yaml.dump(user_data, f)
            return True
        else:
            print(f"[!] Registration failed ({resp.status_code}): {resp.text}")
            return False

                
             
        