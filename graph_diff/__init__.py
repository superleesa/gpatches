from typing import Any

from networkx import Graph
from pydantic import BaseModel


class ParamDiff(BaseModel):
    # TODO: add a child class for text diff / dict diff
    old_param_value: Any
    new_param_value: Any


class NodeDiff(BaseModel):
    added_params: dict[str, Any]
    removed_params: dict[str, Any]
    changed_params: dict[str, ParamDiff]


class GraphDiff(BaseModel):
    # TODO: support edge changes

    added_nodes: dict[str, dict[str, Any]]
    removed_nodes: dict[str, dict[str, Any]]
    changed_nodes: dict[str, NodeDiff]

    removed_edges: dict[tuple[str, str], dict[str, Any]]
    added_edges: dict[tuple[str, str], dict[str, Any]]


def diff_node(
    old_node_params: dict[str, Any], new_node_params: dict[str, Any]
) -> NodeDiff:
    old_param_names = set(old_node_params.keys())
    new_param_names = set(new_node_params.keys())

    return NodeDiff(
        added_params={
            param_name: new_node_params[param_name]
            for param_name in new_param_names - old_param_names
        },
        removed_params={
            param_name: old_node_params[param_name]
            for param_name in old_param_names - new_param_names
        },
        changed_params={
            param_name: ParamDiff(
                old_param_value=old_node_params[param_name],
                new_param_value=new_node_params[param_name],
            )
            for param_name in new_param_names & old_param_names
            if new_node_params[param_name] != old_node_params[param_name]
        },
    )


def diff_graphs(old_graph: Graph, new_graph: Graph) -> GraphDiff:
    """
    NOTE: Only supports directed graphs for now.
    """
    if not old_graph.is_directed() or not new_graph.is_directed():
        raise ValueError("Both old_graph and new_graph must be directed graphs.")

    return GraphDiff(
        removed_nodes={
            k: old_graph.nodes[k] for k in set(old_graph.nodes) - set(new_graph.nodes)
        },
        added_nodes={
            k: new_graph.nodes[k] for k in set(new_graph.nodes) - set(old_graph.nodes)
        },
        changed_nodes={
            k: diff_node(old_graph.nodes[k], new_graph.nodes[k])
            for k in set(old_graph.nodes) & set(new_graph.nodes)
            if old_graph.nodes[k] != new_graph.nodes[k]
        },
        removed_edges={
            k: old_graph.edges[k] for k in set(old_graph.edges) - set(new_graph.edges)
        },
        added_edges={
            k: new_graph.edges[k] for k in set(new_graph.edges) - set(old_graph.edges)
        },
    )
