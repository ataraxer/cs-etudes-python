#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Edge(object):
    def __init__(self, dst, value):
        self.dst = dst
        self.value = value

    def __repr__(self):
        return "({} {})".format(self.dst, self.value)


class Graph(object):
    def __init__(self, directed=False):
        self.directed = directed
        self.edges = {}


    def add(self, value):
        self.edges[value] = set()
        return self


    def connect(self, src, dst, value=1):
        edge = Edge(dst, value)
        self.edges[src].add(edge)
        if not self.directed:
            edge = Edge(src, value)
            self.edges[dst].add(edge)
        return self


    def are_connected(self, src, dst, value=None):
        marked, _ = self._dfs(src)
        return dst in marked


    def path_to(self, src, dst):
        marked, edge_to = self._dfs(src)
        return self._path_to(marked, edge_to, src, dst)


    def shortest_path_to(self, src, dst):
        marked, edge_to = self._bfs(src)
        return self._path_to(marked, edge_to, src, dst)


    def _path_to(self, marked, edge_to, src, dst):
        if dst in marked:
            item = dst
            path = [dst]

            while item != src:
                item = edge_to[item]
                path.append(item)

            path.reverse()
            return path


    def _dfs(self, vertex, marked=None, edge_to=None, action=lambda *args: None):
        marked = marked or set()
        marked.add(vertex)
        edge_to = edge_to or {}

        action(vertex)

        for edge in self.edges[vertex]:
            if edge.dst not in marked:
                action(vertex)
                edge_to[edge.dst] = vertex
                self._dfs(edge.dst, marked, edge_to, action)

        return marked, edge_to


    def _bfs(self, vertex):
        queue = [vertex]
        marked = set(queue)
        edge_to = {}

        while queue:
            vertex = queue.pop(0)
            for edge in self.edges[vertex]:
                if edge.dst not in marked:
                    edge_to[edge.dst] = vertex
                    marked.add(edge.dst)
                    queue.append(edge.dst)

        return marked, edge_to


    def connected_components(self):
        marked = set()
        components = {}

        for vertex in self.edges:
            if vertex not in marked:
                components[vertex] = set()
                def process(v): components[vertex].add(v)
                marked, _ = self._dfs(vertex, marked, action=process)

        return components


    def __repr__(self):
        result = ''
        for value, edges in self.edges.iteritems():
            result += value
            for edge in edges:
                result += ' -[{}]-> {}'.format(edge.value, edge.dst)
            result += '\n'
        return result


def main():
    graph = Graph(directed=False)

    graph.add('a').add('b')
    graph.connect('a', 'b')

    graph.add('c')
    graph.connect('b', 'c')
    graph.connect('a', 'c')

    graph.add('d').add('x').add('y')
    graph.connect('x', 'y')

    print graph
    print graph.connected_components()


if __name__ == '__main__':
    main()
