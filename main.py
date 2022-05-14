import random

file = "9.200-40.txt"
p = 0.1  # tempo wygasania feromonów
Q = 0.1  # stała dodawania feromonów
alfa = 2  # paramert znaczenia feromonow
beta = 15  # parametr znaczenia dlugosci


class Node:
    def __init__(self, value, id):
        self.value = value
        self.id = id

    def setDist(self, other):
        for i in range(len(self.value)):
            if self.value[i:] == other.value[:len(other.value) - i]:
                return i
        return len(self.value)

    def getPath(self, other, paths):
        return paths[self.id][other.id]

    def __str__(self):
        return  f"{self.value}"
    def __repr__(self):
        return f"{self.value}"


class Path:
    def __init__(self, length, pheromone):
        self.length = length
        self.pheromone = pheromone

    def disPheromone(self):
        self.pheromone *= (1 / p)

    def addPheromone(self, result):
        self.pheromone += result * Q

    def setLenght(self,l):
        self.length=l

    def __str__(self):
        return f"{self.length},{self.pheromone}"

    def __repr__(self):
        return f"{self.length},{self.pheromone}"


best_road = None
best_result = 0

class Ant:
    def __init__(self, stamina, start):
        self.stamina = stamina
        self.current = start
        self.road = []
        self.result = 1
        self.running = True

    def journey(self,paths,nodes):
        global best_result
        global best_road
        while (self.running):  #chodzenie po grafie
            #print(self.stamina)
            possible_nodes = []
            self.road.append(self.current)
            for i in nodes:
                if(i==self.current):
                    continue
                #print(self.current)
                if (self.current.getPath(i,paths).length <= self.stamina and not (self.road.__contains__(i))):
                    possible_nodes.append(i)
            if len(possible_nodes) == 0:
                self.running = False
            if self.running == False:
                break
            possibilities = []
            for i in possible_nodes:
                tmp_path = self.current.getPath(i, paths)
                possibilities.append(pow(tmp_path.pheromone, alfa) / pow(tmp_path.length, beta))
            choice = random.choices(possible_nodes, possibilities)
            self.result += 1
            self.stamina -= self.current.getPath(choice[0],paths).length
            self.current = choice[0]

        prv_node = None
        for tmp_node in possible_nodes:  # dodawanie feromonow
            if(prv_node == None):
                prv_node = tmp_node
                continue
            tmp_path = tmp_node.getPath(prv_node,paths)
            tmp_path.addPheromone(self.result)
            prv_node= tmp_node

        if self.result > best_result:  # porownac z globalnym
            best_road = self.road
            best_result = self.result
            print("new best result", best_result)

class Hive:
    def __init__(self,ants,generation):
        self.generation=generation
        self.ants=ants
    def start(self,paths,nodes):
        for i in range(self.generation):
            for ant in range(self.ants):
                temp=Ant(200,nodes[random.randint(0,len(nodes)-1)])
                temp.journey(paths,nodes)
            for path in paths:
                for x in path:
                    x.disPheromone()

def readData(filename):
    nodes=[]
    with open(filename) as f:
        lines=f.readlines()
    for index, i in enumerate(lines):
        value=i.replace('\n','')
        nodes.append(Node(value,index))
    paths=[]
    for i in range(len(nodes)):
        paths.append([])
        for j in range(len(nodes)):
            paths[-1].append(Path(0,1))
    return nodes,paths

def setLengths(nodes,paths):
    for y in range(len(paths)):
        for x in range(len(paths)):
            if x!=y:
                value=nodes[y].setDist(nodes[x])
                paths[y][x].length=value
    return  paths


def main():
    nodes,paths=readData(file)
    setLengths(nodes,paths)
    #debuguje sobie
    mrowisko = Hive(30,30)
    mrowisko.start(paths,nodes)
    print(best_road)
    print(best_result)

if __name__ == "__main__":
    main()