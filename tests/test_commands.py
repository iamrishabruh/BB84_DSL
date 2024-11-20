# tests/test_commands.py

import unittest
from dsl.commands import Commands

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.commands = Commands()
    
    def test_define_qubit(self):
        self.commands.define_qubit('q0')
        self.assertIn('q0', self.commands.qubits)
    
    def test_define_existing_qubit(self):
        self.commands.define_qubit('q0')
        with self.assertRaises(ValueError):
            self.commands.define_qubit('q0')
    
    def test_apply_h_gate(self):
        self.commands.define_qubit('q0')
        self.commands.apply_gate('h', 'q0')
        gates = [op[0].name for op in self.commands.circuit.data]
        self.assertIn('h', gates)
    
    def test_apply_x_gate(self):
        self.commands.define_qubit('q0')
        self.commands.apply_gate('x', 'q0')
        gates = [op[0].name for op in self.commands.circuit.data]
        self.assertIn('x', gates)
    
    def test_apply_cnot_gate(self):
        self.commands.define_qubit('q0')
        self.commands.define_qubit('q1')
        self.commands.apply_gate('cnot', 'q0', 'q1')
        gates = [op[0].name for op in self.commands.circuit.data]
        self.assertIn('cx', gates)
    
    def test_measure_qubit(self):
        self.commands.define_qubit('q0')
        self.commands.measure_qubit('q0', 'c0')
        self.assertIn('c0', self.commands.classical_bits)
    
    def test_measure_nonexistent_qubit(self):
        with self.assertRaises(ValueError):
            self.commands.measure_qubit('q0', 'c0')
    
    def test_print_variable_classical_bit(self):
        self.commands.define_qubit('q0')
        self.commands.measure_qubit('q0', 'c0')
        self.commands.print_variable('c0')
        self.assertIn(('print', 'c0'), self.commands.instructions)
    
    def test_print_variable_key(self):
        self.commands.shared_key = [1, 0, 1]
        self.commands.generate_key('k0')
        self.commands.print_variable('k0')
        self.assertIn(('print', 'k0'), self.commands.instructions)
        self.assertEqual(self.commands.k0, '101')
    
    def test_alice_send_qubit(self):
        self.commands.define_qubit('q0')
        self.commands.alice_send_qubit('q0')
        self.assertEqual(len(self.commands.alice_bits), 1)
        self.assertEqual(len(self.commands.alice_bases), 1)
    
    def test_bob_measure_qubit(self):
        self.commands.define_qubit('q0')
        self.commands.bob_measure_qubit('q0', 'H')
        self.assertEqual(len(self.commands.bob_bases), 1)
        self.assertIn('c_q0', self.commands.classical_bits)
    
    def test_sift_keys(self):
        self.commands.define_qubit('q0')
        self.commands.alice_send_qubit('q0')
        self.commands.bob_measure_qubit('q0', 'H')
        self.commands.sift_keys()
        # Since we have only one qubit, and bases are both 'H', shared_key should have one bit
        self.assertEqual(len(self.commands.shared_key), 1)
    
    def test_generate_key_without_shared_key(self):
        with self.assertRaises(ValueError):
            self.commands.generate_key('k0')
    
    def test_generate_key(self):
        self.commands.shared_key = [1, 0, 1]
        self.commands.generate_key('k0')
        self.assertTrue(hasattr(self.commands, 'k0'))
        self.assertEqual(self.commands.k0, '101')
    
    def test_execute_eavesdropping(self):
        self.commands.define_qubit('q0')
        self.commands.execute_eavesdropping(custom_probability=0.5)
        # Check if classical bit for eavesdropping exists
        self.assertIn('c_eve_q0', self.commands.classical_bits)

if __name__ == '__main__':
    unittest.main()
