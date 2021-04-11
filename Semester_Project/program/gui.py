import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from converter import NFA_DFA_Conv, Min_DFA

try:
    import pyperclip
except:
    pass



class MDFA_GUI:
    def __init__(self):
        app = QApplication(sys.argv)

        self.root_w = QWidget()
        self.root_w.resize(600, 300)
        self.root_w.setWindowTitle('NFA to minimized DFA')
        self.root_w.show()
        
        table_widget = MDFA_Tabs(self.root_w)
        
        layout = QGridLayout()
        self.root_w.setLayout(layout)
        layout.addWidget(table_widget)
        sys.exit(app.exec_())


class MDFA_Tabs(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        layout = QVBoxLayout(self)
        
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)
        
        # Add tabs
        self.tabs.addTab(self.tab1,"Input")
        self.tabs.addTab(self.tab2,"Simulator")

        #Create tuple items
        self.Q, self.S, self.F, self.q0 = None, None, None, None
        
        # Create first tab
        tab1Layout = QGridLayout()

        #Input for Q
        qLabel = QLabel("Q: ")
        self.qInput = QLineEdit()
        self.qInput.setPlaceholderText("q0, q1, q2, q3...")
        self.qInput.setToolTip("This is where you enter the states, separated by a comma")
        self.qInput.editingFinished.connect(self.verify_all)
        regex = QRegExp("[A-Za-z0-9, ]+")
        self.qInput.setValidator(QRegExpValidator(regex))

        self.qInputErrorLabel = QLabel("")
        self.qInputErrorLabel.setStyleSheet("color: red;")
        self.qInputErrorLabel.setAlignment(Qt.AlignCenter)

        tab1Layout.addWidget(self.qInputErrorLabel, 0, 0, 1, 2)
        tab1Layout.addWidget(qLabel, 1, 0)
        tab1Layout.addWidget(self.qInput, 1, 1)


        #Input for Sigma
        sigmaLabel = QLabel("∑: ")
        self.sigmaInput = QLineEdit()
        self.sigmaInput.setPlaceholderText("a, b, c...")
        self.sigmaInput.setToolTip("This is where you enter the language, separated by a comma")
        self.sigmaInput.editingFinished.connect(self.verify_all)
        regex = QRegExp("[A-Za-z0-9, ]+")
        self.sigmaInput.setValidator(QRegExpValidator(regex))

        self.sigmaInputErrorLabel = QLabel("")
        self.sigmaInputErrorLabel.setStyleSheet("color: red;")
        self.sigmaInputErrorLabel.setAlignment(Qt.AlignCenter)

        tab1Layout.addWidget(self.sigmaInputErrorLabel, 2, 0, 1, 2)
        tab1Layout.addWidget(sigmaLabel, 3, 0)
        tab1Layout.addWidget(self.sigmaInput, 3, 1)


        #Input for Delta
        deltaLabel = QLabel("δ: ")
        self.deltaInput = QLineEdit()
        self.deltaInput.setPlaceholderText("(q0,a,q0,q1),(q1,b,q1,q2)")
        self.deltaInput.setToolTip("This is where you enter the Transition Function, separated by a comma.\nAs an example, (q0,a,q0,q1) reads as: There are 2 transitions from q0 that process the element a -\none that ends at q0, and one that ends at q1")
        self.deltaInput.editingFinished.connect(self.verify_all)
        regex = QRegExp("[A-Za-z0-9, ()]+")
        self.deltaInput.setValidator(QRegExpValidator(regex))
        
        self.deltaInputErrorLabel = QLabel("")
        self.deltaInputErrorLabel.setStyleSheet("color: red;")
        self.deltaInputErrorLabel.setAlignment(Qt.AlignCenter)

        tab1Layout.addWidget(self.deltaInputErrorLabel, 4, 0, 1, 2)
        tab1Layout.addWidget(deltaLabel, 5, 0)
        tab1Layout.addWidget(self.deltaInput, 5, 1)


        #Input for F
        fLabel = QLabel("F: ")
        self.fInput = QLineEdit()
        self.fInput.setPlaceholderText("q0, q1, q2, q3...")
        self.fInput.setToolTip("This is where you enter the final, or accepting, states. Each one must be an element of Q")
        self.fInput.editingFinished.connect(self.verify_all)
        regex = QRegExp("[A-Za-z0-9, ]+")
        self.fInput.setValidator(QRegExpValidator(regex))

        self.fInputErrorLabel = QLabel("")
        self.fInputErrorLabel.setStyleSheet("color: red;")
        self.fInputErrorLabel.setAlignment(Qt.AlignCenter)
        
        tab1Layout.addWidget(self.fInputErrorLabel, 6, 0, 1, 2)
        tab1Layout.addWidget(fLabel, 7, 0)
        tab1Layout.addWidget(self.fInput, 7, 1)


        #Input for q0
        q0Label = QLabel("q0: ")
        self.q0Combo = QComboBox()
        self.q0Combo.currentIndexChanged.connect(self.changeq0)

        tab1Layout.addWidget(QLabel(""), 8, 0, 1, 2)
        tab1Layout.addWidget(q0Label, 9, 0)
        tab1Layout.addWidget(self.q0Combo, 9, 1)
        tab1Layout.addWidget(QLabel(""), 10, 0, 1, 2)

        #Buttons to convert, import file, and exit
        convertBtn = QPushButton("Convert")
        convertBtn.clicked.connect(self.start_converting)
        #Exit
        exitBtn = QPushButton("Exit")
        exitBtn.clicked.connect(sys.exit)
        #File input
        importFileBtn = QPushButton("Import txt file")
        importFileBtn.clicked.connect(self.getFile)

        tempHBoxLayout = QHBoxLayout()
        tempHBoxLayout.addWidget(convertBtn)
        tempHBoxLayout.addWidget(importFileBtn)
        tempHBoxLayout.addWidget(exitBtn)

        tab1Layout.addLayout(tempHBoxLayout, 11, 0, 1, 2)

        #Set layout
        self.tab1.setLayout(tab1Layout)
        self.tab2.setEnabled(False)
        
        # Add tabs to widget
        layout.addWidget(self.tabs)
        self.setLayout(layout)



    def verify_states(self):
        #Read text, split into separate states
        self.Q = self.qInput.text()
        #Verify not empty
        if not self.Q:
            self.Q = None
            self.q0Combo.clear()
            return

        #Split into different items
        self.Q = [q.strip() for q in self.Q.split(',')]

        #Check if duplicates
        valid = True
        for q in self.Q:
            if not q: valid = False
            if not self.Q.count(q) == 1: valid = False
            if self.S and q in self.S: valid = False

            for char in q: 
                if not char.isalnum(): 
                    valid = False
        
        #If valid, do nothing - else, show error
        if valid: 
            self.qInput.setStyleSheet("")
            self.qInputErrorLabel.setText("")

            #Set combo box items for q0
            self.q0Combo.clear()
            for q in self.Q:
                self.q0Combo.addItem(q)
        else: 
            self.qInput.setStyleSheet("border: 1px solid red;")
            self.qInputErrorLabel.setText("All states must be unique, and must not be the same as any alphabet items")
            self.Q = None
            self.q0Combo.clear()



    def verify_alphabet(self):
        #Read text, split into separate states
        self.S = self.sigmaInput.text()
        if not self.S:
            self.S = None
            return

        self.S = [s.strip() for s in self.S.split(',')]

        #Check if duplicates, or if alphabet item same as a state
        valid = True
        for s in self.S:
            if not s: valid = False
            if not self.S.count(s) == 1: valid = False
            if self.Q and s in self.Q: valid = False

            for char in s: 
                if not char.isalnum(): 
                    valid = False
        
        #If valid, do nothing - else, show error
        if valid: 
            self.sigmaInput.setStyleSheet("")
            self.sigmaInputErrorLabel.setText("")
        else: 
            self.sigmaInput.setStyleSheet("border: 1px solid red;")
            self.sigmaInputErrorLabel.setText("All items must be unique, and must not be the same as any states")
            self.S = None



    def verify_final_states(self):
        #Read text, split into separate states
        self.F = self.fInput.text()
        if not self.F:
            self.F = None
            return

        self.F = [f.strip() for f in self.F.split(',')]

        #Check if duplicates
        valid = True
        for f in self.F:
            if not self.F.count(f) == 1: valid = False
            if self.Q and f not in self.Q: valid = False
        
        #If valid, do nothing - else, show error
        if valid: 
            self.fInput.setStyleSheet("")
            self.fInputErrorLabel.setText("")
        else: 
            self.fInput.setStyleSheet("border: 1px solid red;")
            self.fInputErrorLabel.setText("All items must be unique, and must be part of provided states (Q)")
            self.F = None
        

        
    def verify_transitions(self):
        #Read text, split into separate items
        self.D = self.deltaInput.text()
        if not self.D:
            self.D = None
            return

        #Get transitions, remove whitespace just in case user forgot to
        temp_d = [d.strip().replace(')', '').replace('(', '') for d in self.D.split('),')]
        self.D = {}
        
        #Create dict for transitions, where key is (initial_state, input)
        for transition in temp_d:
            err_msg = ""
            transition_split = [d.strip() for d in transition.split(',')]
            self.D[transition_split[0], transition_split[1]] = transition_split[2:]
            
            valid_start_state = True
            valid_alphabet = True

            #Make sure input to process is part of S, states are part of Q
            if self.Q and transition_split[0] not in self.Q: valid_start_state = False
            if self.S and transition_split[1] not in self.S: valid_alphabet = False

            #Check if start state provided part of Q
            if not valid_start_state: err_msg = "Start state of each transition must be part of Q"
            #Check if alphabet provided valid
            if not valid_alphabet: err_msg = "String to process in each transition must be part of ∑"

            #Check if each end state provided is part of Q
            valid_transitions = True
            for s in transition_split[2:]:
               if self.Q and s not in self.Q: valid_transitions = False

            #Check if each transition end state valid
            if not valid_transitions: err_msg = "End state of each transition must be part of Q"
            
            if err_msg:
                self.deltaInput.setStyleSheet("border: 1px solid red;")
                self.deltaInputErrorLabel.setText(err_msg)
                self.D = None
                return

        self.deltaInput.setStyleSheet("")
        self.deltaInputErrorLabel.setText("")


    
    def changeq0(self):
        self.q0 = self.q0Combo.currentText()



    def verify_all(self):
        self.verify_states()
        self.verify_alphabet()
        self.verify_final_states()
        self.verify_transitions()
        comboBoxItems = [self.q0Combo.itemText(i) for i in range(self.q0Combo.count())]
        if self.q0 in comboBoxItems: self.q0Combo.setCurrentText(self.q0)
        else: self.q0 = None


    
    def getFile(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(),"Text files (*.txt)")
        self.read_file(file_path[0])



    def read_file(self, file_path):
        """Reads a file for specified input, 
        looking at the start of each line for the required tuple elements
        
        Args:
            file_path (str): File path string to verify/read from
        Returns:
            None
        """

        if not os.path.exists(file_path): return

        #Read file
        with open(file_path, 'r') as f:
            try:
                #For each line, strip white space and trailing newline
                for line in f:
                    line = line.replace('\n', '').replace(' ', '')
                    line = ''.join([c for c in line if c.isalnum() or c == ',' or c == ':' or c == '(' or c == ')'])
                    if line.count(':') > 1: continue

                    print(line[0:2])
                    if (line[0:2] == 'q:' or line[0:2] == 'Q:') and not (line[0:3] == 'q0:' or line[0:3] == 'Q0:'): self.qInput.setText(line[2:])
                    elif (line[0:2] == 's:' or line[0:2] == 'S:'): self.sigmaInput.setText(line[2:])
                    elif (line[0:2] == 'd:' or line[0:2] == 'D:'): self.deltaInput.setText(line[2:])
                    elif (line[0:3] == 'q0:' or line[0:3] == 'Q0:'): self.q0 = line[3:]
                    elif (line[0:2] == 'f:' or line[0:2] == 'F:'): self.fInput.setText(line[2:])
            except: pass
            finally: self.verify_all()


        
    def start_converting(self):
        if not self.Q:
            self.qInputErrorLabel.setText("States must be properly specified")
            return

        if not self.S:
            self.sigmaInputErrorLabel.setText("Alphabet must be properly specified")
            return

        if not self.D:
            self.deltaInputErrorLabel.setText("Transition function must be properly specified")
            return

        if not self.F:
            self.fInputErrorLabel.setText("Final states must be properly specified")
            return

        self.q0 = self.q0Combo.currentText()

        #Convert NFA to DFA
        converter = NFA_DFA_Conv(self.Q, self.S, self.D, self.F, self.q0)
        converter.convert_nfa_dfa()

        #Minimize DFA
        DFA_Q = [''.join(q) for q in converter.Q_prime]
        DFA_S = converter.S_prime
        DFA_D = converter.D_prime
        DFA_F = [''.join(f) for f in converter.F_prime]
        DFA_q0 = ''.join(converter.start_state_lambda_closure)

        self.converter = Min_DFA(DFA_Q, DFA_S, DFA_D, DFA_F, DFA_q0)
        self.converter.minimize_DFA()

        #Create simulator tab
        self.tab2.setEnabled(True)
        delta_str = ""
        for k, v in converter.D_prime.items():
            delta_str += "({}, {}, {}),".format(k[0], k[1], v)
        delta_str = delta_str[:-1]

        self.create_sim_layout([''.join(b) for b in self.converter.blocks], self.converter.S, delta_str, [''.join(f) for f in self.converter.F_prime], ''.join(self.converter.q0_prime))
        self.tabs.setCurrentIndex(1)



    def create_sim_layout(self, Q, S, D, F, q0):
        try:
            self.minDFA_qInput.setText(', '.join(Q))
            self.minDFA_sigmaInput.setText(', '.join(S))
            self.minDFA_deltaInput.setText(D)
            self.minDFA_fInput.setText(', '.join(F))
            self.minDFA_q0Input.setText(q0)

            self.wInputErrorLabel.setStyleSheet("color: red; border: none;")
            self.wInputErrorLabel.setText("")
        
        except:
            #Create tab
            tab2Layout = QGridLayout()

            #Input for Q
            minDFA_qLabel = QLabel("Q: ")
            self.minDFA_qInput = QLineEdit(', '.join(Q))
            #minDFA_qInput.setEnabled(False)

            tab2Layout.addWidget(minDFA_qLabel, 0, 0)
            tab2Layout.addWidget(self.minDFA_qInput, 0, 1)

            #Input for Sigma
            minDFA_sigmaLabel = QLabel("∑: ")
            self.minDFA_sigmaInput = QLineEdit(', '.join(S))
            self.S_prime = S
            #minDFA_sigmaInput.setEnabled(False)

            tab2Layout.addWidget(minDFA_sigmaLabel, 1, 0)
            tab2Layout.addWidget(self.minDFA_sigmaInput, 1, 1)


            #Input for Delta
            minDFA_deltaLabel = QLabel("δ: ")
            self.minDFA_deltaInput = QLineEdit(D)
            #minDFA_deltaInput.setEnabled(False)

            tab2Layout.addWidget(minDFA_deltaLabel, 2, 0)
            tab2Layout.addWidget(self.minDFA_deltaInput, 2, 1)


            #Input for F
            minDFA_fLabel = QLabel("F: ")
            self.minDFA_fInput = QLineEdit(', '.join(F))
            #minDFA_fInput.setEnabled(False)
            
            tab2Layout.addWidget(minDFA_fLabel, 3, 0)
            tab2Layout.addWidget(self.minDFA_fInput, 3, 1)


            #Input for q0
            minDFA_q0Label = QLabel("q0: ")
            self.minDFA_q0Input = QLineEdit(q0)
            #minDFA_qInput.setEnabled(False)

            tab2Layout.addWidget(minDFA_q0Label, 4, 0)
            tab2Layout.addWidget(self.minDFA_q0Input, 4, 1)

            #Create line to test strings
            wLabel = QLabel("String to process: ")
            self.wInput = QLineEdit("")
            self.wInput.editingFinished.connect(self.verify_string)

            self.wInputErrorLabel = QTextEdit("")
            self.wInputErrorLabel.setStyleSheet("color: red; border: none;")
            self.wInputErrorLabel.setAlignment(Qt.AlignCenter)
            self.wInputErrorLabel.setFont(QFont('Helvetica', 10))

            tab2Layout.addWidget(self.wInputErrorLabel, 5, 0, 1, 2)
            tab2Layout.addWidget(wLabel, 6, 0)
            tab2Layout.addWidget(self.wInput, 6, 1)

            #Buttons to Process and exit
            processBtn = QPushButton("Process string")
            processBtn.clicked.connect(self.process_string)
            copyBtn = QPushButton("Copy GraphViz")
            copyBtn.clicked.connect(self.copy_graphviz)
            exitBtn = QPushButton("Exit")
            exitBtn.clicked.connect(sys.exit)
            

            tempHBoxLayout = QHBoxLayout()
            tempHBoxLayout.addWidget(processBtn)
            tempHBoxLayout.addWidget(copyBtn)
            tempHBoxLayout.addWidget(exitBtn)

            tab2Layout.addLayout(tempHBoxLayout, 7, 0, 1, 2)


            #Set layout
            self.tab2.setLayout(tab2Layout)



    def verify_string(self):
        for c in self.wInput.text():
            if c not in self.S_prime:
                self.wInputErrorLabel.setStyleSheet("color: red; border: none;")
                self.wInputErrorLabel.setText("All characters in string must be part of alphabet")
                self.wInput.setStyleSheet("border: 1px solid red;")
                return False

        self.wInputErrorLabel.setText("")
        self.wInput.setStyleSheet("")
        return True




    def process_string(self):
        if self.verify_string():
            result, comps = self.converter.process_string(self.wInput.text())
            if result == 'ACCEPT': self.wInputErrorLabel.setStyleSheet("color: green; border: none;")
            elif result == 'REJECT': self.wInputErrorLabel.setStyleSheet("color: red; border: none;")

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

            result_str = ""
            result_str += result
            result_str += '\n'
            result_str += 'Starting state  Ending state  Remaining string  Character processed\n'
            result_str += '-'*75
            result_str += '\n'
            for line in comps[:-1]:
                col0_str_padded = line[0].ljust(col0_maxlen)
                col1_str_padded = line[1].ljust(col1_maxlen)
                col2_str_padded = line[2].ljust(col2_maxlen)
                col3_str_padded = line[3].ljust(col3_maxlen)
                
                result_str += '{}\t{}\t{}\t{}\n'.format(col0_str_padded, col1_str_padded, col2_str_padded, col3_str_padded)

            result_str += comps[-1]
            self.wInputErrorLabel.setText(result_str)



    def copy_graphviz(self):
        try:
            pyperclip.copy(self.converter.get_graphviz())
            self.wInputErrorLabel.setStyleSheet("color: green; border: none;")
            self.wInputErrorLabel.setText("Graphviz output copied successfully")
        except:
            msgBox = QMessageBox()
            msgBox.setTextInteractionFlags(Qt.TextSelectableByMouse)
            msgBox.setIcon(QMessageBox.Warning)
            msgbox_txt = "Failed to copy graphviz - Pyperclip module not installed. Please copy the graphviz text from below.\n\n"
            msgbox_txt += self.converter.get_graphviz()
            msgBox.setText(msgbox_txt)
            msgBox.setWindowTitle("Failed to copy")
            msgBox.setStandardButtons(QMessageBox.Ok)
            msgBox.exec()



if __name__ == '__main__':
    mdfa_gui = MDFA_GUI()