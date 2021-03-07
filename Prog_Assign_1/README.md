All code/work was created by Matthew Kennedy, for CS5800, spring semester 2021
The purpose of this program is to convert a provided NFA or NFA-Lambda into a DFA, as well as test input strings



### Running
There are 3 ways to run this program:
* Using the .exe file (Windows only)
	example: ./nfa_lambda_dfa.exe [flags]
* Using the python(3) command (windows/linux)
	example: python3 nfa_lambda_dfa.py [flags]
* Running the .py file without using python(3) command (./nfa_lambda_dfa.py) (windows/linux)
	example: ./nfa_lambda_dfa.py [flags]
	
	

### Command line arguments
* -hH

	If this arg is provided, no other args are processed - the program will display the help message and exit.
* -file
 
	If this arg is provided (and not -hH), no other args are processed - the program will attempt to read from a file
* -qQ
 
	Program will read this as the NFA/NFA-lambda's State element (list of states) - see "Tuple Elements" section below for formatting.
* -sS
 
	Program will read this as the NFA/NFA-lambda's Alphabet element (list of acceptable inputs to process) - see "Tuple Elements" section below for formatting.
* -dD
 
	Program will read this as the NFA/NFA-lambda's Transition functions - see "Tuple Elements" section below for formatting.
* -q0Q0
 
	Program will read this as the NFA/NFA-lambda's Starting state (q0) - see "Tuple Elements" section below for formatting.
* -fF

	Program will read this as the NFA/NFA-lambda's Final (accepting) states - see "Tuple Elements" section below for formatting.
	
	

### Tuple Elements
There are 5 tuple elements that define an NFA/NFA-Lambda: (Q, (S)igma, (D)elta, q0, (F)inal states)
Listed below is the way this program processes each element:
* Q

	Program reads this as a comma-separated-values list. Leading/trailing whitespace should be processed/removed by the program.
	Example: q0,q1,q2
* S

	Program reads this as a comma-separated-values list. Leading/trailing whitespace should be processed/removed by the program.
	**Note, the term "lambda" is used to describe lambda for NFA-lambda**
	Example: a,b,c,lambda
	
* D

	Program reads this as a comma-separated-values list. Each item is enclosed in paranthesis, with the following syntax: (transition_start_state, element_to_process, possible_transition_end_state_1, possible_transition_end_state_2, ...), (...)
	**Note, the term "lambda" is used to describe lambda for NFA-lambda**
	Example: (q0,a,q0,q1),(q1,b,q1,q2). The first tuple, (q0,a,q0,q1), reads as: There are 2 transitions from q0 that process the element a - one that ends at q0, and one that ends at q1.
	
* q0

	Program reads this as a single value, verifies the state provided is part of the States provided earlier.
	Example: q0
	
* F

	Program reads this as a comma-separated-values list. Leading/trailing whitespace should be processed/removed by the program.
	Example: q0,q1

	
	
### Input/flags:
As mentioned, this program requires an NFA/NFA-Lambda to be passed in. There are several ways to do this:
1. Using the -file arguments

	When the -file argument is specified, the program will check if the argument following -flag is a valid file path.
	If the file is valid, the program will attempt to read from the file. For a file to be valid, the file must have 5 lines, where each line starts with a unique tuple element (qQ, sS, dD, q0Q0, fF), followed by a ':'.
	If the program fails to find all 5 elements in the file, the file will display the help message and exit.
	An example is provided, called "example.txt"
2. Using command line arguments

	If the -file argument is not specified, and the -hH argument is not specified, the program will check if the -qQ, -sS, -dD, -q0Q0, -fF arguments are provided. If so, the program checks the argumenmt following each and verifies them.
3. Manual input

	If the there is no -file or -hH arguments, and the 5 tuple element arguments are not provided, the program will prompt the user for the 5 tuple elements to define the NFA/NFA-lambda.



If at any point the input provided fails, there are likely helpful error messages, or a help message to display useful information.
	
