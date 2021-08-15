# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"

    # Funcao que realizara a busca por profundidade
    # Poit -> Ponto onde pacman estara no momento
    # Stack-> Pilha de vertices ja visitados
    # Moves-> Pilha de movimentos a serem realizados para se chegar ao ponto final.
    def realizeDFS(point, stack, moves):
        # Coloca um vertice visitado na pilha
        stack.append(point)

        # Se vertice eh o ponto final, encerra.
        if problem.isGoalState(point):
            return True

        # Percorre sucessores
        for i in problem.getSuccessors(point):
            # Se nao foi visitado
            if not i[0] in stack:
                # Insere o movimento na pilha e continua a DFS
                moves.append(i[1])
                found = realizeDFS(i[0], stack, moves)

                # Se encontrou goal, este caminho esta certo.
                if found:
                    return True
                # Se nao encontrou goal, remove do caminho.
                else:
                    moves.pop()

        return False
        
    # Pilha de visitados
    stack_dfs = []
    # Pilha de Movimentos
    moves = []
    # Ponto inicial
    start = problem.getStartState()
    # Realizar DFS
    realizeDFS(start, stack_dfs, moves)

    # retorna os movimentos necessarios para chegar no final.
    return moves

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"    

    start = problem.getStartState()
    queue = []
    visited = []
    road = []

    # Marca ponto inicial como visitado e pega seus sucessores
    visited.append(start)
    for i in problem.getSuccessors(start):
        visited.append(i[0])
        queue.append((i[0], [i[1]]))

    # Inicia BFS
    while len(queue) > 0:
        # Primeiro elemento da fila e o retira da fila
        first = queue[0]
        queue.pop(0)

        # Verifica se eh o ponto final e marca seu caminho
        if problem.isGoalState(first[0]):
            road = first[1]
            break
        
        # Percorre seus sucessores, passando seu caminho
        for i in problem.getSuccessors(first[0]):
            if not i[0] in visited:
                # Marca elemento para nao entrar novamente na queue
                visited.append(i[0])

                road_element = first[1][:]
                road_element.append(i[1])
                queue.append((i[0], road_element))    

    # Retorna o caminho BFS
    return road
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    start = problem.getStartState()
    queue = util.PriorityQueue()
    visited = []
    moves = []

    #Marca start como visitado
    visited.append(start)

    #Coloca seus sucessores na fila
    for i in problem.getSuccessors(start):
        d = i[2]
        
        queue.push( (i[0], [i[1]], d), d)
        visited.append(i[0])

    # Enquanto nao for vazia
    while not queue.isEmpty():
        # Remove da fila e expande
        v = queue.pop()
        
        # Se for o objetivo, encerra
        if problem.isGoalState(v[0]):
            moves = v[1]
            break

        # Expande o no
        for i in problem.getSuccessors(v[0]):
            d = i[2]

            # Se nao tiver sido visitado anteriormente
            if not i[0] in visited:
                road = v[1][:]
                road.append(i[1])

                queue.push( (i[0], road, d+v[2]), d+v[2])
                visited.append(i[0])  
            # Caso contrario, verifica se distancia atual eh menor
            else:
                for index, j in enumerate(queue.heap):
                    if j[2][0] == i[0]:
                        if d+v[2] < j[2][2]:
                            # Deleta o pre armazenado
                            del queue.heap[index]

                            # reconstroi o caminho
                            road = v[1][:]
                            road.append(i[1])
    
                            # recola na fila com a distancia e prioridade atualizada
                            queue.push( (i[0], road, d+v[2]), d+v[2])
                            break
    
    return moves
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    
    start = problem.getStartState()
    queue = util.PriorityQueue()
    visited = []
    moves = []

    # Calcula heuristica do start e insere na fila e visitados
    hi = heuristic(start, problem)
    queue.push( (start, [], 0), hi)
    visited.append(start)

    while not queue.isEmpty():
        # remove por prioridade e expande
        v = queue.pop()
        
        # Se for objetivo, encerra
        if problem.isGoalState(v[0]):
            moves = v[1]
            break

        # Expandindo
        for i in problem.getSuccessors(v[0]):
            # Calcula heuristica e pega a distancia
            h = heuristic(i[0], problem)
            d = i[2]

            # Se nao tiver sido visitado anteriormente
            if not i[0] in visited:
                #Cria a rota
                road = v[1][:]
                road.append(i[1])

                # Insere na fila com prioridade usando heuristica
                queue.push( (i[0], road, d+v[2]), d+v[2]+h)
                visited.append(i[0])  
                
            # Se ja foi visitado, entao verifica se distancia eh menor
            else:
                for index, j in enumerate(queue.heap):
                    if j[2][0] == i[0]:
                        if d+h+v[2] < j[2][2]:
                            del queue.heap[index]

                            road = v[1][:]
                            road.append(i[1])
    
                            queue.push( (i[0], road, d+v[2]), d+v[2]+h)
                            break
    
    return moves
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
