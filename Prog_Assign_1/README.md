All code/work was created by Matthew Kennedy, for CS5800, spring semester 2021
The purpose of this program is to convert a provided NFA or NFA-Lambda into a DFA, as well as test input strings.
Examples of running this program located at the bottom.
Please note - any instances of "0" seen for state is used to represent the empty state, as the actual symbol for that is not recognized by graphviz


## Modules
There are 2 modules:
* An NFA/NFA-lambda to DFA converter, which can test input strings against newly-created DFA
* A DFA simulator, which will read in a DFA from file, and process a provided string against the DFA

## DFA simulator
To run this, there are 2 arguments that must be passed in:
1. File path to create DFA from

	For an example on how this file should look, see file "example_dfa.txt"
3. String to process


If arguments passed in are invalid or missing, program will prompt user for a file and string to process.


### Example:
./dfa_simulator.py "dfa_file.txt" "aaaabbbb"


## NFA/NFA-lambda to DFA converter
### Running
There are 3 ways to run this program:
* Using the .exe file (Windows only)
	
	example: ./nfa_lambda_dfa.exe (args)
	
* Using the python(3) command (windows/linux)

	example: python3 nfa_lambda_dfa.py (args)
	
* Running the .py file without using python(3) command (./nfa_lambda_dfa.py) (windows/linux)

	example: ./nfa_lambda_dfa.py (args)
	
<p>&nbsp;</p>
<p>&nbsp;</p>

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

<p>&nbsp;</p>
<p>&nbsp;</p>

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

<p>&nbsp;</p>
<p>&nbsp;</p>

### Input/flags:
As mentioned, this program requires an NFA/NFA-Lambda to be passed in. There are several ways to do this:
1. Using the -file argument

	When the -file argument is specified, the program will check if the argument following -flag is a valid file path.
	If the file is valid, the program will attempt to read from the file. For a file to be valid, the file must have 5 lines, where each line starts with a unique tuple element (qQ, sS, dD, q0Q0, fF), followed by a ':'.
	If the program fails to find all 5 elements in the file, the file will display the help message and exit.
	An example is provided, called "example.txt"
2. Using command line arguments

	If the -file argument is not specified, and the -hH argument is not specified, the program will check if the -qQ, -sS, -dD, -q0Q0, -fF arguments are provided. If so, the program checks the argument following each and verifies them.
3. Manual input

	If the there is no -file or -hH arguments, and the 5 tuple element arguments are not provided, the program will prompt the user for the 5 tuple elements to define the NFA/NFA-lambda. See above Tuple Elements section for formatting on each element

<p>&nbsp;</p>
<p>&nbsp;</p>

### Examples
./nfa_lambda_dfa.py -file example.txt

./nfa_lambda_dfa.py -h

./nfa_lambda_dfa.py -q "q0,q1,q2" -S "a,b,c,lambda" -D "(q0,a,q0,q1,q2),(q1,b,q1),(q2,c,q2),(q2,lambda,q1)" -Q0 "q0" -f "q1"

	This is from example 5.6.1 in the book
	
./nfa_lambda_dfa.py -Q "q0,q1,q2" -s "a,b" -d "(q0,a,q0,q1),(q1,b,q1,q2)" -q0 "q0" -F "q2"

	This is example 5.6.2 in the book

<p>&nbsp;</p>
<p>&nbsp;</p>

If at any point the input provided fails, there are likely helpful error messages, or a help message to display useful information.
	
