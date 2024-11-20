# dsl/interpreter.py

import logging
from .parser import parse
from .commands import Commands

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DSLInterpreter:
    def __init__(self):
        self.commands = Commands()
        logger.info("DSLInterpreter initialized.")

    def interpret(self, script):
        logger.info("Starting interpretation of the script...")
        try:
            # Parse the script
            parsed_commands = parse(script)
            logger.info(f"Parsed commands: {parsed_commands}")
        except Exception as e:
            logger.error(f"Parsing Error: {e}")
            return

        # Execute each command in the parsed script
        for idx, cmd in enumerate(parsed_commands, start=1):
            action = cmd[0]
            logger.info(f"Executing command {idx}: {cmd}")
            try:
                if action == 'qubit':
                    self.commands.define_qubit(cmd[1])
                elif action in ['h', 'x', 's', 't', 'rz']:
                    self.commands.apply_gate(action, cmd[1])
                elif action == 'cnot':
                    self.commands.apply_gate(action, cmd[1], cmd[2])
                elif action == 'measure':
                    self.commands.measure_qubit(cmd[1], cmd[2])
                elif action == 'print':
                    self.commands.print_variable(cmd[1])
                elif action == 'alice_send':
                    self.commands.alice_send_qubit(cmd[1])
                elif action == 'bob_measure':
                    self.commands.bob_measure_qubit(cmd[1], cmd[2])
                elif action == 'sift_keys':
                    self.commands.sift_keys()
                elif action == 'check_eavesdropping':
                    self.commands.check_eavesdropping()
                elif action == 'generate_key':
                    self.commands.generate_key(cmd[1])
                elif action == 'eavesdrop':
                    self.commands.execute_eavesdropping()
                else:
                    logger.warning(f"Unknown action '{action}' encountered.")
            except ValueError as ve:
                logger.error(f"Execution Error: {ve}")
                return
            except Exception as ex:
                logger.error(f"Unexpected Error: {ex}")
                return

        # After executing all commands, handle print instructions
        self.execute_prints()

    def execute_prints(self):
        for instr in self.commands.instructions:
            if instr[0] == 'print':
                var_name = instr[1]
                # Check if it's a classical bit
                if var_name.startswith('c'):
                    if var_name in self.commands.classical_bits:
                        bit = self.retrieve_bit_value(var_name)
                        logger.info(f"{var_name} = {bit}")
                        print(f"{var_name} = {bit}")
                    else:
                        logger.error(f"Print Error: Classical bit '{var_name}' is not defined.")
                        print(f"Print Error: Classical bit '{var_name}' is not defined.")
                elif var_name.startswith('k'):
                    # It's a secret key
                    if hasattr(self.commands, var_name):
                        key = getattr(self.commands, var_name)
                        logger.info(f"{var_name} = {key}")
                        print(f"{var_name} = {key}")
                    else:
                        logger.error(f"Print Error: Key '{var_name}' is not defined.")
                        print(f"Print Error: Key '{var_name}' is not defined.")
                else:
                    logger.error(f"Print Error: Unknown variable '{var_name}'.")
                    print(f"Print Error: Unknown variable '{var_name}'.")

    def retrieve_bit_value(self, c_name):
        # Retrieve the measurement outcome from the sifted keys
        try:
            index = list(self.commands.classical_bits.keys()).index(c_name)
            if index < len(self.commands.sifted_bob_bits):
                return self.commands.sifted_bob_bits[index]
            else:
                return "Undefined"
        except ValueError:
            return "Undefined"
