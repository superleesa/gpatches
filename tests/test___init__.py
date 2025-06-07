import pytest

from gpatches import diff_graphs, ParamPatch, NodePatch
from gpatches import GraphPatch
from tests.helpers import create_graph_with_data


@pytest.mark.parametrize(
    "g1, g2, expected_diff",
    [
        pytest.param(
            # Added and removed nodes
            create_graph_with_data([("A", {"x": 1}), ("B", {"y": 2})], directed=True),
            create_graph_with_data([("B", {"y": 2}), ("C", {"z": 3})], directed=True),
            GraphPatch(
                added_nodes={"C": {"z": 3}},
                removed_nodes={"A": {"x": 1}},
                changed_nodes={},
                added_edges={},
                removed_edges={},
            ),
            id="added_and_removed_nodes",
        ),
        pytest.param(
            # No node or edge changes
            create_graph_with_data(
                [("A", {"foo": 1}), ("B", {"bar": 2})], directed=True
            ),
            create_graph_with_data(
                [("A", {"foo": 1}), ("B", {"bar": 2})], directed=True
            ),
            GraphPatch(
                added_nodes={},
                removed_nodes={},
                changed_nodes={},
                added_edges={},
                removed_edges={},
            ),
            id="no_changes",
        ),
        pytest.param(
            # Changed node params
            create_graph_with_data([("A", {"x": 1, "y": 2})], directed=True),
            create_graph_with_data([("A", {"x": 1, "y": 3, "z": 4})], directed=True),
            GraphPatch(
                added_nodes={},
                removed_nodes={},
                changed_nodes={
                    "A": NodePatch(
                        added_params={"z": 4},
                        removed_params={},
                        changed_params={
                            "y": ParamPatch(old_param_value=2, new_param_value=3)
                        },
                    )
                },
                added_edges={},
                removed_edges={},
            ),
            id="changed_node_params",
        ),
        pytest.param(
            # Added and removed edges
            # FIXME: should treated as changed edge in the future
            create_graph_with_data(
                [("A", {}), ("B", {})], edges=[("A", "B", {"weight": 1})], directed=True
            ),
            create_graph_with_data(
                [("A", {}), ("B", {})], edges=[("B", "A", {"weight": 2})], directed=True
            ),
            GraphPatch(
                added_nodes={},
                removed_nodes={},
                changed_nodes={},
                added_edges={("B", "A"): {"weight": 2}},
                removed_edges={("A", "B"): {"weight": 1}},
            ),
            id="added_and_removed_edges",
        ),
        pytest.param(
            # No edge changes
            create_graph_with_data(
                [("A", {}), ("B", {})], edges=[("A", "B", {"weight": 5})], directed=True
            ),
            create_graph_with_data(
                [("A", {}), ("B", {})], edges=[("A", "B", {"weight": 5})], directed=True
            ),
            GraphPatch(
                added_nodes={},
                removed_nodes={},
                changed_nodes={},
                added_edges={},
                removed_edges={},
            ),
            id="no_edge_changes",
        ),
    ],
)
def test_diff_graphs_api(g1, g2, expected_diff):
    diff = diff_graphs(g1, g2)
    assert diff == expected_diff


def test_diff_graphs_raises_on_undirected() -> None:
    g1 = create_graph_with_data([], directed=False)
    g2 = create_graph_with_data([], directed=True)
    with pytest.raises(ValueError):
        diff_graphs(g1, g2)
