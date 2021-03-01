"""
NAME: Graph
AUTHOR: Tanaka Chitete
PURPOSE: Implement a Graph
CREATION: 01/03/2021
LAST MODIFICATION: 01/03/2021
"""

from GraphNode import GraphNode
from LinkedList import LinkedList
from Queue import Queue
from Stack import Stack

class Graph:
    # CONSTRUCTORS

    """
    CONSTRUCTOR
    IMPORT(S): NONE
    EXPORT(S): Address of new Graph
    PURPOSE: Make new Graph
    CREATION: 01/03/2021
    LAST MODIFICATION: 01/03/2021
    """

    def __init__(self, isDirected=False):
        self.__nodes = LinkedList()
        self.__isDirected = isDirected
        self.__nodeCount = 0
        self.__connectionCount = 0


    # SETTERS (MUTATORS)

    def add(self, label):
        if label is None:
            raise ValueError("Cannot call add with None label")
        elif not isinstance(label, str):
            raise ValueError("Cannot call add with non-str label")
        elif self.has(label):
            raise ValueError("Cannot call add with label of existant node")
        else:
            newNode = GraphNode(label)
            self.__nodes.insertLast(newNode)
            self.__nodeCount += 1
    

    def connect(self, srcLabel, destLabel):
        if self.__nodeCount < 2:
            raise RuntimeError("Cannot call connect on Graph with less than two nodes")
        elif srcLabel is None or destLabel is None:
            raise ValueError("Cannot call connect with None label")
        elif not isinstance(srcLabel, str) or not isinstance(destLabel, str):
            raise ValueError("Cannot call add with non-str label")
        elif srcLabel == destLabel:
            raise ValueError("Cannot call connect with equal labels")
        elif not self.__has(srcLabel) or not self.__has(destLabel):
            print(self.__nodes)

            raise ValueError("Cannot call connect with label of non-existant node")
        else:
            self.__connect(srcLabel, destLabel)


    # GETTERS (ACCESSORS)

    def get(self, label):
        if self.__nodes.isEmpty():
            raise RuntimeError("Cannot call get on an empty graph")
        elif label is None:
            raise ValueError("Cannot call get with a None label")
        elif not isinstance(label, str):
            raise ValueError("Cannot call get with a non-str label")
        elif not self.has(label):
            raise ValueError("Cannot call get with label of non-existant node")
        else:
            return self.__get(label)


    def nodeCount(self):
        return self.__nodeCount


    def connectionCount(self):
        return self.__connectionCount


    # OPERATORS

    def has(self, label):
        if self.__nodes.isEmpty():
            return False
        if label is None:
            raise ValueError("Cannot call has with a None label")
        elif not isinstance(label, str):
            raise ValueError("Cannot call has with a non-str label")
        else:
            return self.__has(label)


    def areNeighbours(self, srcLabel, destLabel):
        if self.__nodeCount < 2:
            raise RuntimeError("Cannot call areNeighbours on Graph with less than 2 nodes")
        elif srcLabel is None or destLabel is None:
            raise ValueError("Cannot call areNeighbours with a None label")
        elif not isinstance(srcLabel, str) or not isinstance(destLabel, str):
            raise ValueError("Cannot call areNeighbours with equal labels")
        else:
            return self.__areNeigbours(srcLabel, destLabel)


    def bfs(self):
        upcoming = Queue() 
        visited = Queue()

        start = self.__nodes.peekFirst()

        # Prepares to visit startNode's neighbours
        upcoming.enqueue(start)
        # Prevents start from being visited again and adds it to visited
        start.wasVisitedBool = True
        visited.enqueue(start.label)

        while not upcoming.isEmpty():
            node = upcoming.dequeue()
            nodeNeighbours = iter(node.neighbours)
            # Visits node's neigbours
            while nodeNeighbours.hasNext():
                neighbour = next(nodeNeighbours)
                if not neighbour.wasVisited():
                    # Prepares to visit neighbour's neighbours
                    upcoming.enqueue(neighbour)
                    # Prevents neighbour from being visited again and adds it to visited
                    neighbour.wasVisitedBool = True
                    visited.enqueue(neighbour.label)
        
        # Allows nodes to be operated on again
        self.__unvisit()

        return visited
    

    def dfs(self):
        nodes = iter(self.__nodes)
        visited = Queue()

        while nodes.hasNext():
            curr = next(nodes)
            # Visits node's neighbours
            if not curr.wasVisited():
                self.__visit(curr, visited)
        
        # Allows nodes to be operated on again
        self.__unvisit()

        return visited


    def printPaths(self, srcLabel, destLabel):
        path = Stack()
        path.push(srcLabel)

        src = self.get(srcLabel)
        dest = self.get(destLabel)

        self.__printPaths(src, dest, path)

        # Allows nodes to be operated on again
        self.__unvisit()


    # PRIVATE SUBMODULES

    def __connect(self, srcLabel, destLabel):
        src = self.__get(srcLabel)
        dest = self.__get(destLabel)

        src.addNeighbour(dest)
        if not self.__isDirected:
            dest.addNeighbour(src)

        self.__connectionCount += 1


    def __has(self, label):
        nodes = iter(self.__nodes)
        has = False

        while nodes.hasNext() and not has:
            n = next(nodes)
            if n.label == label:
                has = True
        
        return has


    def __areNeigbours(self, srcLabel, destLabel):
        areNeighbours = False
        nodes = iter(self.__nodes)
        # Finds node with label srcLabel
        while nodes.hasNext() and not areNeighbours:
            node = next(nodes)
            # Upon finding node, searches n's neighbours for neighbour with label destLabel
            if node.label == srcLabel:
                neighbours = iter(node.neighbours)
                while neighbours.hasNext() and not areNeighbours:
                    neighbour =  next(neighbours)
                    # Upon finding neighbour, validates that node and neighbour are neighbours
                    if neighbour.label == destLabel:
                        areNeighbours = True

        return areNeighbours

    
    def __get(self, label):
        n = None
        nodes = iter(self.__nodes)
        while nodes.hasNext() and not n:
            curr = next(nodes)
            if curr.label == label:
                n = curr

        return n


    def __unvisit(self):
        nodes = iter(self.__nodes)
        while nodes.hasNext():
            curr = next(nodes)
            if curr.wasVisited():
                curr.wasVisitedBool = False

    
    def __visit(self, node, visited):
        # Prevents node from being visited again and adds it to visited
        node.wasVisitedBool = True
        visited.enqueue(node.label)

        neighbours = iter(node.neighbours)
        while neighbours.hasNext():
            curr = next(neighbours)
            # Visits curr's neighbours
            if not curr.wasVisited():
                self.__visit(curr, visited)
        

    def __printPaths(self, node, dest, path):
        # Adds p to paths and stops recursing
        if node.label == dest.label:
            print(path)
        else:
            # Prevents node from being visited again
            node.wasVisitedBool = True
            # Visits node's neighbours
            neighbours = iter(node.neighbours)
            while neighbours.hasNext():
                curr = next(neighbours)
                if not curr.wasVisited():
                    path.push(curr.label)
                    self.__printPaths(curr, dest, path)
                    path.pop()

            # Allows node to be visited again
            node.wasVisitedBool = False