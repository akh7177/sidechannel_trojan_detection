#!/usr/bin/env python3

import re, sys, csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patheffects
from tabulate import tabulate

def parse_vcd(filename):
    id2name = {}
    toggles = defaultdict(int)
    last_val = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('$var'):
                parts = line.split()
                if len(parts) >= 5:
                    sigid = parts[3]
                    name = parts[4]
                    id2name[sigid] = name
            elif line.startswith('b'):
                parts = line.split()
                if len(parts) == 2:
                    val, sigid = parts
                    val = val[1:]
                    name = id2name.get(sigid)
                    if name:
                        prev = last_val.get(name)
                        if prev is not None and prev != val:
                            toggles[name] += 1
                        last_val[name] = val
            elif line and not line.startswith('$') and not line.startswith('#'):
                val = line[0]
                sigid = line[1:]
                name = id2name.get(sigid)
                if name:
                    prev = last_val.get(name)
                    if prev is not None and prev != val:
                        toggles[name] += 1
                    last_val[name] = val
    return toggles

#Compare

def compare_toggles(clean_tog, troj_tog,
                    rel_threshold=0.25):
    all_signals = sorted(set(list(clean_tog.keys()) + list(troj_tog.keys())))
    results = []
    for sig in all_signals:
        C = clean_tog.get(sig, 0)
        T = troj_tog.get(sig, 0)
        abs_diff = T - C
        if C == 0 and T == 0:
            rel = 0.0
        elif C == 0:
            rel = float('inf')
        else:
            rel = (T - C) / C

        suspicious = False
        if rel=='inf' or rel>=rel_threshold: suspicious=True

        results.append({
            "signal": sig,
            "clean": C,
            "trojan": T,
            "abs_diff": abs_diff,
            "rel": rel,
            "suspicious": suspicious,
        })
    return results

#Output stuff after this line

def output_results(results, csv_out="toggle_report.csv", png_out="toggle_compare.png"):

    with open(csv_out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["signal","clean","trojan","abs_diff","rel(%)","suspicious"])
        for r in results:
            rels = "inf" if r["rel"] == float('inf') else f"{r['rel']*100:.3f}"
            writer.writerow([r["signal"], r["clean"], r["trojan"], r["abs_diff"], rels, r["suspicious"]])
    print(f"\nCSV saved to {csv_out}")

    topN = min(40, len(results))
    top = results[:topN]
    labels = [r["signal"] for r in top]
    clean_vals = [r["clean"] for r in top]
    troj_vals = [r["trojan"] for r in top]
    x = np.arange(len(labels))
    width = 0.4

    fig, ax = plt.subplots(figsize=(max(10, len(labels)*0.25), 6))
    fig.patch.set_facecolor('black')       
    ax.set_facecolor('black')              

  
    clean_color = "#004c6d"
    troj_color = "#c1e7ff"

  
    plt.bar(x - width/2, clean_vals, width, label="Clean", color=clean_color)
    plt.bar(x + width/2, troj_vals, width, label="Trojan", color=troj_color)

  
    plt.xticks(x, labels,rotation=45,fontsize=9, color='white')
    plt.ylabel("Toggle count", color='white')
    plt.title("Signal Toggle Comparison (Clean vs Trojan)", color='white', fontsize=12)

    for i, r in enumerate(top):
        if r["suspicious"]:
            plt.text(i, max(clean_vals[i], troj_vals[i]) + 0.5, "*",
                    color="red", ha="center", fontsize=14, fontweight='bold')

    plt.legend(facecolor='black', edgecolor='white', fontsize=9, labelcolor='white')
    plt.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')

    plt.tight_layout()
    plt.savefig(png_out, dpi=200, facecolor=fig.get_facecolor())
    print(f"Plot saved to {png_out}")
    plt.show()

def print_results_table(results):
    table_data = []
    for r in results:
        rels = "inf" if r["rel"] == float('inf') else f"{r['rel']*100:.1f}%"
        table_data.append([
            r["signal"][:45],
            r["clean"],
            r["trojan"],
            r["abs_diff"],
            rels,
            "True" if r["suspicious"] else "False"
        ])
    headers = ["Signal", "Clean", "Trojan", "AbsDiff", "Rel %", "Susp"]

    print(tabulate(
        table_data,
        headers=headers,
        tablefmt="grid",
        colalign=("center", "center", "center", "center", "center", "center")
    ))

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 analyze_vcd.py clean.vcd trojan.vcd")
        sys.exit(1)
    clean_file = sys.argv[1]
    trojan_file = sys.argv[2]
    print("Parsing", clean_file)
    clean_tog = parse_vcd(clean_file)
    print("Parsing", trojan_file)
    troj_tog = parse_vcd(trojan_file)
    results = compare_toggles(clean_tog, troj_tog)
    print_results_table(results)
    output_results(results)

if __name__ == "__main__":
    main()
