INTMIN = float('-inf')
INTMAX = float('inf')
            

RobotCdn = [[[0, 0], [0, 8]], [[5, 9], [5, 5]], [[0, 0], [5, 5]]]

TaskCdn = [[[5, 0], [3, 12]], [[4, 6], [0, 6]], [[5, 0], [0, 6]]]

grid = [[1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
        [1, 0, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1],
        [1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0, 1, 1, 1, 1, 1, 2],
        [2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]     
k, r = len(RobotCdn), len(TaskCdn)
M, N = len(grid), len(grid[0])

class node:
    x = -1
    y = -1
    dist = 0
    def __init__(self,a, distance0 = 0):
        self.x, self.y = a
        self.dist = distance0

def heapperm(a, size, perms):
    if size == 1:
        perms.append([0] + a)
        return
    for i in range(size):
        heapperm(a, size-1, perms)
        if size & 1:
            a[0], a[size-1] = a[size-1], a[0]
        else:
            a[i], a[size-1] = a[size-1], a[i]
                
def hamiltoniancycles():
    ### GENERATES ALL CYCLIC PERMUTATIONS 
    perms = []
    heapperm(list(range(1, k+r, 1)), k+r - 1, perms)
    return perms

def nodeDist(sp, dp):
    # Find min distance source to dest by BFS
    dest = node(dp, 0)
    source = node(sp, 0)
    visited = [[False for j in range(N)] for i in range(M)]
    q = []
    visited[source.x][source.y] = True
    q.append(source)

    while len(q) > 0:
        curr = q.pop(0)
        if  curr.y == dest.y and curr.x == dest.x :
            return curr.dist
        
        
        if curr.x - 1 >= 0 and not visited[curr.x - 1][curr.y] and grid[curr.x - 1][curr.y] != 0:
            q.append(node([curr.x - 1, curr.y], curr.dist + 1))
            visited[curr.x - 1][curr.y] = True
            
        if curr.x + 1 < M and not visited[curr.x + 1][curr.y] and grid[curr.x + 1][curr.y] != 0:
            q.append(node([curr.x + 1, curr.y], curr.dist + 1))
            visited[curr.x + 1][curr.y] = True
        
        if curr.y - 1 >= 0 and not visited[curr.x][curr.y - 1] and grid[curr.x][curr.y - 1] != 0:
            q.append(node([curr.x, curr.y - 1], curr.dist + 1))
            visited[curr.x][curr.y - 1] = True
        
        if curr.y + 1 < N and not visited[curr.x][curr.y + 1] and grid[curr.x][curr.y + 1] != 0:
            q.append(node([curr.x, curr.y + 1], curr.dist + 1))
            visited[curr.x][curr.y + 1] = True
            
    return -1

def Graph():
    
    for i in range(k+r):
        for j in range(k+r):
            u, v = vertexType[i], vertexType[j]
            if  v == 1 and u == 0 :
                
                adjMat[i][j] = nodeDist(vertexData[i][0], vertexData[j][0])
            elif  v == 1 and u == 1 :
                
                adjMat[i][j] = nodeDist(vertexData[i][0], vertexData[i][1]) + nodeDist(vertexData[i][1], vertexData[j][0])
            elif  v == 0 and u == 1 :
                adjMat[i][j] = nodeDist(vertexData[i][0], vertexData[i][1]) + nodeDist(vertexData[i][1], vertexData[j][1])
            else:
                pass

def span(cycle):
    a = 0
    for i in range(len(cycle)):
        if vertexType[cycle[i]] == 0:
            a = i
            break

    m = INTMIN
    cycle = cycle[a:] + cycle[:a]
    t = 0
    
    for i in range(len(cycle) - 1):
        t += adjMat[cycle[i]][cycle[i+1]]
        if vertexType[cycle[i + 1]] == 0:
            ## next item is an agent
            m = max(m, t)
            t = 0
    t += adjMat[cycle[-1]][cycle[0]]
    m = max(m, t)
    return m

def getpath(cyc):
    a = 0
    for i in range(len(cyc)):
        if vertexType[cyc[i]] == 0:
            a = i
            break
    cyc = cyc[a:] + cyc[:a]
    s, e = 0, 0
    assignments = dict()
    for i in range(len(cyc)):
        if (i+1 < len(cyc) and vertexType[cyc[i + 1]] == 0) or i + 1 == len(cyc):
            e = i
            assignments[cyc[s]] = cyc[s+1: e+1]
            s, e = i+1, i+1
            
    return assignments

adjMat = [[0 for j in range(k+r)] for i in range(k+r)]
vertexType = [0 for i in range(len(RobotCdn))] + [1 for i in range(len(TaskCdn))]
vertexData = RobotCdn + TaskCdn

Graph()
minSpan = INTMAX
index = 0
cycles = hamiltoniancycles()

for i in range(len(cycles)):
    cycle = cycles[i]
    s= span(cycle)
    if s < minSpan:
        minSpan = s
        index = i

print("approximate  ", minSpan)
print("schedule", getpath(cycles[index]))