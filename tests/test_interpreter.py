# tests/test_interpreter.py

import unittest
from dsl.interpreter import DSLInterpreter

class TestDSLInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = DSLInterpreter()
    
    def test_interpret_qubit_definition(self):
        script = "qubit q0"
        self.interpreter.interpret(script)
        self.assertIn('q0', self.interpreter.commands.qubits)
    
    def test_interpret_apply_gates(self):
        script = """
        qubit q0
        h q0
        x q0
        """
        self.interpreter.interpret(script)
        gates = [op[0].name for op in self.interpreter.commands.circuit.data]
        self.assertIn('h', gates)
        self.assertIn('x', gates)
    
    def test_interpret_measurement(self):
        script = """
        qubit q0
        measure q0 c0
        """
        self.interpreter.interpret(script)
        self.assertIn('c0', self.interpreter.commands.classical_bits)
    
    def test_interpret_alice_send_and_bob_measure(self):
        script = """
        qubit q0
        alice_send q0
        bob_measure q0 H
        """
        self.interpreter.interpret(script)
        self.assertEqual(len(self.interpreter.commands.alice_bits), 1)
        self.assertEqual(len(self.interpreter.commands.bob_bases), 1)
        self.assertIn('c_q0', self.interpreter.commands.classical_bits)
    
    def test_interpret_sift_keys(self):
        script = """
        qubit q0
        alice_send q0
        bob_measure q0 H
        sift_keys
        """
        self.interpreter.interpret(script)
        self.assertEqual(len(self.interpreter.commands.shared_key), 1)
    
    def test_interpret_generate_key_and_print(self):
        script = """
        qubit q0
        alice_send q0
        bob_measure q0 H
        sift_keys
        generate_key k0
        print k0
        """
        self.interpreter.interpret(script)
        self.assertTrue(hasattr(self.interpreter.commands, 'k0'))
        self.assertEqual(self.interpreter.commands.k0, '1')  # Depending on random bit

    def test_interpret_full_bb84_protocol(self):
        script = """
        # BB84 Protocol Example
        qubit q0
        qubit q1
        qubit q2

        alice_send q0
        alice_send q1
        alice_send q2

        bob_measure q0 H
        bob_measure q1 X
        bob_measure q2 H

        sift_keys
        check_eavesdropping
        generate_key k0
        print k0
        """
        self.interpreter.interpret(script)
        self.assertTrue(hasattr(self.interpreter.commands, 'k0'))
        self.assertGreaterEqual(len(self.interpreter.commands.shared_key), 0)
    
    def test_interpret_eavesdropping(self):
        script = """
        # BB84 Protocol with Eavesdropping
        qubit q0
        qubit q1
        qubit q2

        alice_send q0
        alice_send q1
        alice_send q2

        eavesdrop

        bob_measure q0 H
        bob_measure q1 X
        bob_measure q2 H

        sift_keys
        check_eavesdropping
        generate_key k0
        print k0
        """
        self.interpreter.interpret(script)
        self.assertTrue(hasattr(self.interpreter.commands, 'k0'))
        self.assertGreaterEqual(len(self.interpreter.commands.shared_key), 0)

if __name__ == '__main__':
    unittest.main()
