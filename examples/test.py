import sys
sys.path.append('..')
import argparse

import chainer

from elaas.elaas import Collection
from elaas.family.simple import SimpleHybridFamily
from visualize import visualize
import deepopt.chooser

parser = argparse.ArgumentParser(description='Hybrid Example')
parser.add_argument('-s', '--save_dir', default='_models')
parser.add_argument('-v', '--verbose', action='store_true')
args = parser.parse_args()

mnist = Collection('simple_hybrid', args.save_dir, nepochs=10, verbose=args.verbose)
mnist.set_model_family(SimpleHybridFamily)

train, test = chainer.datasets.get_mnist(ndim=3)
mnist.add_trainset(train)
mnist.add_testset(test)

mnist.set_searchspace(
    nfilters_embeded=[1],
    nlayers_embeded=[1],
    nfilters_cloud=[1],
    nlayers_cloud=[1,2,3],
    lr=[0.001],
    branchweight=[.1]
)

def constraintfn(**kwargs):
    #TODO: change to memory cost
    if kwargs['nfilters_embeded'] > 2:
        return False

    return True

mnist.set_constraints(constraintfn)

# switch chooser
mnist.set_chooser(deepopt.chooser.EpochChooser(k=3))

# currently optimize based on the validation accuracy of the main model
traces = mnist.train()
# visualize(traces)


# generate c
# mnist.generate_c((1,28,28))

# generate container
# mnist.generate_container()

# get traces for the collection
# mnist = Collection('simple_hybrid', save_dir)
# traces = mnist.get_do_traces()
