from client import Node2VecWalkGenerator

graph = {
    "A": {"B": 1.0, "C": 1.0},
    "B": {"A": 1.0, "D": 1.0},
    "C": {"A": 1.0, "D": 1.0},
    "D": {"B": 1.0, "C": 1.0}
}
gen = Node2VecWalkGenerator(graph, p=0.5, q=2.0)
walk = gen.generate_walk("A", walk_length=8)
print("Biased Random Walk:", walk)
