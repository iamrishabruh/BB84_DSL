# Quantum Key Distribution Domain-Specific Language

## Overview
The **Quantum Key Distribution (QKD) DSL** is a Domain-Specific Language designed for simulating quantum cryptography and post-quantum cryptography algorithms. It provides cryptographers and developers with an intuitive platform for defining and testing quantum-safe cryptographic protocols, particularly focusing on QKD mechanisms.

## Features
- Specialized syntax Enables defining quantum cryptographic protocols with ease.
- Quantum operations support for single and multi-qubit gates (Hadamard, CNOT).
- Classical operations handle key sifting, eavesdropping detection, and hybrid quantum-classical operations.
- Simulation tools test eavesdropping scenarios and security protocols.
- Built modular to be easily adaptable for future developments in post-quantum cryptography.

## Grammar Overview
The DSL uses a grammar defined in Extended Backus-Naur Form (EBNF) to support constructs for quantum operations, function definitions, conditional statements, and more.

### Grammar Snippet
```ebnf
<program> ::= { <statement> }

<quantum_op> ::= "qubit" <identifier>
               | <gate_op>
               | <measurement>

<gate_op> ::= "h" <identifier>
            | "x" <identifier>
            | "y" <identifier>
            | "z" <identifier>
            | "cnot" <identifier> <identifier>

<measurement> ::= "measure" <identifier> <identifier> [ "shots" "=" <number> ]
```

## Example Usage
```python
qubit q1
qubit q2
h q1          # Apply Hadamard gate to q1
x q2          # Apply Pauli-X gate to q2
cnot q1 q2    # Apply CNOT gate
measure q1 c1 shots=1024  # Measure q1 into c1 with 1024 shots
```

## Classical Operations
```python
alice_send q1            # Alice sends qubit q1
bob_measure q1 c1        # Bob measures q1 into classical bit c1
sift_keys                # Sift the keys
check_eavesdropping      # Detect eavesdropping
generate_key key1, 2, 256 # Generate 2 keys, each 256 bits
```

## Functions and Control Structures
```python
function prepare_qubit(q, bit) {
    if (bit == 1) {
        x q
    } else {
        h q
    }
    alice_send q
}

call prepare_qubit(q1, 1)
```

## Installation and Usage

1) Clone the repository:
```bash
git clone https://github.com/iamrishabruh/PQC.git
cd PQC
```
2) Install required dependencies:
```bash
pip install -r requirements.txt
```

3) Run the interpreter:
```bash
python main.py your_script.dsl
```

Write your scripts in .dsl files and pass them to the interpreter.

## Core Components
- Parses DSL scripts into an Abstract Syntax Tree (AST).
- Executes DSL statements, managing quantum operations and classical logic.
- Command Module: Handles execution of quantum gates, measurements, and cryptographic functions.

## Future Enhancements
- A real-time console for command testing.
- Circuit visualization and measurement outcomes.
- Connect the DSL with quantum hardware or simulators.
- Simulate various eavesdropping strategies and analyze security.

## Contributing
Contributions are welcome! Please follow these steps:

1) Fork the repository.
2) Create a new branch for your feature or bugfix.
3) Submit a pull request with a clear description of your changes.

## License
This project is licensed under the MIT License.

## Contact
If you have any questions or feedback, feel free to reach out:

Email: [rchouhan.network@gmail.com]
