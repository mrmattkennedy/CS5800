#!/usr/bin/env python3

"""Purpose of this module is to convert NFA/NFA lambda to DFA
Course is CS 5800
Author is Matthew Kennedy

Example:
    Option to run either the .py file, or .exe file 
    With each option, can either
        1) Pass in a file to read input from
        2) Pass in command line arguments, specified in README
        3) Enter inputs manually
"""

import os
import sys
import copy
import random

try:
    import pyperclip
except:
    pass

class NFAL_DFA:
    """Class to convert NFA\Lambda to DFA, as well as process strings for this new DFA

    Attributes:
        Q (list): States of M (starting NFA\Lambda)
        S (list): (S)sigma of M (alphabet of NFA\Lambda), same for new DFA (M prime)
        D (dict): (D)elta of M (starting NFA\Lambda)
        start_state (str): q0, starting state of M
        F (list): Final (accepting) states of M
        input_trans_func (dict): input transition function of M
        start_state_lambda_closure - Used as starting point for algorithm to convert NFA\Lambda to DFA
        Q_prime (list): States of M prime (new DFA)
        S_prime (list): (S)sigma of M prime (alphabet of DFA), same for M
        D_prime (dict): (D)elta of M prime (new DFA)
        F_prime (list): Final (accepting) states of M prime
    """



    def __init__(self, args):
        """Init runs through methods procedurally
        Starts by processing input arguments and getting necessary tuple elements of NFA\Lambda
        Next, creates the input transition function for this NFA\Lambda
        Next, gets the lambda closure of starting state of M, for use in the new DFA
        Next, creates the DFA
        After this, the program will create the graphviz file, then test strings on this new DFA

        Args:
            args (list): Command line arguments passed in 

        Returns:
            None

        """

        self.process_inputs(args)
        self.create_input_transition_func()
        self.get_q0_lambda_closure()
        self.create_dfa()
        self.output_dfa()
        self.create_graphviz_format()
        self.test_strings()

    

    def test_strings(self):
        """Processes random strings, then gives user option to process strings

        Args:
            None

        Returns:
            None

        """

        print('\n\n')
        print('='*50)
        print('Testing strings')
        print('='*50)
        print('\n')

        run_random = input("Would you like to run pre-built random strings? If yes, type anything and hit enter, if not, just hit enter: ")
        if run_random:
            #Create random strings
            strings = []
            for _ in range(10):
                string = ''.join(random.choice(self.S_prime) for i in range(random.randint(8, 20)))
                strings.append(string)

            #Test/output random strings
            for s in strings:
                result, comps = self.process_string(s)
                self.print_nicely(s, result, comps)

        print()
        #Give the option for custom strings
        while True:
            s = input("Enter a string to test, or leave blank to exit:\t")
            if s:
                result, comps = self.process_string(s)
                self.print_nicely(s, result, comps)
            else:
                break

        

    def print_nicely(self, s, result, comps):
        """Prints out computations and result of processed string nicely
        Aligns each output to the right, so much easier to read

        Args:
            s (str): String that was processed
            result (str): ACCEPT or REJECT, result of the string being processed
            comps (list): List of each computation in processing

        Returns:
            None

        """

        #Get max length for each column
        col0 = [i[0] for i in comps]
        col0.append('Starting state')
        col0_maxlen = max([len(i) for i in col0])

        col1 = [i[1] for i in comps]
        col1.append('Ending state')
        col1_maxlen = max([len(i) for i in col1])

        col2 = [i[2] for i in comps]
        col2.append('Remaining string')
        col2_maxlen = max([len(i) for i in col2])

        col3 = [i[3] for i in comps]
        col3.append('Character processed')
        col3_maxlen = max([len(i) for i in col3])

        #Print column header, then pad each line with the max length for that column to align
        print('Starting state\tEnding state\tRemaining string\tCharacter processed')
        print('-'*75)
        for line in comps[:-1]:
            col0_str_padded = line[0].ljust(col0_maxlen)
            col1_str_padded = line[1].ljust(col1_maxlen)
            col2_str_padded = line[2].ljust(col2_maxlen)
            col3_str_padded = line[3].ljust(col3_maxlen)
            print('{}\t{}\t{}\t{}'.format(col0_str_padded, col1_str_padded, col2_str_padded, col3_str_padded))

        #Print last line (reason rejected or accepted), then print the string/actual result
        print(comps[-1])
        print('String {}: {}\n'.format(s, result))



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
        state = ''.join(self.start_state_lambda_closure)
        computations = [[state, 'lambda', string, 'lambda']]

        #Process string, if ever not an option to move, just return False
        while string:
            char_to_process = string[0]
            if (state, char_to_process) in self.D_prime.keys():
                old_state = state
                state = self.D_prime[state, char_to_process]
                string = string[1:]
                if string:
                    computations.append([old_state, state, string, char_to_process])
                else:
                    computations.append([old_state, state, 'lambda', char_to_process])
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
            
        
    
    def create_graphviz_format(self):
        """Creates graphviz formatted string (extra credit)
        Prints it, also prompts user for save path if they want that

        Args:
            None

        Returns:
            None

        """
        
        print("\n\nPlease enter a path to save file output to (leave blank to skip)")
        save_path = input("Note: the graphviz text will be printed out here, as well as automatically copied (if pyperclip found on system):\t")
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

        #Print text out, also put on clipboard
        print(output_str, '\n\n')
        try:
            pyperclip.copy(output_str)
        except:
            print('Module pyperclip not on system, so text will not be put on clipboard automatically')
        
        #Save output
        if save_path:
            with open(save_path, "w") as f:
                f.write(output_str)



    def output_dfa(self):
        """Displays each element of the tuple that defines the new DFA

        Args:
            None

        Returns:
            None

        """

        #Output transition table
        print('Input transition table of M:')
        for k, v in self.input_trans_func.items():
            if not v:
                v = ['0']
            v.sort()
            print('\t', k, '->', ''.join(v))
    
        print('\nTuple elements of newly created DFA:\n')
        #Output states
        print("Q prime:")
        for s in self.Q_prime:
            print('\t', ''.join(s))

        #Output alphabet
        print("\nSigma prime is the same as Sigma (alphabet) of M, except for removal of lambda if it was present")
        print(','.join(self.S_prime))

        #Output delta
        print('\nDelta prime:')
        for k, v in self.D_prime.items():
            print('\t', k, '->', v)

        #Output start state
        print('\nStart state of new DFA is equal to lambda closure of start state of M, which is {}'.format(''.join(self.start_state_lambda_closure)))

        #Output final states
        print('\nF prime:')
        for f in self.F_prime:
            print('\t', ''.join(f))

        print('\n\n')



    def create_dfa(self):
        """Creates DFA from start state lambda closure and input transition functioin.
        For each node/symbol, check if that node has an arc reaching somewhere with that symbol
        If not, break node down into states, then get the infinitary union of each state's input 
        transitive function value (Y). 
        Then, convert to string representation (or just 0 if Y is empty), add Y to the list of nodes,
        and the string representation to the new DFA's transitive function table for that node/symbol

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

                    #Append string repr of Y as transition from the node/symbol
                    self.D_prime[node_str_rep, symbol] = Y_str_rep
                    
        #Create F_prime
        self.F_prime = []
        for node in self.Q_prime:
            if any(s for s in node if s in self.F) and node not in self.F_prime:
                self.F_prime.append(node)

        #Add empty set recursion
        if any (v for v in self.D_prime.values() if v == '0'):
            for symbol in self.S:
                if symbol != 'lambda':
                    self.D_prime[(0, symbol)] = 0
            self.Q_prime.append('0')



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



    def process_inputs(self, args):
        """Processes input. Defaults to file path if -file flag specified
        If file unreadable or flag not set, checks if user passed in all other necessary flags
        If not that, prompts user for a file path, or the option to just enter info manually.

        Args:
            args (list): Command line arguments passed in to program

        Returns:
            None

        """

        print('\n'*50)
        #Check if help flag passed in
        if "-h" in args or "-H" in args:
            self.show_help()

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

        if not self.Q or not self.S or not self.D or not self.start_state or not self.F:
            self.show_help()
        
        #Verify elements
        self.verify_elements()



    def verify_elements(self):
        """After getting all 5 necessary tuple elements for M, this method verifies them
        For Q, just splits it
        For S, just splits it
        For D, splits accordingly, verifies all elements are present in Q and S
        For q0, verifies q0 is part of Q
        For F, verifies all F are part of Q

        Args:
            None

        Returns:
            None

        """

        #Get states, remove whitespace just in case user forgot to
        self.Q = [q.strip() for q in self.Q.split(',')]
        for q in self.Q:
            assert self.Q.count(q) == 1, "No duplicate states allowed"

        #Get alphabet, remove whitespace just in case user forgot to
        self.S = [s.strip() for s in self.S.split(',')]
        for s in self.S:
            assert self.S.count(s) == 1, "No duplicate alphabet items allowed"

        #Get transitions, remove whitespace just in case user forgot to
        temp_d = [d.strip().replace(')', '').replace('(', '') for d in self.D.split('),')]
        self.D = {}
        #Create dict for transitions, where key is (initial_state, input)
        for transition in temp_d:
            transition_split = [d.strip() for d in transition.split(',')]
            self.D[transition_split[0], transition_split[1]] = transition_split[2:]

            #Make sure input to process is part of S, states are part of Q
            assert transition_split[1] in self.S, "Input to process in transitions must be part of S, {} is not".format(transition_split[1])
            assert transition_split[0] in self.Q, "States specified in transition must be part of Q, {} is not".format(s)
            for s in transition_split[2:]:
                assert s in self.Q, "States specified in transition must be part of Q, {} is not".format(s)

        #Verify q0 is part of Q
        assert self.start_state in self.Q, "Starting state needs to be part of Q, {} is not part of {}".format(self.start_state, self.Q)

        #Get final states, remove whitespace just in case user forgot to
        self.F = [f.strip() for f in self.F.split(',')]
        for f in self.F:
            assert self.F.count(f) == 1, "No duplicate final states allowed"

        #Verify F is part of Q
        for f in self.F:
            assert f in self.Q, "Final state(s) needs to be part of Q, {} is not part of {}".format(f, self.Q)


    
    def read_file(self, file_path):
        """Reads a file for specified input, 
        looking at the start of each line for the required tuple elements

        Args:
            file_path (str): File path string to verify/read from

        Returns:
            None

        """

        assert os.path.exists(file_path), "File must be a valid path"

        #Read file
        with open(file_path, 'r') as f:
            tuple_counts = {'Q': 0, 'S': 0, 'D': 0, 'Q0': 0, 'F': 0} 

            #For each line, strip white space and trailing newline
            for line in f:
                line = line.rstrip('\n').strip()

                #Get counts of each element of tuple defining M, make sure there is 1 of each
                if line:
                    line_split = [l.strip() for l in line.split(':')]
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

                    elif (line_split[0] == 'f' or line_split[0] == 'F'):
                        tuple_counts['F'] += 1
                        self.F = line_split[1]
            
            #Assert each key has count of 1
            for k, v in tuple_counts.items():
                assert v == 1, "Must be exactly 1 value for {}".format(k)



    def show_help(self):
        """Prints help string, exits after

        Args:
            None
        Returns:
            None

        """

        print("""
        You can either execute .exe file, or run python file
3 options:
    Specify a file using flag below
    Run program with arguments passed in
    Enter inputs manually, prompted by program

Flags:
-hH - Help message (exits after showing)
-qQ - States of M
-sS - Alphabet of M (s for Sigma)
-dD - Transition functions of M (d for Delta)
-q0 - Start state of M
-fF - Final states of M
-file - Specifies a file to read from (format specified in README, example also provided)
    Note - if all flags provided, including -file, program will always try to read from file.""")
        input()
        sys.exit()




if __name__ == '__main__':
    converter = NFAL_DFA(sys.argv)