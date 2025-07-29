from cognite.neat.graph.extractors.data_model_extractor import DataModelExtractor
from cognite.client import CogniteClient
from cognite.client.credentials import OAuthClientCredentials
from cognite.client.config import ClientConfig
from typing import Dict


class CogniteDataModelExporter:
    def __init__(self, config: Dict):
        self.project = config["cognite"]["project"]
        self.client_id = config["cognite"]["client_id"]
        self.client_secret = config["cognite"]["client_secret"]
        self.token_url = config["cognite"]["token_url"]

        self.client = self._init_cognite_client()

    def _init_cognite_client(self) -> CogniteClient:
        credentials = OAuthClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_url=self.token_url,
        )
        return CogniteClient(ClientConfig(
            client_name="graphbridge-cognite",
            project=self.project,
            credentials=credentials
        ))

    def export_data_model(self, space: str, model_id: str, version: str, output_path: str):
        extractor = DataModelExtractor(cognite_client=self.client)
        data_model_graph = extractor.extract_data_model_graph(
            space=space,
            external_id=model_id,
            version=version,
        )
        data_model_graph.to_yaml_file(output_path)
        print(f"✅ Exported Cognite data model to {output_path}")
