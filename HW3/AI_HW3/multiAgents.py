from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        minGhostDistance = min([manhattanDistance(newPos, state.getPosition()) for state in newGhostStates])

        scoreDiff = childGameState.getScore() - currentGameState.getScore()

        pos = currentGameState.getPacmanPosition()
        nearestFoodDistance = min([manhattanDistance(pos, food) for food in currentGameState.getFood().asList()])
        newFoodsDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
        newNearestFoodDistance = 0 if not newFoodsDistances else min(newFoodsDistances)
        isFoodNearer = nearestFoodDistance - newNearestFoodDistance

        direction = currentGameState.getPacmanState().getDirection()
        if minGhostDistance <= 1 or action == Directions.STOP:
            return 0
        if scoreDiff > 0:
            return 8
        elif isFoodNearer > 0:
            return 4
        elif action == direction:
            return 2
        else:
            return 1


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (Part 1)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        # Begin your code (Part 1)
        """
        The "minimax" function first checks if the game is over. If so, it returns the 
        evaluation of the current state. If the game is not over, the function gets the 
        legal actions available to the agent in the current state. For each legal action, 
        the function gets the next game state that would result from taking that action.
        The function then recursively calls "minimax" for the next agent or next depth. 
        Depending on whether the current agent is Pacman or a ghost, the function chooses 
        the maximum or minimum score. If the current depth is 0, the function returns 
        the action that resulted in the maximum score. Otherwise, it returns the best score.
        """
        def minimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
            scores = []
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                nextGameState = gameState.getNextState(agentIndex, action)
                if agentIndex < gameState.getNumAgents() - 1:
                    score = minimax(agentIndex+1, depth, nextGameState)
                else:
                    score = minimax(0, depth+1, nextGameState)
                scores.append(score)
            
            if agentIndex > 0:
                score = min(scores)
            elif depth > 0:
                score = max(scores)
            else:
                return actions[scores.index(max(scores))]
            return score
        
        return minimax(0, 0, gameState)
        # End your code (Part 1)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (Part 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        # Begin your code (Part 2)
        """
        The "alpha_beta" function first checks if the game is over. If so, it returns the 
        evaluation of the current state. If the game is not over, the function gets the 
        legal actions available to the agent in the current state. For each legal action, 
        the function gets the next game state that would result from taking that action.
        The function then recursively calls "alpha_beta" for the next agent or next depth,
        passing in the updated alpha and beta values. It then performs alpha-beta pruning
        by updating the alpha or beta value if the score is lower or higher than the current 
        alpha or beta value, respectively. Depending on whether the current agent is 
        Pacman or a ghost, the function chooses the maximum or minimum score. If the current
        depth is 0, the function returns the action that resulted in the maximum score. 
        Otherwise, it returns the best score.
        """
        def alpha_beta(agentIndex, depth, gameState, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            scores = []
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                nextGameState = gameState.getNextState(agentIndex, action)
                if agentIndex < gameState.getNumAgents() - 1:
                    score = alpha_beta(agentIndex+1, depth, nextGameState, alpha, beta)
                else:
                    score = alpha_beta(0, depth+1, nextGameState, alpha, beta)
                scores.append(score)
                
                if agentIndex > 0:
                    if score < alpha:
                        return score
                    beta = min(beta, score)
                else:
                    if score > beta:
                        return score
                    alpha = max(alpha, score)

            if agentIndex > 0:
                score = min(scores)
            elif depth > 0:
                score = max(scores)
            else:
                return actions[scores.index(max(scores))]
            return score

        return alpha_beta(0, 0, gameState, float('-inf'), float('inf'))
        # End your code (Part 2)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (Part 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        # Begin your code (Part 3)
        """
        The "expectimax" function first checks if the game is over. If so, it returns the 
        evaluation of the current state. If the game is not over, the function gets the 
        legal actions available to the agent in the current state. For each legal action, 
        the function gets the next game state that would result from taking that action.
        The function then recursively calls "expectimax" for the next agent or next depth.
        Next, we calculate the expected score based on the scores obtained from all
        possible actions, assuming the ghosts choose their actions randomly based on
        some probability distribution. Depending on whether the current agent is Pacman or
        a ghost, the function chooses the maximum or expected score. If the current depth
        is 0, the function returns the action that resulted in the maximum score. 
        Otherwise, it returns the score.
        """
        def expectimax(agentIndex, depth, gameState):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)

            scores = []
            actions = gameState.getLegalActions(agentIndex)
            for action in actions:
                nextGameState = gameState.getNextState(agentIndex, action)
                if agentIndex < gameState.getNumAgents() - 1:
                    score = expectimax(agentIndex+1, depth, nextGameState)
                else:
                    score = expectimax(0, depth+1, nextGameState)
                scores.append(score)

            if agentIndex > 0:
                score = sum(scores) / len(scores)
            elif depth > 0:
                score = max(scores)
            else:
                return actions[scores.index(max(scores))]
            return score

        return expectimax(0, 0, gameState)
        # End your code (Part 3)


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (Part 4).
    """
    # Begin your code (Part 4)
    """
    The function starts by getting Pacman's position and the current score, and then
    sets some constants for the values of different game elements. Next, we calculates
    the distances between Pacman and each ghost, food, and capsule on the game board
    using the manhattanDistance function. For each ghost, we check if it is scared or not.
    For the food and capsule, we find the nearest one to Pacman. 
    Finally, the function returns the updated score for the current game state.
    """
    pos = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()
    
    GHOST = -5
    SCARED_GHOST = 200
    FOOD = 10
    CAPSULE = 15
    
    ghosts = currentGameState.getGhostStates()
    distance = [manhattanDistance(pos, ghost.getPosition()) for ghost in ghosts]
    for dis, ghost in zip(distance, ghosts):
        if dis:
            if ghost.scaredTimer:
                score += SCARED_GHOST / dis
            elif dis < 7:
                score += GHOST / dis
    
    foods = currentGameState.getFood()
    dis = [manhattanDistance(pos, food) for food in foods.asList()]
    if dis:
        nearestFoodDistance = min(dis)
        score += FOOD / nearestFoodDistance
    else:
        score += FOOD
    
    capsules = currentGameState.getCapsules()
    dis = [manhattanDistance(pos, capsule) for capsule in capsules]
    if dis:
        nearestCapsuleDistance = min(dis)
        score += CAPSULE / nearestCapsuleDistance
    else:
        score += CAPSULE
    
    return score
    # End your code (Part 4)

# Abbreviation
better = betterEvaluationFunction


