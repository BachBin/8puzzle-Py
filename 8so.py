from copy import deepcopy

DIRECTIONS = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}

#file
file = open('input.txt', 'r')
f = file.read()
Ar = []
for i in f:
    if (i.isnumeric()) == True:
        Ar.append(int(i))
START = [Ar[0:3],Ar[3:6],Ar[6:9]]

file = open('output.txt.','r')
f = file.read()
Ar = []
for i in f:
    if (i.isnumeric()) == True:
        Ar.append(int(i))
END = [Ar[0:3], Ar[3:6], Ar[6:9]]
#end file

def print_matrix(array):
    for a in range(len(array)):
        for i in array[a]:
            print(i, end=' ')
        print()


class Node:
    def __init__(self, current_node, previous_node, g, h, dir):
        self.current_node = current_node
        self.previous_node = previous_node
        self.g = g
        self.h = h
        self.dir = dir

    def f(self):
        return self.g + self.h              #f = gx + hx


def get_pos(node, element): #lấy vị trí nút element trong node
    for row in range(len(node)):
        if element in node[row]:
           return (row, node[row].index(element)) #duyệt tìm thấy thì trả về row và colum


def cal_cost(node): #Tính toán chi phí của 1 node
    cost = 0
    for row in range(len(node)):
        for col in range(len(node[0])):
            pos = get_pos(END, node[row][col])
            cost += abs(row - pos[0]) + abs(col - pos[1])
    return cost


def getAdjNode(node): #Tính toán các vị trí mà nút 0 có thể di chuyển lưu vào list
    listNode = []
    emptyPos = get_pos(node.current_node, 0) #vi tri nut 0

    for dir in DIRECTIONS.keys():
        newPos = (emptyPos[0] + DIRECTIONS[dir][0], emptyPos[1] + DIRECTIONS[dir][1])
        if 0 <= newPos[0] < len(node.current_node) and 0 <= newPos[1] < len(node.current_node[0]):
            newState = deepcopy(node.current_node)
            newState[emptyPos[0]][emptyPos[1]] = node.current_node[newPos[0]][newPos[1]]
            newState[newPos[0]][newPos[1]] = 0
            listNode.append(Node(newState, node.current_node, node.g + 1, cal_cost(newState), dir))

    return listNode


def getBestNode(openSet):
    firstIter = True
    for node in openSet.values():
        if firstIter or node.f() < bestF:
            firstIter = False
            bestNode = node
            bestF = bestNode.f()
    return bestNode


def buildPath(closedSet): #trả về danh sách lưu cách di chuyển và trạng thái lúc đó
    node = closedSet[str(END)]
    branch = list()

    while node.dir:
        branch.append({
            'dir': node.dir,
            'node': node.current_node
        })
        node = closedSet[str(node.previous_node)]
    branch.append({
        'dir': '',
        'node': node.current_node
    })
    branch.reverse()
    return branch


def main(puzzle):
    open_set = {str(puzzle): Node(puzzle, puzzle, 0, cal_cost(puzzle), "")}
    closed_set = {}

    while True:
        test_node = getBestNode(open_set)

        closed_set[str(test_node.current_node)] = test_node

        if test_node.current_node == END:
            return buildPath(closed_set)

        adj_node = getAdjNode(test_node)

        for node in adj_node:
            if str(node.current_node) in closed_set.keys() or str(node.current_node) in open_set.keys() and open_set[
                str(node.current_node)].f() < node.f():
                continue
            open_set[str(node.current_node)] = node

        del open_set[str(test_node.current_node)]


if __name__ == '__main__':

    start = main(START)
    print('--------------------------------')
    print('Bước di chuyển: ', len(start) - 1)
    print()
    print("INPUT")
    for b in start:
        print_matrix(b['node'])
        print()
    print("Hoàn thành.")




