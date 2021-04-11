import copy
import random

class NFA_DFA_Conv:
    def __init__(self, Q, S, D, F, q0):
        self.Q = Q
        self.S = S
        self.D = D
        self.F = F
        self.start_state = q0


    
    def convert_nfa_dfa(self):
        self.create_input_transition_func()
        self.get_q0_lambda_closure()
        self.create_dfa()



    def create_dfa(self):
        """Creates DFA from start state lambda closure and input transition functioin.
        For each node/symbol, check if that node has an arc reaching somewhere with that symbol
        If not, break node down into states, then get the infinitary union of each state's input 
        transitive function value (Y). 
        Then, convert to string representation (or just 0 if Y is empty), add Y to the list of nodes,
        and the string representation to the new DFA's transitive function table for that node/symbol
        After this is done, check all nodes in original states to see if any weren't added.

        Args:
            None
        Returns:
            None
        """

        self.Q_prime = [self.start_state_lambda_closure]
        self.S_prime = [s for s in self.S if s != 'lambda']
        self.D_prime = {}
        self.F_prime = []
        
        #Check each node, verify the key exists in (D)elta_prime
        for node in self.Q_prime:
            #Check each symbol that isn't lambda
            for symbol in self.S: 
                if symbol == 'lambda':
                    continue
                
                #Get string repr of node, check if it already exists in D_prime
                node_str_rep = ''.join(node)
                if not (node_str_rep, symbol) in self.D_prime.keys():                    
                    Y = []
                    #For each state in that node, get the input transitive function value
                    for state in node:
                        if self.input_trans_func[state, symbol]:
                            for s in self.input_trans_func[state, symbol]:
                                #If value not already in Y, add it
                                if s not in Y:
                                    Y.append(s)

                    #Create string repr for Y, used for Delta
                    Y.sort()
                    Y_str_rep = "{}".format(''.join(Y)) if Y else '0'
                    if Y:
                        if Y not in self.Q_prime:
                            self.Q_prime.append(Y)

                    #Append string repr of Y as transition from the node/symbol
                    self.D_prime[node_str_rep, symbol] = Y_str_rep

        #Check if any nodes that were in original Q are not in Q_prime
        for q in self.Q:
            if not any(q in new_states for new_states in self.Q_prime):
                #Add to Q_prime
                self.Q_prime.append([q])
                for symbol in self.S: 
                    if symbol == 'lambda':
                        continue
                    
                    Y = []
                    #For each state in that node, get the input transitive function value
                    if self.input_trans_func[q, symbol]:
                        for s in self.input_trans_func[q, symbol]:
                            #If value not already in Y, add it
                            if s not in Y:
                                Y.append(s)

                    #Create string repr for Y, used for Delta
                    Y.sort()
                    Y_str_rep = "{}".format(''.join(Y)) if Y else '0'
                    if Y:
                        if Y not in self.Q_prime:
                            self.Q_prime.append(Y)

                    #Append string repr of Y as transition from the node/symbol
                    self.D_prime[q, symbol] = Y_str_rep

        #Create F_prime
        self.F_prime = []
        for node in self.Q_prime:
            if any(s for s in node if s in self.F) and node not in self.F_prime:
                self.F_prime.append(node)

        #Add empty set recursion
        if any (v for v in self.D_prime.values() if v == '0'):
            for symbol in self.S:
                if symbol != 'lambda':
                    self.D_prime[('0', symbol)] = '0'
            self.Q_prime.append(['0'])



    def get_q0_lambda_closure(self):
        """Gets lambda closure for starting state - this is required for the NFA\Lambda to DFA algorithm
        No other lambda closures needed. Just sees if there are any lambda branches to reach out on from start state
        Follows as far as possible.
        
        Args:
            None
        Returns:
            None
        """

        self.start_state_lambda_closure = [self.start_state]

        if (self.start_state, 'lambda') in self.D.keys():
            states_to_visit = copy.deepcopy(self.D[self.start_state, 'lambda'])

            while states_to_visit:
                curr_state = states_to_visit[0]

                #Check if any other new lambda arcs from current state, add if there are
                next_states = copy.deepcopy([v for k, v in self.D.items() if (curr_state in k and 'lambda' in k) and (curr_state not in v) and (state not in v)])
                if next_states:
                    for s in next_states[0]:
                        if s not in states_to_visit:
                            states_to_visit.append(s)

                self.start_state_lambda_closure.append(curr_state)

                #Delete the state we were on from the list
                del states_to_visit[0]


    
    def create_input_transition_func(self):
        """Creates input transition function. Loops through each combo of state/symbol that isn't lambda
        Keeps track of states for that specific transition - appends normally if not lambda
        If any lambda arcs, adds any states reachable by lambda if original state has a looped element
        Additionally, tries to reach out on lambda branches and search for the specified symbol, adds that state if possible

        Args:
            None
        Returns:
            None
        """

        self.input_trans_func = {}

        for state in self.Q:
            for symbol in self.S: 
                if symbol == 'lambda':
                    continue
                #Create empty list of states to store in table
                states = []

                #If w is an input that isn't lambda, process normally (append to states)
                if (state, symbol) in self.D.keys():
                    for s in self.D[state, symbol]:
                        states.append(s)
                
                #Check if there are any arcs with lambda that are not loops. Need to deep copy to use del function later
                states_to_visit = copy.deepcopy([v for k, v in self.D.items() if (state in k and 'lambda' in k) and (state not in v)])

                #If there are lambda arcs, use algorithm
                if states_to_visit:
                    #Due to the way states to visit is acquired, it's just a nested list
                    states_to_visit = states_to_visit[0]
                    #Insert starting state into list
                    states_to_visit.insert(0, copy.deepcopy(state))
                    
                    #While more lambda arcs, repeat algorithm
                    while states_to_visit:
                        #Update current state
                        curr_state = states_to_visit[0]
                        
                        #Check if any other new lambda arcs from current state, add if there are
                        next_states = copy.deepcopy([v for k, v in self.D.items() if (curr_state in k and 'lambda' in k) and (curr_state not in v) and (state not in v)])
                        if next_states:
                            for s in next_states[0]:
                                if s not in states_to_visit:
                                    states_to_visit.append(s)
                        
                        #If the current state has transitions, check them for the input w. Add if it's there.
                        if (curr_state, symbol) in self.D.keys():
                            new_states = copy.deepcopy([s for s in self.D[curr_state, symbol]])
                            for s in new_states:
                                if s not in states:
                                    states.append(s)
                        
                        #Add the state if the initial state has a loop
                        if (state, symbol) in self.D and state in self.D[state, symbol]:
                            if curr_state not in states:
                                states.append(curr_state)

                        #Delete the state we were on from the list
                        del states_to_visit[0]

                #Set input transition for state/symbol to states found
                self.input_trans_func[state, symbol] = states




