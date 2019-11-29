
from bayes_net import *

# Exemplo dos acetatos:

bn = BayesNet()

bn.add('ST',[],0.6)
bn.add('PT',[],0.05)

bn.add('AC', [('ST', True)], 0.9)
bn.add('AC', [('ST', False)], 0.001)

bn.add("PA", [('PT', True)], 0.25)
bn.add("PA", [('PT', False)], 0.004)

bn.add("CP", [('ST', True), ("PA", True)], 0.02)
bn.add("CP", [('ST', True), ("PA", False)], 0.01)
bn.add("CP", [('ST', False), ("PA", True)], 0.011)
bn.add("CP", [('ST', False), ("PA", False)], 0.001)

bn.add("UR", [('PT', True), ("PA", True)], 0.9)
bn.add("UR", [('PT', False), ("PA", True)], 0.1)
bn.add("UR", [('PT', True), ("PA", False)], 0.9)
bn.add("UR", [('PT', False), ("PA", False)], 0.01)

print(bn.individualProb('PA', True))
