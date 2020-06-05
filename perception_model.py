import sys
import os
sys.path.append("../snap-triadic-homophily/snap-python/swig")
#sys.path.append("/m/cs/work/asikaia5/reps/pymisc/")
import snap
#import runs
import numpy
import net_create as nc
import argparse
import matplotlib.pyplot as plt; plt.ion()
import seaborn as sns
import pickle
#import parse_dic

# How to run, with python 2
#python basic_model_perception.py .75 .75 .5 .75 .5 .5 100 20 50 difF_homoph figname.pdf
# sav sbc na cv taa tbb nodes avgdeg iterations run_name folder


def run_model_and_save(sv, nv, cv, nodes, avgdeg, taa, tbb, iterations, run_name, folder):
    """
    sv: 2d vector with s parameter groups a and b

    """

    #TODO: Save a network after it has been simulated
    trnd = snap.TRnd(0) #from the clock? The default value seems to mean that the random seed is always the same
    sa, sb = sv

    iterations = int(iterations)
    edges= int((nodes * avgdeg) /2.)
    sizes= snap.TFltV()
    asize= int(nv*nodes)
    bsize= nodes - asize
    sizes.Add(asize)
    sizes.Add(bsize)

    try:
        network = nc.create_network_from_t(avgdeg, sizes, taa, tbb, trnd)
    except ValueError:
        print("Could not create network with {} and {} nodes and average degree {}".format(sizes[0], sizes[1], avgdeg))

    biasVec = snap.TFltV()
    biasVec.Add(sv[0])
    biasVec.Add(sv[1])

    Paas, Pbbs = [], []
    instds, outstds = [], []

    for ite in range(iterations):
        snap.RunBiasedTriadicModel(network, edges, cv, sizes, biasVec, trnd)

    modelstr=" ".join(map(str,[sv[0],sv[1],nv,cv,nodes,avgdeg,iterations,taa,tbb]))

    Pab = snap.GetPMatrixElement(0, 1, network, sizes)
    Paa = snap.GetPMatrixElement(0, 0, network, sizes)
    Pbb = snap.GetPMatrixElement(1, 1, network, sizes) #1 - Pab - Paa

    biases_a, degs_a = [], []
    biases_b, degs_b = [], []
    true_fraction = (asize + 0.) / (asize + bsize)
    def classify_node(node):
        if node < asize:
            return 1 # If in group a, it is minority
        else:
            return 0 # If in group b, it's majority

    #Iterate over nodes
    for NI in network.Nodes():
        deg = 0
        perc = 0
        #Iterate over neighbors
        for Id in NI.GetOutEdges():
            perc += classify_node(Id)
            deg+= 1
        if deg > 0:
            bias = (perc + 0.) / (deg * true_fraction)
        else:
            bias = 0.
        if classify_node(NI.GetId()) == 1:
            biases_a.append(bias)
            degs_a.append(deg)
        else:
            biases_b.append(bias)
            degs_b.append(deg)

    bias_a = numpy.mean(biases_a)
    bias_b = numpy.mean(biases_b)

    if not os.path.exists(folder):
        os.mkdir(folder)
    summary_name = 'summary.txt'
    if not os.path.exists(os.path.join(folder, summary_name)):
        res = 'name sa sb na cv taa tbb nodes avgdeg iter bias_a bias_b\n'
        save_summary(res, os.path.join(folder, summary_name))
        #max_file = 0
    #else:
    #    max_file = max([int(f.split('.')[0]) for f in os.listdir(folder)])


    res = ' '.join(['{}'] * 12) + '\n'
    path_name = os.path.join(folder, run_name + '.p')
    if os.path.exists(path_name):
        run_name += '_0'
        path_name = os.path.join(folder, run_name + '.p')
    res = res.format(run_name, sa, sb, nv, cv, taa, tbb, nodes, avgdeg, iterations, bias_a, bias_b)
    save_summary(res, os.path.join(folder, 'summary.txt'))

    print(res)
    dic = {'sa': sa,
            'sb': sb,
            'na': nv,
            'cv': cv,
            'taa': taa,
            'tbb': tbb,
            'nodes': nodes,
            'avgdeg': avgdeg,
            'iterations': iterations,
            'biases_a': biases_a,
            'biases_b': biases_b,
            'degs_a': degs_a,
            'degs_b': degs_b}

    with open(path_name, 'wb') as w:
        pickle.dump(dic, w)

def save_summary(data, name):
    with open(name, 'a+') as w:
        w.write(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--sav', type=float, default=.5)
    parser.add_argument('--sbv', type=float, default=.5)
    parser.add_argument('--nv', type=float, default=.1)
    parser.add_argument('--cv', type=float, default=.5)
    parser.add_argument('--taa', type=float, default=.5)
    parser.add_argument('--tbb', type=float, default=.5)
    parser.add_argument('--nodes', type=int, default=1000)
    parser.add_argument('--avgdeg', type=float, default=20)
    parser.add_argument('--iterations', type=int, default=50)
    parser.add_argument('--run_name', type=str, default='0')
    parser.add_argument('--folder', type=str, default='./')
    args = parser.parse_args()

    nv, sav, sbv, cv, taa, tbb, nodes, avgdeg, iterations, run_name, folder = [args.nv, args.sav, args.sbv, args.cv, args.taa, args.tbb, args.nodes, args.avgdeg, int(args.iterations), args.run_name, args.folder]
    run_model_and_save([sav, sbv], nv, cv, nodes, avgdeg, taa, tbb, iterations, run_name, folder)

