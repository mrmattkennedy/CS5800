import os
import sys

class DFA_Sim:
    """Class to simulate DFA and process input string

    Attributes:
        Q (list): States of M (starting NFA\Lambda)
        S (list): (S)sigma of M (alphabet of NFA\Lambda), same for new DFA (M prime)
        D (dict): (D)elta of M (starting NFA\Lambda)
        start_state (str): q0, starting state of M
        F (list): Final (accepting) states of M
    """

    def __init__(self, args):
        """Reads file in, processes string, prints nicely

        Args:
            args (list): command line arguments

        Returns:
            None

        """
        print('\n'*50)
        test_str = self.read_file(args)
        self.verify_elements()
        result, comps = self.process_string(test_str)
        self.print_nicely(test_str, result, comps)
        input()
        

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
        state = self.start_state
        computations = [[state, 'lambda', string, 'lambda']]

        #Process string, if ever not an option to move, just return False
        while string:
            char_to_process = string[0]
            if (state, char_to_process) in self.D.keys():
                old_state = state
                state = ''.join(self.D[state, char_to_process])
                string = string[1:]
                if string:
                    computations.append([old_state, state, string, char_to_process])
                else:
                    computations.append([old_state, state, 'lambda', char_to_process])
            else:
                computations.append('No transitions available')
                return 'REJECT', computations

        #Make sure actually in a final state
        for f in self.F:
            f_str_repr = ''.join(f)
            if f_str_repr == state:
                computations.append('String finished processing, ended in final state')
                return 'ACCEPT', computations

        computations.append('String finished processing, ended at non-final state')
        return 'REJECT', computations



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



    def read_file(self, args):
        """Reads a file for specified input, 
        looking at the start of each line for the required tuple elements

        Args:
            file_path (str): File path string to verify/read from

        Returns:
            None

        """
        if len(args) != 2 or not os.path.exists(args[0]):
            print("Arguments passed in missing or invalid")
            file_path = input("Enter path to file:\t")
            test_str = input("Enter string to process:\t")
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

        return test_str

if __name__ == '__main__':
    dfa_sim = DFA_Sim(sys.argv)