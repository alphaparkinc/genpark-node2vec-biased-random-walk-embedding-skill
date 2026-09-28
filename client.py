"""Node2Vec 2nd-Order Biased Random Walk Engine.
100% Python Standard Library.
"""

import random

class Node2VecWalkGenerator:
    """Node2Vec 2nd-order random walk with p (return) and q (in-out) hyperparameters."""
    def __init__(self, adj_dict, p=1.0, q=1.0):
        self.adj = adj_dict
        self.p = p
        self.q = q

    def _get_transition_prob(self, t, v, x):
        if x == t:
            return 1.0 / self.p
        elif x in self.adj[t]:
            return 1.0
        else:
            return 1.0 / self.q

    def generate_walk(self, start_node, walk_length=6):
        walk = [start_node]
        if not self.adj[start_node]:
            return walk

        cur = random.choice(list(self.adj[start_node].keys()))
        walk.append(cur)

        for _ in range(walk_length - 2):
            prev = walk[-2]
            cur = walk[-1]
            nbrs = list(self.adj[cur].keys())
            if not nbrs:
                break
            weights = [self._get_transition_prob(prev, cur, x) for x in nbrs]
            total_w = sum(weights)
            r = random.uniform(0, total_w)
            cum = 0.0
            next_node = nbrs[-1]
            for x, w in zip(nbrs, weights):
                cum += w
                if r <= cum:
                    next_node = x
                    break
            walk.append(next_node)
        return walk
