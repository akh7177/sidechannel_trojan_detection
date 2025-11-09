## Usage Instructions

**Step 1**- Install requirements from requirements.txt

`pip install -r requirements.txt`



**Step 2**- Generate the Value Change Dump (Output VCDs uploaded in project files)

`iverilog -D DUMPFILE="alu_clean.vcd" -o sim_clean.vvp alu_clean.v alu_tb.v`

Generate alu\_trojan.vcd in a similar manner



**Step 3** - Analyse the VCD files using analyze\_vcd.py script (Output uploaded in project files)

`python3 analyze_vcd.py alu_clean.vcd alu_trojan.vcd`
