import yaml
from exporters.cognite_exporter import CogniteDataModelExporter
from loaders.neo4j_loader import Neo4jLoader

def load_config():
    with open("config/config.yaml") as f:
        config = yaml.safe_load(f)
        print("🔍 Loaded config keys:", list(config.keys()))  # Add this line
        return config

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

def select_target():
    print("\nSelect the **target** platform:")
    print("1 - Neo4j")
    print("2 - Azure Digital Twins")
    return input("Enter the number of the target: ").strip()

def run_cognite_export(config):
    space = input("Enter the space name: ").strip()
    model_id = input("Enter the data model ID: ").strip()
    version = input("Enter the version: ").strip()
    output_path = f"exported/{model_id}_v{version}.yaml"

    exporter = CogniteDataModelExporter(config)
    exporter.export_data_model(space, model_id, version, output_path)
    return output_path

def run_target_loader(target_choice, yaml_path):
    if target_choice == "1":
        print(f"👉 Neo4j loader would now read from {yaml_path}")
        # loader = Neo4jLoader()
        # loader.load_from_yaml(yaml_path)
    elif target_choice == "2":
        print(f"👉 Azure Digital Twin loader would now read from {yaml_path}")
        # loader = AzureDTLoader()
        # loader.load_from_yaml(yaml_path)
    else:
        print("❌ Invalid target selected.")

def run_target_loader(target_choice, yaml_path, config):
    if target_choice == "1":
        neo4j_config = config["neo4j"]
        uri = neo4j_config["uri"]
        user = neo4j_config["user"]
        password = neo4j_config["password"]

        loader = Neo4jLoader(uri, user, password)
        loader.load_from_yaml(yaml_path)
        loader.close()
    elif target_choice == "2":
        print(f"👉 Azure Digital Twin loader would now read from {yaml_path}")
    else:
        print("❌ Invalid target selected.")

if __name__ == "__main__":
    config = load_config()
    exporter_type = select_exporter()

    if exporter_type == "cognite":
          yaml_file_path = run_cognite_export(config)

    target_choice = select_target()
    run_target_loader(target_choice, yaml_file_path,config)