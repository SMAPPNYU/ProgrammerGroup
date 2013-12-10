"""
Network utilities
"""

def display_retweet_network(network, outfile=None, show=False):
    """
    Take a DiGraph (retweet network?) and display+/save it to file.
    Nodes must have a 'color' property, represented literally and indicating their type
    Edges must have a 'weight' property, represented as edge width
    """
    import networkx as nx
    import matplotlib.pyplot as plt

    # Create a color list corresponding to nodes.
    node_colors = [ n[1]["color"] for n in network.nodes(data=True) ]

    # Get edge weights from graph
    edge_weights = [ e[2]["weight"] for e in network.edges(data=True) ]

    # Build up graph figure
    #pos = nx.random_layout(network)
    pos = nx.spring_layout(network)
    nx.draw_networkx_edges(network, pos, alpha=0.3 , width=edge_weights, edge_color='m')
    nx.draw_networkx_nodes(network, pos, node_size=400, node_color=node_colors, alpha=0.4)
    nx.draw_networkx_labels(network, pos, fontsize=6)

    plt.title("Retweet Network", { 'fontsize': 12 })
    plt.axis('off')

    if outfile:
        print "Saving network to file: {0}".format(outfile)
        plt.savefig(outfile)

    if show:
        print "Displaying graph. Close graph window to resume python execution"
        plt.show()