import snap
import random

def get_p_from_t(taa, tbb):
    if (taa == 1 and tbb == 0) or (tbb == 1 and taa == 0):
        raise ValueError("The point (taa, tbb) = ({}, {}) is not physical".format(taa, tbb))
    elif taa < 0 or taa > 1 or tbb < 0 or tbb > 1:
        raise ValueError("The values (taa, tbb) = ({}, {})  are not between 0 and 1".format(taa, tbb))
    elif taa == 1 and tbb == 1:
        """
        This is not a unique solution, infact each paa with paa = 1-pbb works. We chose this to make this function useful for other parts of the code
        """
        paa = 0.5
        pbb = 0.5
        pab = 0
    else:
        paa = taa*(1-tbb)/(2-taa-tbb)
        pbb = tbb*(1-taa)/(2-taa-tbb)
        pab = 1-paa-pbb
    return (paa, pbb, pab)

def random_network(n_edges, size, trnd):
    if int(n_edges) > size*(size-1)/2:
        raise ValueError("{} is too many edges for {} nodes".format(int(n_edges), size))
    graph = snap.GenRndGnm(snap.PUNGraph, int(size), int(n_edges), False, trnd) #This should raise an error when too many edges but instead it just hangs
    return graph

def create_network_from_t(avgdeg, sizes, taa, tbb, trnd):
    """
    Works best for sparse networks because there is a chance that for given taa and tbb and avgdeg there are too many links in one of the groups.
    This happens if avgdeg*sum(sizes)*paa > sizes[0]*(sizes[0]-1)/2.
    """

    if len(sizes) > 2:
        raise ValueError("not implemented for more than 2 groups")
    elif len(sizes) < 2:
        raise ValueError("need two group sizes")

    paa, pbb, pab = get_p_from_t(taa, tbb)

    n_edges = avgdeg * sum(sizes) / 2.

    graph1 = random_network(int(n_edges*paa), sizes[0], trnd)
    graph2 = random_network(int(n_edges*pbb), sizes[1], trnd)

    group1_size = graph1.GetNodes()
    for node in graph2.Nodes():
        new_id = node.GetId() + group1_size
        graph1.AddNode(new_id)
    for edge in graph2.Edges():
        edge_start = edge.GetSrcNId() + group1_size
        edge_end = edge.GetDstNId() + group1_size
        graph1.AddEdge(edge_start, edge_end)

    while graph1.GetEdges() < n_edges:
        new_start = random.randint(0, sizes[0]-1)
        new_end = random.randint(sizes[0], sizes[0] + sizes[1]-1)
        graph1.AddEdge(new_start, new_end)


    return graph1


