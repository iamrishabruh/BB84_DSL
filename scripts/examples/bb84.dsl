# BB84 Protocol with Eavesdropping
qubit q1
qubit q2
qubit q3
qubit q4
qubit q5
qubit q6
qubit q7
qubit q8
qubit q9
qubit q10


alice_send q1
alice_send q2
alice_send q3
alice_send q4
alice_send q5
alice_send q6
alice_send q7
alice_send q8
alice_send q9
alice_send q10


bob_measure q1 X
bob_measure q2 H
bob_measure q3 X
bob_measure q4 H
bob_measure q5 X
bob_measure q6 H
bob_measure q7 X
bob_measure q8 H
bob_measure q9 X
bob_measure q10 H


sift_keys
check_eavesdropping
generate_key k1
print k1


