from cognite.neat import NeatSession
from cognite.client import CogniteClient
from cognite.client.credentials import CredentialProvider, Token
from cognite.client.config import ClientConfig
from typing import Dict


class CogniteDataModelExporter:
    def __init__(self, config: Dict):
        self.project = config["cognite"]["project"]
        self.client_name = config["cognite"]["client_name"]
        self.auth_token_override = config["cognite"]["auth_token_override"]
        self.base_uri = config["cognite"]["base_uri"]

        self.client = self._init_cognite_client()

    @staticmethod
    def _create_credentials(self) -> CredentialProvider:
        return Token(str(self.auth_token_override))
        
    def _init_cognite_client(self) -> CogniteClient:

        return CogniteClient(ClientConfig(
            client_name=self.client_name,
            project=self.project,
            credentials=self._create_credentials(self),
            base_url=self.base_uri
        )
    )

    def export_data_model(self, space: str, model_id: str, version: str, output_path: str):
        neat =  NeatSession(self.client)
        neat.read.cdf.data_model(
            (space,
            model_id,
            version)
        )
        neat.to.yaml(output_path)
        print(f"✅ Exported Cognite data model to {output_path}")
