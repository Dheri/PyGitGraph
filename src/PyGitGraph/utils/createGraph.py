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

    # print(repo.references)
    for ref in repo.references:
        print(ref.commit, ref)
        add_parent_chain_to_graph(graph, ref.commit)

    # add_parent_chain_to_graph(graph, head_commit)
    print('graph.nodes list', list(graph.nodes))
    # for node in graph.nodes:
    #     print(node)
    # print(list(graph.successors("7392f2d90373013dcd7c08b3db18379638680f7e")))
    pos = nx.spring_layout(graph, weight='weight')
    options = {
        'node_color': 'orange',
        'node_size': 2,
        'width': 1,
        'arrow_size': 3,
        'with_labels': False,
        'pos': pos
    }
    print('number_of_nodes', graph.number_of_nodes())
    print(list(graph.edges(data=True)))

    nx.draw_networkx(graph, **options)
    nx.write_gexf(graph, 'output.gexf')
    plt.show()


def add_parent_chain_to_graph(graph, rev):
    print('graph len is', len(graph), 'rev is ', rev.hexsha)
    print('short_sha', rev.hexsha, 'committed_date', rev.committed_date)

    for parent in rev.parents:
        if graph.has_edge(rev.hexsha, parent.hexsha):
            print('edge already in graph')
            return
        # weight = (len(graph) % 24) + 1
        weight = 1
        print('weight: ', weight)
        graph.add_edge(rev.hexsha, parent.hexsha, weight=weight)
        add_parent_chain_to_graph(graph, parent)


if __name__ == '__main__':
    create_graph()
