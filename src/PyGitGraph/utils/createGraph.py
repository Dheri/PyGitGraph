import sys
import networkx as nx
from git import Repo, Git, IndexFile
import matplotlib.pyplot as plt
import os


def create_graph():
    repo_name = "progit2"
    code_dir = "code"
    dir_path = os.path.join(os.getenv("userprofile"), code_dir, repo_name)
    repo = Repo(dir_path)
    print(dir_path)
    graph = nx.DiGraph()
    for ref in repo.references:
        print(ref.commit, ref)
        if graph.has_node(ref.commit.hexsha) and ('refs' in graph.nodes[ref.commit.hexsha]):
            refs = graph.nodes[ref.commit.hexsha]['refs']
            refs = refs + ", " + ref.name
            graph.nodes[ref.commit.hexsha]['refs'] = refs
        else:
            graph.add_node(ref.commit.hexsha, refs=ref.name)
        add_parent_chain_to_graph(graph, ref.commit)

    print('graph.nodes list', list(graph.nodes))
    pos = nx.spiral_layout(graph)
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
    print(list(graph.nodes(data=True)))

    nx.draw_networkx(graph, **options)
    nx.write_gexf(graph, '{}.gexf'.format(repo_name))
    plt.show()


def add_parent_chain_to_graph(graph, rev):
    # print('graph len is', len(graph), 'rev is ', rev.hexsha)
    # print('short_sha', rev.hexsha[:6], 'committed_date', rev.committed_date)

    for parent in rev.parents:
        if graph.has_edge(rev.hexsha, parent.hexsha):
            print('edge {} - {} already in graph'.format(rev.hexsha[:6], parent.hexsha[:6]))
            return
        weight = 1
        graph.add_edge(rev.hexsha, parent.hexsha, weight=weight)
        add_parent_chain_to_graph(graph, parent)


if __name__ == '__main__':
    create_graph()
