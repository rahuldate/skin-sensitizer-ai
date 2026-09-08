import openmm as mm
from openmm import app, unit
import os

print("="*60)
print("🚀 OpenMM Molecular Dynamics Test Engine")
print(f"✅ OpenMM Version: {mm.__version__}")
print("="*60)

# Create a clean test peptide box (Alanine Dipeptide) to verify dynamics
pdb_text = """
ATOM      1  N   ALA A   1       1.000   1.000   1.000  1.00  0.00           N
ATOM      2  CA  ALA A   1       2.000   1.000   2.000  1.00  0.00           C
ATOM      3  C   ALA A   1       2.000   2.000   2.000  1.00  0.00           C
ATOM      4  O   ALA A   1       1.000   2.000   2.000  1.00  0.00           O
ATOM      5  CB  ALA A   1       3.000   1.000   1.000  1.00  0.00           C
TER
END
"""

with open("test_peptide.pdb", "w") as f:
    f.write(pdb_text.strip())

# Setup OpenMM System
pdb = app.PDBFile("test_peptide.pdb")
forcefield = app.ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')

modeller = app.Modeller(pdb.topology, pdb.positions)
modeller.addHydrogens(forcefield)

system = forcefield.createSystem(
    modeller.topology,
    nonbondedMethod=app.NoCutoff,
    constraints=app.HBonds
)

integrator = mm.LangevinMiddleIntegrator(
    300 * unit.kelvin,
    1.0 / unit.picoseconds,
    0.002 * unit.picoseconds  # 2 fs timestep
)

simulation = app.Simulation(modeller.topology, system, integrator)
simulation.context.setPositions(modeller.positions)

print("1. Minimizing Energy...")
simulation.minimizeEnergy(maxIterations=100)
state = simulation.context.getState(getEnergy=True)
print(f"   Potential Energy: {state.getPotentialEnergy()}")

print("2. Running 1,000 Step Production Trajectory...")
simulation.step(1000)
state_final = simulation.context.getState(getEnergy=True, getPositions=True)
print(f"   Final Potential Energy: {state_final.getPotentialEnergy()}")
print("\n🎉 OpenMM MD Engine Executed Successfully on your Mac!")
