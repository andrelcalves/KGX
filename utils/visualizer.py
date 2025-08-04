
from pathlib import Path
import json
import yaml


def generate_html_graph_preview_from_yaml(yaml_file: str):
    """
    Generate an interactive HTML graph preview from a CDF NEAT-exported YAML file.
    The HTML is saved in the same directory as the input YAML, with a similar filename.

    Args:
        yaml_file (str): Path to the input YAML file.
    Returns:
        str: Path to the generated HTML file.
    """

    def parse_yaml_to_cytoscape_elements(yaml_path):
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)

        views = data.get("views", [])
        properties = data.get("properties", [])

        nodes = []
        node_ids = set()
        edges = []

        for view in views:
            view_id = view["view"]
            label = view.get("name") or view_id.split(":")[-1].split("(")[0]
            if view_id not in node_ids:
                nodes.append({"data": {"id": view_id, "label": label}})
                node_ids.add(view_id)

        for prop in properties:
            if prop.get("connection") == "direct":
                source_id = prop["view"]
                target_id = prop["value_type"]
                if source_id not in node_ids:
                    nodes.append({"data": {"id": source_id, "label": source_id}})
                    node_ids.add(source_id)
                if target_id not in node_ids:
                    nodes.append({"data": {"id": target_id, "label": target_id}})
                    node_ids.add(target_id)
                edges.append({
                    "data": {
                        "source": source_id,
                        "target": target_id,
                        "label": prop["name"]
                    }
                })

        return nodes + edges

    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
      <title>KGX Model Preview</title>
      <script src="https://unpkg.com/cytoscape/dist/cytoscape.min.js"></script>
      <style>
        #cy { width: 100%; height: 800px; border: 1px solid #ccc; }
      </style>
    </head>
    <body>
      <h2>KGX Model Preview</h2>
      <div id="cy"></div>
      <script>
        const cy = cytoscape({
          container: document.getElementById('cy'),
          elements: %%ELEMENTS_JSON%%,
          style: [
            {
              selector: 'node',
              style: {
                'background-color': '#007acc',
                'label': 'data(label)',
                'color': '#fff',
                'font-size': '8px',
                'text-valign': 'center',
                'text-halign': 'center',
                'text-outline-width': 1,
                'text-outline-color': '#007acc'
              }
            },
            {
              selector: 'edge',
              style: {
                'width': 2,
                'label': 'data(label)',
                'font-size': '6px',
                'line-color': '#ccc',
                'target-arrow-color': '#ccc',
                'target-arrow-shape': 'triangle'
              }
            }
          ],
          layout: {
            name: 'cose',
            animate: true
          }
        });
      </script>
    </body>
    </html>
    """

    elements = parse_yaml_to_cytoscape_elements(yaml_file)
    html_content = html_template.replace("%%ELEMENTS_JSON%%", json.dumps(elements, indent=2))

    html_file = Path(yaml_file).with_suffix(".html")
    Path(html_file).write_text(html_content)

    return str(html_file)
