import qiskit
from qiskit import QuantumCircuit

print(qiskit.__version__)

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
