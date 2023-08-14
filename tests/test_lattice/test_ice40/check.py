import subprocess
import magma as m
from magma.testing.utils import check_gold

def check_ice40(callee_file, name, circuit):

    m.compile(f"build/{name}", circuit, output="mlir-verilog")

    assert subprocess.run(["yosys"]+["-q"]+["-p",f"synth_ice40 -top Top -json build/{name}.json"]+[f"build/{name}.v"]).returncode==0

    assert check_gold(callee_file, f"{name}.v")
    assert check_gold(callee_file, f"{name}.json")

