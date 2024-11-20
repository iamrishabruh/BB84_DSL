# tests/test_bb84.py

import unittest
from dsl.interpreter import DSLInterpreter

class TestBB84Protocol(unittest.TestCase):
    def setUp(self):
        self.interpreter = DSLInterpreter()
    
    def test_bb84_execution(self):
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
    
    def test_bb84_with_eavesdropping(self):
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