class Min_DFA:
    def __init__(self, Q, S, D, F, q0):
        self.Q = Q
        self.S = S
        self.D = D
        self.F = F
        self.start_state = q0



    def minimize_DFA(self):
        self.make_blocks()
        self.blocks_to_dfa()


    
    def make_blocks(self):
        non_final_states = [q for q in self.Q if q not in self.F]
        blocks = [non_final_states, self.F]
        blocks_changed = True

        #Do this until no new blocks
        while blocks_changed:
            blocks_changed = False

            for block in blocks:
                #If just 1 state in the block, then they are not
                if len(block) == 1: continue

                new_block = []
                first_state = block[0]
                for state in block[1:]:
                    #Test if first state and this state are equivalent
                    #Create 100 strings of length 100, test if each state matches at each character
                    equivalent = True
                    for _ in range(100):
                        #If already not equivalent, just exit the loop
                        if not equivalent: break

                        string_to_process = ''.join(random.choice(self.S) for i in range(100))
                        state1 = ''.join(first_state)
                        state2 = ''.join(state)

                        #Process each string for both states, check equivalency at every step
                        for char_to_process in string_to_process:
                            if not equivalent: break

                            state1 = ''.join(self.D[state1, char_to_process])
                            state2 = ''.join(self.D[state2, char_to_process])

                            #Check if equivalent
                            if (state1 in self.F and state2 not in self.F) or (state1 not in self.F and state2 in self.F):
                                blocks_changed = True
                                equivalent = False
                                new_block.append(state)
                                block.remove(state)
            
                #If the new block is not empty, add it to blocks
                if new_block: blocks.append(new_block)

        self.blocks = blocks



    def blocks_to_dfa(self):
        #Define F_prime and q0_prime
        self.F_prime = []
        for block in self.blocks:
            all_final = True
            for state in block:
                if state == self.start_state:
                    self.q0_prime = block

                if state not in self.F: 
                    all_final = False

            if all_final: self.F_prime.append(block)

        #For start block, get connection of each state
        self.D_prime = {}
        for block in self.blocks:
            block_transitions = {k: v for k, v in self.D.items() if k[0] in block}

            for s in self.S:
                #Get all transitions for a string in a block
                s_transitions = []
                for state in block:
                    if (state, s) in block_transitions:
                        s_transitions.append(block_transitions[state, s])

                #s_transitions = [q for q in s_transitions]
                #Verify each transition belongs to the same block
                for to_block in self.blocks:
                    #Check if any transitions belong in this block, then verify all transitions belong in this block
                    if any(state in to_block for state in s_transitions):
                        #If false, return an error
                        if not all(state in to_block for state in s_transitions): 
                            return -1
                        #If true, assign this as new transitions for D prime
                        else: 
                            s_transitions.sort()
                            self.D_prime[''.join(block), s] = ''.join(to_block)
                            break



    def process_string(self, string):
        """Processes a string provided one char at a time.
        If at any point no possible path to follow, returns False
        If entire string processed, but ends not on a final string, return False
        Otherwise, return True
        Args:
            None
        Returns:
            ACCEPT if string processed correctly
            REJECT if not
            Computations that took place
        """
    
        #Start state
        state = ''.join(self.q0_prime)
        computations = [[state, 'lambda', string, 'lambda']]

        #Process string, if ever not an option to move, just return False
        while string:
            char_to_process = string[0]
            if (state, char_to_process) in self.D_prime.keys():
                old_state = state
                state = ''.join(self.D_prime[state, char_to_process])

                if string: computations.append([old_state, state, string, char_to_process])
                else: computations.append([old_state, state, 'lambda', char_to_process])

                string = string[1:]

            else:
                computations.append('No transitions available')
                return 'REJECT', computations

        #Make sure actually in a final state
        for f in self.F_prime:
            f_str_repr = ''.join(f)
            if f_str_repr == state:
                computations.append('String finished processing, ended in final state')
                return 'ACCEPT', computations

        computations.append('String finished processing, ended at non-final state')
        return 'REJECT', computations



    def get_graphviz(self):
        final_nodes_str_repr = ''.join(["{{{}}}".format(''.join(f)) for f in self.F_prime])

        #Create string for all transition functions
        transitions_str_repr = ""
        for k, v in self.D_prime.items():
            start = "{{{}}}".format(k[0])
            end = "{{{}}}".format(v)
            label = k[1]

            line = '\t{} -> {} [ label = "{}" ];\n'.format(start, end, label)
            transitions_str_repr += line

        #Create actual output string
        output_str = 'digraph matt_kennedys_output {{'
        output_str += '\n\trankdir=LR;'
        output_str += '\n\tsize="8,5"'
        output_str += '\n\tnode [shape = doublecircle]; {}'.format(final_nodes_str_repr)
        output_str += '\n\tnode [shape = circle];'
        output_str += '\n{}'.format(transitions_str_repr)
        output_str += '}}'
        return output_str


if __name__ == '__main__': pass
