from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import AerSimulator
import logging
import random

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Commands:
    def __init__(self, num_qubits=1):
        
        # Initialize Quantum and Classical Registers
        self.qreg_counter = 0
        self.creg_counter = 0
        self.qreg = QuantumRegister(num_qubits, 'qreg')
        self.creg = ClassicalRegister(num_qubits, 'creg')
        self.circuit = QuantumCircuit(self.qreg, self.creg)

        # Dictionaries to keep track of qubits and classical bits
        self.qubits = {}
        self.classical_bits = {}

        # Instruction queue for print commands
        self.instructions = []

        # Lists to store Alice's and Bob's bits and bases
        self.alice_bits = []
        self.alice_bases = []
        self.bob_bases = []
        self.bob_bits = []

        # Shared key after sifting
        self.shared_key = []

        # Eavesdropping flag and probability
        self.eavesdropping = False
        self.eavesdrop_probability = 0.5  # Default 50%

        # Error rate threshold for eavesdropping detection
        self.error_threshold = 0.1  # Default 10%

        # Initialize the AerSimulator backend
        self.simulator = AerSimulator()

    def define_qubit(self, q_name):
        if q_name in self.qubits:
            raise ValueError(f"Qubit '{q_name}' is already defined.")

        # Create a new QuantumRegister with a unique name
        qreg_name = f'qreg_{self.qreg_counter}'
        qreg = QuantumRegister(1, qreg_name)
        self.circuit.add_register(qreg)
        self.qubits[q_name] = qreg[0]  # Store the actual qubit reference
        logger.info(f"Defined qubit '{q_name}'.")

        # Create a corresponding ClassicalRegister with a unique name
        creg_name = f'creg_{self.creg_counter}'
        creg = ClassicalRegister(1, creg_name)
        self.circuit.add_register(creg)
        self.classical_bits[f'c_{q_name}'] = creg[0]
        logger.info(f"Defined classical bit 'c_{q_name}' for qubit '{q_name}'.")

        # Increment counters for unique register naming
        self.qreg_counter += 1
        self.creg_counter += 1

        logger.info(f"Defined qubit '{q_name}' and classical bit 'c_{q_name}'.")
    def apply_random_gate(self, q_name, target_q_name=None):
        available_gates = ["h", "x", "s", "t", "rz", "cnot"]
        gate = random.choice(available_gates)
        
        if gate == "rz":
            angle = random.uniform(0, 2 * 3.14159)
            self.apply_gate(gate, q_name, angle=angle)
        elif gate == "cnot":
            if not target_q_name:
                raise ValueError("CNOT gate requires a control and a target qubit.")
            self.apply_gate(gate, q_name, target_q=target_q_name)
        else:
            self.apply_gate(gate, q_name)

        logger.info(f"Applied random gate '{gate}' on '{q_name}'.")

    def alice_send_qubit(self, q_name):
        """Alice randomly selects a bit (0 or 1) and a basis ('+' for rectilinear, 'x' for diagonal) to send the qubit."""
        if q_name not in self.qubits:
            raise ValueError(f"Qubit '{q_name}' is not defined.")

        # Alice randomly selects a bit (0 or 1) and a basis ('+' for rectilinear, 'x' for diagonal)
        bit = random.randint(0, 1)
        basis = random.choice(['+', 'x'])  # Restrict basis to BB84 compatible choices

        self.alice_bits.append(bit)
        self.alice_bases.append(basis)

        # Prepare the qubit based on Alice's bit and basis
        if basis == '+':  # Rectilinear basis
            if bit == 1:
                self.circuit.x(self.qubits[q_name])  # Apply Pauli-X for bit 1
        elif basis == 'x':  # Diagonal basis
            self.circuit.h(self.qubits[q_name])  # Hadamard for diagonal basis
            if bit == 1:
                self.circuit.x(self.qubits[q_name])  # Apply Pauli-X after Hadamard if bit is 1

        # Add a barrier to separate operations
        self.circuit.barrier()

        logger.info(f"Alice sent qubit '{q_name}' with bit={bit} and basis='{basis}'.")
        logger.info(f"Current quantum circuit after Alice's send operation:\n{self.circuit}")
    def bob_measure_qubit(self, q_name, basis):
        """Bob randomly selects a basis (rectilinear or diagonal) to measure the qubit."""
        if q_name not in self.qubits:
            logger.error(f"Error: Qubit '{q_name}' not found in self qubits. Available qubits: {self.qubits.keys()}")
            raise ValueError(f"Qubit '{q_name}' is not defined in self qubits.")

        # Bob randomly selects a measurement basis
        basis = random.choice(['+', 'x'])  # '+' for rectilinear, 'x' for diagonal
        logger.info(f"Bob is measuring qubit '{q_name}' with basis '{basis}'.")

        # Store Bob's chosen basis
        self.bob_bases.append(basis)

        # Apply Hadamard gate if Bob chooses the diagonal basis
        if basis == 'x':  # Diagonal basis
            self.circuit.h(self.qubits[q_name])
            logger.info(f"Applied Hadamard gate on qubit '{q_name}' for diagonal measurement.")
        # If rectilinear basis is chosen, no gate is needed

        # Measure the qubit into the corresponding classical bit
        c_name = f'c_{q_name}'
        if c_name in self.classical_bits:
            try:
                logger.info(f"Measuring qubit '{q_name}' into classical bit '{c_name}'.")
                self.circuit.measure(self.qubits[q_name], self.classical_bits[c_name])
                logger.info(f"Current quantum circuit after Bob's measurement:\n{self.circuit}")
            except Exception as e:
                logger.error(f"Error while measuring qubit '{q_name}': {e}")
                raise
        else:
            logger.error(f"Error: Classical bit for qubit '{q_name}' is not defined.")
            raise ValueError(f"Classical bit for qubit '{q_name}' is not defined.")
    def sift_keys(self):
        """Sift keys by comparing Alice's and Bob's bases."""
        compiled_circuit = transpile(self.circuit, self.simulator)
        job = self.simulator.run(compiled_circuit, shots=1)
        result = job.result()
        counts = result.get_counts()

        outcome = list(counts.keys())[0][::-1]  # Reverse for little-endian order

        self.bob_bits = [int(outcome[i]) for i in range(len(self.qreg))]

        for i in range(len(self.alice_bases)):
            if self.alice_bases[i] == self.bob_bases[i]:
                self.shared_key.append(self.alice_bits[i])

        if not self.shared_key:
            logger.warning("No matching bases found. Shared key is empty.")
        else:
            logger.info(f"Sifted key: {self.shared_key}")

    def check_eavesdropping(self):
        """Check for eavesdropping by analyzing the error rate."""
        if not self.shared_key:
            logger.warning("No key to analyze for eavesdropping.")
            return

        errors = sum([1 for a, b in zip(self.alice_bits, self.bob_bits) if a != b])
        error_rate = errors / len(self.shared_key)

        if error_rate > self.error_threshold:
            logger.warning(f"Eavesdropping detected with error rate {error_rate}!")
        else:
            logger.info(f"No eavesdropping detected. Error rate: {error_rate}.")

    def generate_key(self, key_name, num_keys=1, key_length=None):
        """
        Generate one or more shared keys.
    
        :param key_name: Base name for the keys to be generated.
        :param num_keys: Number of keys to generate. Default is 1.
        :param key_length: Desired length of the key(s). If not provided, the full sifted key will be used.
        :raises ValueError: If no shared key is available or if the key length exceeds available bits.
        """

        if not self.shared_key:
            raise ValueError("No shared key available to generate.")
    
        # Determine the maximum key length available from the sifted key
        max_available_length = len(self.shared_key)
    
        if key_length is None:
            key_length = max_available_length
        elif key_length > max_available_length:
            raise ValueError(f"Requested key length {key_length} exceeds available sifted key length {max_available_length}.")
    
        # Generate multiple keys if requested
        keys = []
        for i in range(num_keys):
            # Generate a new key by using `key_length` bits from the shared key
            key = "".join(str(bit) for bit in self.shared_key[:key_length])
        
            # Optionally: Shuffle or rotate the sifted bits for multiple keys
            # (You could rotate or modify the shared key for each subsequent key)
        
            # Add key to the list of generated keys
            keys.append(key)
    
        # Store the generated keys with unique names
        for i, key in enumerate(keys):
            full_key_name = f"{key_name}_{i+1}" if num_keys > 1 else key_name
            setattr(self, full_key_name, key)
            print(f"Generated key '{full_key_name}': {key}")
    
        # Optionally: Return the list of keys for further processing or verification
        return keys
    def print_variable(self, var_name):
        # Schedule the variable for printing after execution
        self.instructions.append(("print", var_name))
        print(f"Scheduled print for variable '{var_name}'.")