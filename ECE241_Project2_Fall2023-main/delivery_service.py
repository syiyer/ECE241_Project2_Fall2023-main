"""
UMass ECE 241 - Advanced Programming
Project 2 - Fall 2023
"""
import sys
from graph import Graph, Vertex
from priority_queue import PriorityQueue
from collections import deque

class DeliveryService:
    def __init__(self) -> None:
        self.city_map = None
        self.MST = None

    def buildMap(self, filename: str) -> None:
        file = open(filename, "r")  # Opening filename arg in read mode
        lines = file.readlines()  # Creating list of lines from text
        self.city_map = Graph()  # initialise graph of map
        for line in lines:
            nums = line.split("|")
            self.city_map.addEdge(int(nums[0]), int(nums[1]), int(nums[2]))
            #  Add corresponding vertices and edges
        file.close()  # close file
        pass

    def isWithinServiceRange(self, restaurant: int, user: int, threshold: int) -> bool:
        v = self.city_map.getVertex(restaurant)  # get vertex at id given
        location = False
        if v is None:
            return location
        visited = []  # initialise empty list for visited vertexes
        vertQueue = deque([(restaurant, 0)])  # create deque starting at restaurant
        while len(vertQueue) > 0:  # run while deque still has items
            currentVert, distance = vertQueue.popleft()
            if distance > threshold:
                # continue if corresponding distance is higher than threshold to check other paths
                continue
            if currentVert == user and distance <= threshold:
                #  return service range is true when distance below threshold
                return True
            visited.append(currentVert)  # add each vertex visited to list
            for nextVert in self.city_map.getVertex(currentVert).getConnections():
                if nextVert.getId() not in visited:  # check if vertex has been visited
                    nextDistance = distance + self.city_map.getVertex(currentVert).getWeight(nextVert)
                    #  get new distance
                    vertQueue.append((nextVert.getId(), nextDistance))
                    #  add new items to deque
        return location
        pass

    def buildMST(self, restaurant: int) -> bool:
        v = self.city_map.getVertex(restaurant)
        self.MST = Graph()  # initialise new MST as graph
        pq = PriorityQueue()  # create priority queue instance
        v.setDistance(0)
        pq.buildHeap([(v.getDistance(), v) for v in self.city_map])
        # create the priorityqueue based on the vertexes in the map
        visited = []  # initialise visited vertexes
        while not pq.isEmpty():
            currentVertex = pq.delMin()  # get current vertex based on pq
            if currentVertex not in visited:
                visited.append(currentVertex)  # add the current vertex to visited list
                if currentVertex.getPred() is not None:
                    pred = currentVertex.getPred()  # find predecessor of current vertex
                    self.MST.addEdge(currentVertex.getId(), pred.getId(), currentVertex.getWeight(pred))
                    #  add new edge based on current vertex and predecessor
                for nextVert in currentVertex.getConnections():
                    newDist = currentVertex.getWeight(nextVert)
                    # get new distance
                    if nextVert not in visited and newDist < nextVert.getDistance():
                        nextVert.setDistance(newDist)
                        # update distance
                        nextVert.setPred(currentVertex)
                        # update predecessor
                        pq.decreaseKey(nextVert, newDist)
                        # decrease key based on value
        pass

    def minimalDeliveryTime(self, restaurant: int, user: int) -> int:
        v = self.MST.getVertex(restaurant)
        v1 = self.MST.getVertex(user)
        # get two vertexes at given ids
        time = 0
        # initialise time as 0
        visited = []
        # initialise empty list of vertexes
        if v is None or v1 is None:
            return -1
        # return -1 for in the vertexes don't exist in map
        visited = self.minimalDeliveryTimeHelper(restaurant, user, visited)
        # get outputted list of vertexes from helper
        for i in range(len(visited)-1):
            time += self.MST.getVertex(visited[i]).getWeight(self.MST.getVertex(visited[i+1]))
            #  get total time from MST and vertexes
        return time
        pass

    def minimalDeliveryTimeHelper(self, restaurant: int, user: int, visited: list):
        visited.append(restaurant)  # add each visited vertex to list to keep track
        if restaurant == user:
            # return list of vertexes if delivery reached user
            return visited
        v = self.MST.getVertex(restaurant)
        for nextVert in v.getConnections():
            # go through connections vertex by vertex
            if nextVert.getId() not in visited:
                # check if vertex already been visited
                visited1 = self.minimalDeliveryTimeHelper(nextVert.getId(), user, visited)
                # initialise new list for recurse of function
                if visited1:
                    return visited1
                    # return new list if existing
        visited.pop()
        # take out value from visited list

    def findDeliveryPath(self, restaurant: int, user: int) -> str:
        v = self.city_map.getVertex(restaurant)  # retrieve vertex for restaurant
        v1 = self.city_map.getVertex(user)  # retrieve vertex for user
        if v is None or v1 is None:  # return invalid if either vertex do not exist
            return "INVALID"
        path, weight = self.findDeliveryPathHelper(restaurant, user)
        # call helper function to get path and time for delivery
        if path is None:  # return not accessible if no path for delivery
            return "INVALID"
        pathStr = "->".join(str(v) for v in path) + "(" + str(weight) + ")"
        #  concatenate path of string of vertexes and total time for delivery
        return pathStr
        pass

    def findDeliveryPathHelper(self, restaurant: int, user: int):
        vertQueue = PriorityQueue()
        # initialise priority queue instance for vertexes
        distance = {}
        # initialise empty dict for distances
        path = {}
        # initialise empty dict for paths
        for v in self.city_map:
            distance[v.getId()] = float('inf')
            path[v.getId()] = []
            # fill both dicts with initial values
        realPath = []
        # initialise empty list for actual path to user
        distance[restaurant] = 0
        # initialise distance dict to restaurant as 0
        vertQueue.buildHeap([(distance[v.getId()], v.getId()) for v in self.city_map])
        # fill priority queue with corresponding initial values
        while not vertQueue.isEmpty():
            currentDistance, currentVert = vertQueue.delMin1()
            #  retrieve corresponding values from priority queue
            for nextVert in self.city_map.getVertex(currentVert).getConnections():
                # iterate item through item for connecting vertexes in current vertex
                newDistance = currentDistance + self.city_map.getVertex(currentVert).getWeight(nextVert)
                # retrieve new distance from weight between vertexes
                if newDistance < distance[nextVert.getId()]:
                    # check if distance is less than distance already in dict
                    distance[nextVert.getId()] = newDistance
                    # update new lower distance if lower
                    path[nextVert.getId()] = path[currentVert] + [currentVert]
                    # update new path for lower distance
                    vertQueue.decreaseKey(nextVert.getId(), newDistance)
                    # update priority queue for new values
        realPath = path[user] + [user]
        # get correct list of vertexes to user from path dict
        time = distance[user]
        # get correct total distance to user from distance dict
        return realPath, time

    def findDeliveryPathWithDelay(self, restaurant: int, user: int, delay_info: dict[int, int]) -> str:
        v = self.city_map.getVertex(restaurant)  # retrieve vertex for restaurant
        v1 = self.city_map.getVertex(user)  # retrieve vertex for user
        if v is None or v1 is None:  # return invalid if either vertex do not exist
            return "INVALID"
        path, weight = self.findDeliveryPathWithDelayHelper(restaurant, user, delay_info)
        # call helper function to get path and time for delivery
        if path is None:  # return not accessible if no path for delivery
            return "INVALID"
        pathStr = "->".join(str(v) for v in path) + "(" + str(weight) + ")"
        #  concatenate path of string of vertexes and total time for delivery
        return pathStr
        pass
    def findDeliveryPathWithDelayHelper(self, restaurant: int, user: int, delay_info: dict[int, int]):
        vertQueue = PriorityQueue()
        # initialise priority queue instance for vertexes
        distance = {}
        # initialise empty dict for distances
        path = {}
        # initialise empty dict for paths
        for v in self.city_map:
            distance[v.getId()] = float('inf')
            path[v.getId()] = []
            # fill both dicts with initial values
        realPath = []
        # initialise empty list for actual path to user
        distance[restaurant] = 0
        # initialise distance value to restaurant as 0
        vertQueue.buildHeap([(distance[v.getId()], v.getId()) for v in self.city_map])
        # fill priority queue with corresponding initial values
        while not vertQueue.isEmpty():
            currentDistance, currentVert = vertQueue.delMin1()
            #  retrieve corresponding values from priority queue
            for nextVert in self.city_map.getVertex(currentVert).getConnections():
                # iterate item through item for connecting vertexes in current vertex
                newDistance = currentDistance + self.city_map.getVertex(currentVert).getWeight(nextVert)
                # retrieve new distance from weight between vertexes
                newDistance += delay_info.get(nextVert.getId(), 0)
                # add additional delay time from information given
                if newDistance < distance[nextVert.getId()]:
                    # check if distance is less than distance already in dict
                    distance[nextVert.getId()] = newDistance
                    # update new lower distance if lower
                    path[nextVert.getId()] = path[currentVert] + [currentVert]
                    # update new path for lower distance
                    vertQueue.decreaseKey(nextVert.getId(), newDistance)
                    # update priority queue for new values
        realPath = path[user] + [user]
        # get correct list of vertexes to user from path dict made
        time = distance[user]
        # get correct total distance to user from distance dict
        return realPath, time

    ## DO NOT MODIFY CODE BELOW!
    @staticmethod
    def nodeEdgeWeight(v):
        return sum([w for w in v.connectedTo.values()])

    @staticmethod
    def totalEdgeWeight(g):
        return sum([DeliveryService.nodeEdgeWeight(v) for v in g]) // 2

    @staticmethod
    def checkMST(g):
        for v in g:
            v.color = 'white'

        for v in g:
            if v.color == 'white' and not DeliveryService.DFS(g, v):
                return 'Your MST contains circles'
        return 'MST'

    @staticmethod
    def DFS(g, v):
        v.color = 'gray'
        for nextVertex in v.getConnections():
            if nextVertex.color == 'white':
                if not DeliveryService.DFS(g, nextVertex):
                    return False
            elif nextVertex.color == 'black':
                return False
        v.color = 'black'
        return True


# NO MORE TESTING CODE BELOW!
# TO TEST YOUR CODE, MODIFY test_delivery_service.py
