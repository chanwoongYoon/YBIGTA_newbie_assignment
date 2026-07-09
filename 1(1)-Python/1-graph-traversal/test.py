import lib

"""
4 5 1
1 2
1 3
1 4
2 4
3 4
"""

n = 4
m = 5
root = 1

graph_test = lib.Graph(n)

graph_test.add_edge(1,3)
graph_test.add_edge(1,2)
graph_test.add_edge(1,4)
graph_test.add_edge(2,4)
graph_test.add_edge(3,4)

graph_test.search_and_print(1)