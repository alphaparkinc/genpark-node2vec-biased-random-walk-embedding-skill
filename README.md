# genpark-node2vec-biased-random-walk-embedding-skill

Agent Skill implementing **Node2Vec 2nd-Order Biased Random Walks** exploring local neighborhoods (DFS vs BFS) via return parameter $p$ and in-out parameter $q$.

## Architectural Overview
```mermaid
flowchart LR
    StepPrev["Previous Node (t)"] --> StepCur["Current Node (v)"]
    StepCur --> Choice{"Next Node (x)"}
    Choice -- "x == t" --> Return["Weight 1/p (Return Bias)"]
    Choice -- "x in Nbr(t)" --> Local["Weight 1.0 (Local Clustering)"]
    Choice -- "x not in Nbr(t)" --> Explore["Weight 1/q (Exploration / DFS)"]
```
