import qiskit
import numpy as np
from qiskit.providers.aer import QasmSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from azure.quantum.qiskit import AzureQuantumProvider
from qiskit import Aer
import time

listaTeste = ["Hadamard", "PauliZ", "RX"]


def initialize(level):
    # provider = AzureQuantumProvider(
    # resource_id="/subscriptions/b1d7f7f8-743f-458e-b3a0-3e09734d716d/resourceGroups/aq-hackathons/providers/Microsoft.Quantum/Workspaces/aq-hackathon-01",
    # location="East US"
    # )
    # #print([backend.name() for backend in provider.backends()])
    # simulator = provider.get_backend("ionq.simulator")
    simulator = Aer.get_backend('statevector_simulator')
    scoreCircuit = QuantumCircuit(level+2, level+2)
    playerCircuit = QuantumCircuit(1,1)

    quantumGateDict= {"Hadamard": playerCircuit.h , "PauliX": playerCircuit.x,
                "PauliY": playerCircuit.y, "PauliZ": playerCircuit.z,}

    quantumRotDict= {"RX": playerCircuit.rx, "RY":playerCircuit.ry, "RZ":playerCircuit.rz}

    return scoreCircuit, playerCircuit, quantumGateDict, quantumRotDict, simulator

def execute_measurement(qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, measurement):
    playerCircuit.reset(0)
    for gate in qGates:
        if gate in quantumGateDict:
            quantumGateDict[gate](0)
        if gate in quantumRotDict:
            quantumRotDict[gate](np.pi/2, 0)
    if measurement == "Z":
        playerCircuit.measure(0, 0)
    elif measurement == "Y":
        playerCircuit.h(0)
        playerCircuit.sdg(0)
        playerCircuit.h(0)
        playerCircuit.measure(0,0)
    else:
        playerCircuit.h(0)
        playerCircuit.h(0)
        playerCircuit.measure(0, 0)

    compiled_circuit = transpile(playerCircuit, simulator)
    job = simulator.run(compiled_circuit, shots = 1)
    result = job.result()
    counts = result.get_counts(playerCircuit)
    # counts = {"0": 1, "1":2}
    if '0' in counts:
        return 0
    else:
        return 1

def Score_circuit(gate, scoreCircuit, score, scorelist):
    cnot_count = 0
    for i in range(2):
        scoreCircuit.reset(i)
    if gate == "H":
        score += 1
    else:
        if "H" in scorelist:
            score += 1
    for gates in scorelist:
        if gates == "H":
            scoreCircuit.h(0)
        else:
            scoreCircuit.cnot(cnot_count, cnot_count+ 1)
            cnot_count += 1                     
    return score, scoreCircuit

#scoreCircuit, playerCircuit, quantumGateDict, quantumRotDict, simulator = initialize()

#execute_measurement(listaTeste)
#playerCircuit.draw(output = 'mpl')
