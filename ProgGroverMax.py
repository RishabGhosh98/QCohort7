#Problem statement You have two integers return the largest.Using grovers search
# Assumptions :- Only numbers belonging to the set of integers.

from qiskit import QuantumCircuit, execute, Aer
import math

def find_the_largest_number(number1,number2) -> int:
    # Determine the number of qubits required to represent the input
    n = max(math.ceil(math.log2(abs(number1))), math.ceil(math.log2(abs(number2)))) + 1
    
    # Create a quantum circuit with n qubits and a single classical output bit
    qc = QuantumCircuit(n, 1)

    # Initialize the qubits to a superposition state
    for i in range(n):
        qc.h(i)
    
    diff = number1 - number2
    # Define an oracle that flips the sign of the target state
    def oracle():
        # Calculate the difference between a and b
        

        # Convert the difference to binary and pad with zeros if necessary
        binary_diff = bin(abs(diff))[2:].zfill(n)

        # Apply X gates to the qubits where binary_diff = 1
        for i in range(n):
            if binary_diff[i] == '1':
                qc.x(i)

        # Apply a phase flip to the target state
        qc.cz(n-1, 0)

        # Apply X gates again to undo the previous X gates
        for i in range(n):
            if binary_diff[i] == '1':
                qc.x(i)

    # Define a diffusion operator that amplifies the amplitude of the marked state
    def diffusion():
        for i in range(n):
            qc.h(i)
            qc.x(i)
        qc.h(n-1)
        #qc.mct(list(range(n-1)), n-1)
        qc.h(n-1)
        for i in range(n):
            qc.x(i)
            qc.h(i)

    # Apply Grover's algorithm
    num_iterations = round(math.pi/4 * math.sqrt(2**n/(abs(diff))))
    for i in range(num_iterations):
        oracle()
        diffusion()

    # Measure the qubits and return the result
    qc.measure(n-1, 0)
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend, shots=1).result()
    counts = result.get_counts()
    print(qc)
    if '1' in counts:
        if number1>0:
            return number1
        else :
            return number2
    else:
        if number2>0:
            return number2
        else :
            return number1

#calling the function
x=find_the_largest_number(-291,13)
print(x)
