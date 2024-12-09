import networkx as nx

class GraphRAGAgent:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build_graph_from_documents(self, documents: str, topic: str) -> str:
        """Build a knowledge graph from the provided documents."""
        # Parse and extract entities and relationships (simplified example)
        for line in documents.split("\n"):
            if "relationship:" in line:
                parts = line.split("relationship:")
                entity1, entity2 = parts[0].strip(), parts[1].strip()
                self.graph.add_edge(entity1, entity2)

        # Enrich graph with additional topic-related nodes
        self.graph.add_node(topic, type="Topic")

        # Serialize the graph to a text-based format for RAG
        enriched_data = "Knowledge Graph:\n"
        for edge in self.graph.edges:
            enriched_data += f"{edge[0]} -> {edge[1]}\n"
        return enriched_data
