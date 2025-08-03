import yaml
import re
from neo4j import GraphDatabase
from collections import defaultdict


class Neo4jLoader:
    def __init__(self, uri: str, user: str, password: str):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_from_yaml(self, yaml_file: str):
        with open(yaml_file, "r") as f:
            data = yaml.safe_load(f)

        views = data.get("views", [])
        properties = data.get("properties", [])

        print(f"🔍 Found {len(views)} views and {len(properties)} properties in YAML.")

        prop_map = defaultdict(list)
        for prop in properties:
            if "view" in prop:
                prop_map[prop["view"]].append(prop)

        with self.driver.session() as session:
            for view in views:
                view_id = view["view"]

                # Rule 1: Skip CogniteDescribable itself
                if view_id == "cdf_cdm:CogniteDescribable(version=v1)":
                    print(f"⛔ Skipping base view: {view_id}")
                    continue

                # Derive fallback label from view_id if 'name' is missing
                match = re.match(r"[^:]+:([^(\s]+)", view_id)
                fallback_label = match.group(1) if match else view_id
                label = view.get("name", fallback_label)
                description = view.get("description", "")
                props = prop_map.get(view_id, [])

                # Rule 2: Add schema props if it implements CogniteDescribable
                if view.get("implements") == "cdf_cdm:CogniteDescribable(version=v1)":
                    print(f"✨ Adding schema properties 'name' and 'description' to: {view_id}")
                    props.append({"name": "name", "value_type": "text"})
                    props.append({"name": "description", "value_type": "text"})

                print(f"🧱 Creating node: {view_id} - {label}")
                session.write_transaction(self._create_node, view_id, label, description, props)

            for prop in properties:
                if prop.get("connection") == "direct":
                    source_id = prop["view"]
                    target_id = prop["value_type"]

                    if source_id == "cdf_cdm:CogniteDescribable(version=v1)" or \
                       target_id == "cdf_cdm:CogniteDescribable(version=v1)":
                        print(f"⛔ Skipping relationship to/from excluded node: {source_id} -> {target_id}")
                        continue

                    rel_type = prop["name"]
                    print(f"🔗 Creating relationship: {source_id} -[{rel_type}]-> {target_id}")
                    session.write_transaction(self._create_relationship, source_id, target_id, rel_type)

    @staticmethod
    def _create_node(tx, node_id: str, label: str, description: str, props: list):
        parameters = {
            "id": node_id,
            "label": label,
            "name": label,
            "description": description,
        }

        prop_assignments = [
            "n.label = $label",
            "n.name = $name",
            "n.description = $description"
        ]

        for prop in props:
            if "name" not in prop:
                print(f"⚠️ Skipping property without a name in node {node_id}")
                continue

            key = prop["name"]

            # Avoid overwriting name or description
            if key in ["name", "description"]:
                continue

            value_type = prop.get("value_type", "text")
            dummy_value = f"<{value_type}>"
            parameters[key] = dummy_value
            prop_assignments.append(f"n.{key} = ${key}")

        prop_string = ",\n        ".join(prop_assignments)

        query = f"""
        MERGE (n:GraphNode {{id: $id}})
        SET {prop_string}
        """
        tx.run(query, **parameters)

    @staticmethod
    def _create_relationship(tx, source_id: str, target_id: str, rel_type: str):
        query = """
        MATCH (a:GraphNode {id: $source_id})
        MATCH (b:GraphNode {id: $target_id})
        MERGE (a)-[r:CONNECTED {type: $type}]->(b)
        """
        tx.run(query, source_id=source_id, target_id=target_id, type=rel_type)
