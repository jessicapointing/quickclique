#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:47:20 2019

@author: jessicapointing
"""

# =========
# Imports
# =========

import qiskit.aqua
from qiskit import Aer
from qiskit.aqua.components.initial_states import Zero
from qiskit.aqua.components.variational_forms import RY
from qiskit.aqua.operator import Operator
from qiskit.aqua.components.optimizers import AQGD
from qiskit.aqua.algorithms import VQE
from qiskit.aqua import QuantumInstance

# =========
# Constants
# =========

# number of qubits
num_qubits = 2

# pauli operators for a hamiltonian
pauli_dict = {
            'paulis': [{"coeff": {"imag": 0.0, "real": -1.052373245772859}, "label": "II"},
                       {"coeff": {"imag": 0.0, "real": 0.39793742484318045}, "label": "IZ"},
                       {"coeff": {"imag": 0.0, "real": -0.39793742484318045}, "label": "ZI"},
                       {"coeff": {"imag": 0.0, "real": -0.01128010425623538}, "label": "ZZ"},
                       {"coeff": {"imag": 0.0, "real": 0.18093119978423156}, "label": "XX"}
                       ]
    }

# ======================
# Setting up the circuit
# ======================

# define the initial state
init_state = Zero(num_qubits)

# get a variational ansatz
ansatz = RY(num_qubits)

# operator from hamiltonian
qubit_op = Operator.load_from_dict(pauli_dict)

qubit_op.run_minimum_clique_cover()

# group the operators
qubit_op.to_grouped_paulis()

# get an optimizer
optimizer = AQGD(maxiter=15, disp=True)

# form the algorithm
vqe = VQE(qubit_op, ansatz, optimizer)

# get a backend
backend = Aer.get_backend("statevector_simulator")

# get a quantum instance
qinstance = QuantumInstance(backend, shots=1024)

# ===================
# Do the optimization
# ===================

result = vqe.run(qinstance)

# ================
# Show the results
# ================

# output of the optimization
print(result)

# show the circuit
circuit = vqe.construct_circuit(list(range(8)), backend)[0]
print(circuit)