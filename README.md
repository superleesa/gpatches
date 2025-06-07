# gpatches

A tool to diff two graphs. This library helps you identify changes between two networkx graphs including added/removed nodes, changed node parameters, and added/removed edges.

## Installation

```
pip install gpatches
```

## Usage

```python
import networkx as nx
from gpatches import diff_graphs

G1 = nx.DiGraph()
G1.add_node("A", x=1, y=2)
G1.add_node("B", foo="bar")
G1.add_edge("A", "B", weight=5)

G2 = nx.DiGraph()
G2.add_node("A", x=1, y=3, z=4)  # Changed y value and added z parameter
G2.add_node("C", color="blue")   # New node
G2.add_edge("A", "C", weight=2)  # New edge

# Diff the graphs
patches = diff_graphs(G1, G2)
print(patches)
```

The output from the above example would be:

```python
GraphPatch(
    added_nodes={'C': {'color': 'blue'}},
    removed_nodes={'B': {'foo': 'bar'}},
    changed_nodes={
        'A': NodePatch(
            added_params={'z': 4},
            removed_params={},
            changed_params={'y': ParamPatch(old_param_value=2, new_param_value=3)}
        )
    },
    removed_edges={('A', 'B'): {'weight': 5}},
    added_edges={('A', 'C'): {'weight': 2}}
)
```
