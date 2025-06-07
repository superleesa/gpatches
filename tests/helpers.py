import networkx as nx


def create_graph_with_data(
    nodes: list[tuple[str | int, dict]],
    edges: list[tuple[str | int, str | int, dict | None]] | None = None,
    directed: bool = False,
    multigraph: bool = False,
) -> nx.Graph:
    """
    Create a NetworkX graph with nodes and edges including attributes.
    """
    if multigraph and directed:
        G = nx.MultiDiGraph()
    elif multigraph:
        G = nx.MultiGraph()
    elif directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()

    G.add_nodes_from(nodes)

    if edges:
        G.add_edges_from(
            [
                (u, v, attrs if attrs else {})
                for u, v, *rest in edges
                for attrs in [rest[0] if rest else {}]
            ]
        )

    return G
