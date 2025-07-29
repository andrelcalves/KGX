import yaml
from exporters.cognite_exporter import CogniteDataModelExporter

def load_config():
    with open("config/config.yaml") as f:
        return yaml.safe_load(f)

def select_exporter():
    print("\nSelect the exporter source:")
    print("1 - Cognite Data Fusion")
    print("2 - Neo4j (coming soon)")
    print("3 - Azure Digital Twins (coming soon)")

    choice = input("Enter the number of the exporter to use: ").strip()

    if choice == "1":
        return "cognite"
    elif choice == "2":
        print("⚠️ Neo4j exporter is not implemented yet.")
        return None
    elif choice == "3":
        print("⚠️ Azure Digital Twins exporter is not implemented yet.")
        return None
    else:
        print("❌ Invalid choice.")
        return None

def run_cognite_export(config):
    space = input("Enter the space name: ").strip()
    model_id = input("Enter the data model ID: ").strip()
    version = input("Enter the version: ").strip()
    output_path = f"exported/{model_id}_v{version}.yaml"

    exporter = CogniteDataModelExporter(config)
    exporter.export_data_model(space, model_id, version, output_path)

if __name__ == "__main__":
    config = load_config()
    exporter_type = select_exporter()

    if exporter_type == "cognite":
        run_cognite_export(config)
