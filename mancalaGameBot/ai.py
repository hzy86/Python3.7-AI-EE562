import time
import random
import io

class key:
    def key(self):
        return "10jifn2eonvgp1o2ornfdlf-1230"

class ai:
    def __init__(self):
        self.t, self.start = 0, 0
        self.depth = 6

    class state:
        def __init__(self, a, b, a_fin, b_fin):
            self.a = a
            self.b = b
            self.a_fin = a_fin
            self.b_fin = b_fin
            self.path = {}

        def describe(self):
            return "  " + str(self.b[::-1]) + "\n" + str(self.b_fin) + "\t\t" + \
                    "     " + str(self.a_fin) + "\n" + "  " + str(self.a)

    # Kalah:
    #         b[5]  b[4]  b[3]  b[2]  b[1]  b[0]
    # b_fin                                         a_fin
    #         a[0]  a[1]  a[2]  a[3]  a[4]  a[5]
    # Main function call:
    # Input:
    # a: a[5] array storing the stones in your holes
    # b: b[5] array storing the stones in opponent's holes
    # a_fin: Your scoring hole (Kalah)
    # b_fin: Opponent's scoring hole (Kalah)
    # t: search time limit (ms)
    # a always moves first
    #
    # Return:
    # You should return a value 0-5 number indicating your move, with search time limitation given as parameter
    # If you are eligible for a second move, just neglect. The framework will call this function again
    # You need to design your heuristics.
    # You must use minimax search with alpha-beta pruning as the basic algorithm
    # use timer to limit search, for example:
    # start = time.time()
    # end = time.time()
    # elapsed_time = end - start
    # if elapsed_time * 1000 >= t:
    #    return result immediately
    def move(self, a, b, a_fin, b_fin, t):
        #For test only: return a random move
        # r = []
        # for i in range(6):
        #     if a[i] != 0:
        #         r.append(i)
        # # # To test the execution time, use time and file modules
        # # # In your experiments, you can try different depth, for example:
        # # f = open('time.txt', 'a') #append to time.txt so that you can see running time for all moves.
        # # # Make sure to clean the file before each of your experiment
        # # for d in [3, 5, 7]: #You should try more
        # #     f.write('depth = '+str(d)+'\n')
        # #     t_start = time.time()
        # #     self.minimax(depth = d)
        # #     f.write(str(time.time()-t_start)+'\n')
        # # f.close()
        # return r[random.randint(0, len(r)-1)]
        #But remember in your final version you should choose only one depth according to your CPU speed (TA's is 3.4GHz)
        #and remove timing code.

        #Comment all the code above and start your code here
        state = self.state(a, b, a_fin, b_fin)
        self.start = time.time()
        self.t = t
        value = self.max_value(state, float('-inf'), float('inf'), 0)

        f = open('time.txt', 'a')
        f.write(str(1000 * (time.time() - self.start)) + '\t' + str(self.t) + '\n')
        f.close()

        res = max(state.path, key = lambda key: state.path[key])

        return res

    # heuristic source
    # https://fiasco.ittc.ku.edu/publications/documents/Gifford_ITTC-FY2009-TR-03050-03.pdf
    def utility(self, state):
        """ return how far ahead of my opponent I am """
        return state.a_fin - state.b_fin

    # terminate if time out or one side wins
    def terminal_test(self, state, depth):
        """ return if the search reaches termination """
        return depth >= self.depth or 1000 * (time.time() - self.start) >= self.t \
                or state.a_fin > 36 or state.b_fin > 36 or (state.a_fin == state.b_fin and state.a_fin == 36)

    def action(self, hole, state):
        """ return a state after choosing the hole to move """
        if state.a[hole] == 0: return
        a1, b1 = state.a[:], state.b[:]
        result = self.state(a1, b1, state.a_fin, state.b_fin)

        # print "moving hole", hole, "before"
        # print result.describe()

        # distribute stones in the chosen hole counterclockwise
        index = hole
        for i in range(result.a[hole]):
            index += 1
            if index == 6:
                result.a_fin += 1
            elif index == 13:
                index = 0
                result.a[index] += 1
            elif index > 6 and index <= 12:
                result.b[index - 7] += 1
            else:
                result.a[index] += 1
        result.a[hole] = 0

        # last stone in own empty hole, take all the stones in the opponent's
        # opposite hole
        if index < 6 and result.a[index] == 1:
            result.a_fin += result.b[index]
            result.b[index] = 0

        # own side out of stones then the opponent move all of his stones to his kalah
        if self.out_of_stones(result.a):
            for i, stones in enumerate(result.b):
                result.b_fin += stones
                result.b[i] = 0
                
        return result

    def out_of_stones(self, holes):
        """ return true if all of the holes contain 0 stone """
        for stones in holes:
            if stones > 0: return False
        return True

    def successors(self, state):
        """ return successors as (hole, state) pairs """
        succ= {}
        for i in range(6):
            next = self.action(i, state)
            if next: succ[i] = next
        return succ

    def max_value(self, state, alpha, beta, depth):
        """ return the max heuristic value this state can obtain """
        if self.terminal_test(state, depth): return self.utility(state)
        v = float('-inf')
        for k, s in self.successors(state).iteritems():
            v = max(v, self.min_value(s, alpha, beta, depth + 1))
            state.path[k] = v
            if v >= beta: return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, depth):
        """ return the min heuristic value this state can obtain """
        if self.terminal_test(state, depth): return self.utility(state)
        v = float('inf')
        for k, s in self.successors(state).iteritems():
            v = min(v, self.max_value(s, alpha, beta, depth + 1))
            if v <= alpha: return v
            beta = min(beta, v)
        return v

    # calling function
    def minimax(self, depth):
        #example: doing nothing but wait 0.1*depth sec
        time.sleep(0.1*depth)
