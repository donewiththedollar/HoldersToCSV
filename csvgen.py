#!/usr/bin/env python3
"""
csv_generator.py

Reads a text file containing lines like:
  1. Address: 0x1234…, Amount: 556003379.092453
and writes out a CSV with headers Rank,Address,Amount.
"""

import re
import csv
import argparse

def parse_holders(input_path):
    """
    Parse the input file for lines containing 'Address: <address>, Amount: <amount>'
    Returns a list of dicts: [{'Address': address, 'Amount': amount}, …]
    """
    pattern = re.compile(r"Address:\s*(0x[0-9A-Fa-f]+),\s*Amount:\s*([0-9]+\.[0-9]+)")
    holders = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                holders.append({
                    'Address': match.group(1),
                    'Amount': match.group(2),
                })
    return holders

def write_csv(holders, output_path):
    """
    Write the list of holders to a CSV file with headers Rank,Address,Amount.
    """
    fieldnames = ['Rank', 'Address', 'Amount']
    with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for idx, holder in enumerate(holders, start=1):
            writer.writerow({
                'Rank': idx,
                'Address': holder['Address'],
                'Amount': holder['Amount']
            })

def main():
    parser = argparse.ArgumentParser(
        description="Generate a CSV of token holders from a text list, with rank column"
    )
    parser.add_argument('input_file', help='Path to text file with raw holders list')
    parser.add_argument('output_file', help='Path to output CSV file')
    args = parser.parse_args()

    holders = parse_holders(args.input_file)
    if not holders:
        print(f"Error: No valid holder lines found in {args.input_file}", file=sys.stderr)
        exit(1)

    write_csv(holders, args.output_file)
    print(f"Success: {len(holders)} entries written to {args.output_file}")

if __name__ == '__main__':
    main()
