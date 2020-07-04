import sys
import networkx as nx
from git import Repo, Git, IndexFile
import matplotlib.pyplot as plt
import os


def create_graph():
    dir_path = os.path.join(os.getenv("userprofile"), 'code', "cnn-explainer")
    repo = Repo(dir_path)
    print(dir_path)
    head_commit = repo.head.commit
    graph = nx.DiGraph()

    add_parent_chain_to_graph(graph, head_commit)
    print(list(graph.successors("7392f2d90373013dcd7c08b3db18379638680f7e")))
    pos = nx.spiral_layout(graph)
    options = {
        'node_color': 'blue',
        'node_size': 12,
        'width': 1,
        'arrow_size': 3,
        'with_labels': False,
        'pos': pos
    }

    nx.draw_networkx(graph,  **options)
    nx.write_gexf(graph, 'output.gexf')
    plt.show()


def add_parent_chain_to_graph(graph, rev):
    print('graph len is', len(graph), 'rev is ', rev.hexsha)
    print('short_sha', rev.hexsha[:5])
    print('committed_date', rev.committed_date)

    for parent in rev.parents:
        if graph.has_edge(rev.hexsha, parent.hexsha):
            print('edge already in graph')
            return
        graph.add_edge(rev.hexsha, parent.hexsha)
        add_parent_chain_to_graph(graph, parent)


if __name__ == '__main__':
    create_graph()
