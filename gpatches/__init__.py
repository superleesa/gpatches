from typing import Any

from networkx import Graph
from pydantic import BaseModel


class ParamPatch(BaseModel):
    # TODO: add a child class for text diff / dict diff
    old_param_value: Any
    new_param_value: Any


class NodePatch(BaseModel):
    added_params: dict[str, Any]
    removed_params: dict[str, Any]
    changed_params: dict[str, ParamPatch]


class GraphPatch(BaseModel):
    # TODO: support edge changes

    added_nodes: dict[str, dict[str, Any]]
    removed_nodes: dict[str, dict[str, Any]]
    changed_nodes: dict[str, NodePatch]

    removed_edges: dict[tuple[str, str], dict[str, Any]]
    added_edges: dict[tuple[str, str], dict[str, Any]]


def diff_node(
    old_node_params: dict[str, Any], new_node_params: dict[str, Any]
) -> NodePatch:
    old_param_names = set(old_node_params.keys())
    new_param_names = set(new_node_params.keys())

    return NodePatch(
        added_params={
            param_name: new_node_params[param_name]
            for param_name in new_param_names - old_param_names
        },
        removed_params={
            param_name: old_node_params[param_name]
            for param_name in old_param_names - new_param_names
        },
        changed_params={
            param_name: ParamPatch(
                old_param_value=old_node_params[param_name],
                new_param_value=new_node_params[param_name],
            )
            for param_name in new_param_names & old_param_names
            if new_node_params[param_name] != old_node_params[param_name]
        },
    )


def diff_graphs(from_graph: Graph, to_graph: Graph) -> GraphPatch:
    """
    NOTE: Only supports directed graphs for now.
    """
    if not from_graph.is_directed() or not to_graph.is_directed():
        raise ValueError("Both from_graph and to_graph must be directed graphs.")

    return GraphPatch(
        removed_nodes={
            k: from_graph.nodes[k] for k in set(from_graph.nodes) - set(to_graph.nodes)
        },
        added_nodes={
            k: to_graph.nodes[k] for k in set(to_graph.nodes) - set(from_graph.nodes)
        },
        changed_nodes={
            k: diff_node(from_graph.nodes[k], to_graph.nodes[k])
            for k in set(from_graph.nodes) & set(to_graph.nodes)
            if from_graph.nodes[k] != to_graph.nodes[k]
        },
        removed_edges={
            k: from_graph.edges[k] for k in set(from_graph.edges) - set(to_graph.edges)
        },
        added_edges={
            k: to_graph.edges[k] for k in set(to_graph.edges) - set(from_graph.edges)
        },
    )
