import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from converter import NFA_DFA_Conv, Min_DFA



class MDFA_GUI:
    def __init__(self):
        app = QApplication(sys.argv)

        self.root_w = QWidget()
        self.root_w.resize(400, 300)
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
            if not self.Q.count(q) == 1: valid = False
            if self.S and q in self.S: valid = False
        
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
            if not self.S.count(s) == 1: valid = False
            if self.Q and s in self.Q: valid = False
        
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

        assert os.path.exists(file_path), "File must be a valid path"

        #Read file
        with open(file_path, 'r') as f:
            try:
                #For each line, strip white space and trailing newline
                for line in f:
                    line = line.replace('\n', '').replace(' ', '')

                    if (line[0] == 'q' or line[0] == 'Q') and not (line[0:2] == 'q0' or line[0:2] == 'Q0'): self.qInput.setText(line[2:])
                    elif (line[0] == 's' or line[0] == 'S'): self.sigmaInput.setText(line[2:])
                    elif (line[0] == 'd' or line[0] == 'D'): self.deltaInput.setText(line[2:])
                    elif (line[0:2] == 'q0' or line[0:2] == 'Q0'): self.q0 = line[3:]
                    elif (line[0] == 'f' or line[0] == 'F'): self.fInput.setText(line[2:])
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
        #converter = NFA_DFA_Conv(self.Q, self.S, self.D, self.F, self.q0)
        #converter.convert_nfa_dfa()

        #Minimize DFA
        #converter = Min_DFA(converter.Q_prime, converter.S_prime, converter.D_prime, converter.F_prime, converter.start_state_lambda_closure)
        converter = Min_DFA(self.Q, self.S, self.D, self.F, self.q0)
        converter.minimize_DFA()


if __name__ == '__main__':
    mdfa_gui = MDFA_GUI()