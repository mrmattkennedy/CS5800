import os
import sys
import copy

class NFAL_DFA:
    def __init__(self, args):
        self.process_inputs(args)
        self.create_input_transition_func()
        self.get_q0_lambda_closure()
        self.create_dfa()
        self.output_dfa()
        self.create_graphviz_format()
        self.test_strings()


    
    def test_strings(self):
        #Test a few random strings
        strings = ['aaaaaaaaaa', 'bbbbbbbbbb', 'aaaaabbbbb', 'abbbbbbbbb', 'aaaabbbbbbbbbbbbbbbbbb', 'aaaaaaaba', 'baaaaaaba']
        for s in strings:
            print(s, self.process_string(s))

        #Give the option for custom strings
        while True:
            s = input("Enter a string to test, or leave blank to exit:\t")
            if s:
                print(s, self.process_string(s))
            else:
                break


    def process_string(self, string):
        #Start state
        state = ''.join(self.start_state_lambda_closure)

        #Process string, if ever not an option to move, just return False
        while string:
            char_to_process = string[0]
            if (state, char_to_process) in self.D_prime.keys():
                state = self.D_prime[state, char_to_process]
                string = string[1:]
            else:
                return False

        #Make sure actually in a final state
        if state not in self.F_prime:
            return False

        return True
            
        
    
    def create_graphviz_format(self):
        #save_path = input("\n\nPlease enter a path to save file output to:\t")
        #Create string for final states
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

        print(output_str, '\n\n')
        #Save output
        #with open(save_path, "w") as f:
        #    f.write(output_str)



    def output_dfa(self):
        #Output states
        print('States of M prime:')
        for s in self.Q_prime:
            print('\t{}'.format(s))

        #Output alphabet
        print('Alphabet is the same (Sigma prime = sigma)')

        #Output delta
        print('Delta prime:')
        for k, v in self.D_prime.items():
            print('\t', k, '->', v)

        #Output start state
        print('Start state of M prime is equal to lambda closure of start state of M, which is {}'.format(self.start_state_lambda_closure))

        #Output final states
        print('M prime final states:')
        for f in self.F_prime:
            print('\t', f)

        print('\n\n')



    def create_dfa(self):
        self.Q_prime = [self.start_state_lambda_closure]
        self.S_prime = self.S
        self.D_prime = {}
        self.start_state_prime = self.start_state
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
                    #For each state in taht node, get the input transitive function value
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

                    self.D_prime[node_str_rep, symbol] = Y_str_rep
                    if any(s for s in Y if s in self.F) and Y not in self.F_prime:
                        self.F_prime.append(Y)
        
        #Add empty set recursion
        for symbol in self.S:
            self.D_prime[(0, symbol)] = 0



    def get_q0_lambda_closure(self):
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
                self.input_trans_func[state, symbol] = states



    def process_inputs(self, args):
        #Check first if there is a path specified, and verify path is valid
        if "-file" in args:
            file_path = args[args.index("-file")+1]
            self.read_file(file_path)

        #Verify each required argument is flagged
        elif (('-q' in args or '-Q' in args) and 
                ('-s' in args or '-S' in args) and
                ('-d' in args or '-D' in args) and
                ('-q0' in args or '-Q0' in args) and
                ('-f' in args or '-F' in args)):

                #Get states
                q_key = '-q' if '-q' in args else '-Q'
                self.Q = args[args.index(q_key)+1]

                #Get (s)igma, or alphabet
                s_key = '-s' if '-s' in args else '-S'
                self.S = args[args.index(s_key)+1]

                #Get (d)elta, or transition functions
                d_key = '-d' if '-d' in args else '-D'
                self.D = args[args.index(d_key)+1]

                #Get q0, or start state
                q0_key = '-q0' if '-q0' in args else '-Q0'
                self.start_state = args[args.index(q0_key)+1]

                #Get final states
                f_key = '-f' if '-f' in args else '-F'
                self.F = args[args.index(f_key)+1]
        
        #Get necessary tuple elements as input
        else:
            print('\n\n')
            file_path = input("Enter a file path (or just hit enter to instead enter each element manually):\t")
            if file_path:
                self.read_file(file_path)
            else:
                self.Q = input("Enter the states (Q), deliminated by commas (i.e. state1,state2...):\t")
                self.S = input("Enter the alphabet (S), deliminated by commas (i.e. a,b,lambda,...):\t")
                self.D = input("Enter the transition functions (Q), using the following format:\n(start_state,input_to_process,end_state_1,end_state_2,...),...:\t")
                self.start_state = input("Enter the start state:\t")
                self.F = input("Enter the final state(s), F, deliminated by commas (i.e. state1,state2...):\t")

        
        #Verify elements
        self.verify_elements()



    def verify_elements(self):
        #Get states, remove whitespace just in case user forgot to
        self.Q = [q.strip() for q in self.Q.split(',')]

        #Get alphabet, remove whitespace just in case user forgot to
        self.S = [s.strip() for s in self.S.split(',')]

        #Get transitions, remove whitespace just in case user forgot to
        temp_d = [d.strip().replace(')', '').replace('(', '') for d in self.D.split('),')]
        self.D = {}
        #Create dict for transitions, where key is (initial_state, input)
        for transition in temp_d:
            transition_split = [d.strip() for d in transition.split(',')]
            self.D[transition_split[0], transition_split[1]] = transition_split[2:]

        #Verify q0 is part of Q
        assert self.start_state in self.Q, "Starting state needs to be part of Q, {} is not part of {}".format(self.start_state, self.Q)

        #Get final states, remove whitespace just in case user forgot to
        self.F = [f.strip() for f in self.F.split(',')]

        #Verify F is part of Q
        for f in self.F:
            assert f in self.Q, "Final state(s) needs to be part of Q, {} is not part of {}".format(f, self.Q)


    
    def read_file(self, file_path):
        assert os.path.exists(file_path), "File must be a valid path"

        #Read file
        with open(file_path, 'r') as f:
            tuple_counts = {'Q': 0, 'S': 0, 'D': 0, 'Q0': 0, 'F': 0} 

            #For each line, strip white space and trailing newline
            for line in f:
                line = line.rstrip('\n').strip()

                #Get counts of each element of tuple defining M, make sure there is 1 of each
                if line:
                    line_split = line.split(': ')
                    if (line_split[0] == 'q' or line_split[0] == 'Q'):
                        tuple_counts['Q'] += 1
                        self.Q = line_split[1]

                    elif (line_split[0] == 's' or line_split[0] == 'S'):
                        tuple_counts['S'] += 1
                        self.S = line_split[1]

                    elif (line_split[0] == 'd' or line_split[0] == 'D'):
                        tuple_counts['D'] += 1
                        self.D = line_split[1]

                    elif (line_split[0] == 'q0' or line_split[0] == 'Q0'):
                        tuple_counts['Q0'] += 1
                        self.start_state = line_split[1]

                    elif (line_split[0] == 'fs' or line_split[0] == 'F'):
                        tuple_counts['F'] += 1
                        self.F = line_split[1]
            
            #Assert each key has count of 1
            for k, v in tuple_counts.items():
                assert v == 1, "Must be exactly 1 value for {}".format(k)

if __name__ == '__main__':
    converter = NFAL_DFA(sys.argv)