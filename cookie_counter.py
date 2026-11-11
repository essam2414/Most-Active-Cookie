#!/usr/bin/env python3
import argparse
import csv
import sys
from datetime import datetime, timezone, date

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print the most active cookie(s) for a given UTC day.")
    parser.add_argument("-f", "--file", required=True, help="Path to CSV file")
    parser.add_argument("-d", "--date", type=date.fromisoformat, required=True, help="UTC date, YYYY-MM-DD")
    return parser

def parse_utc_day(timestamp: str) -> date:
    moment = datetime.fromisoformat(timestamp)
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone(timezone.utc).date()

def get_active_frequencies(filename: str, target_day: date) -> dict:

    frequencies = {}

    with open(filename, mode='r', encoding='utf-8', newline='') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header row

        for row in reader:

            # skip blank lines
            if not row:
                continue

            # skip malformed rows
            if len(row) != 2 or not row[0] or not row[1]:
                print(f"Warning: skipping malformed row {reader.line_num}", file=sys.stderr)
                continue

            cookie = row[0]
            timestamp = row[1]

            try:
                current_day = parse_utc_day(timestamp)
            except ValueError:
                print(f"Warning: skipping row {reader.line_num}, bad timestamp", file=sys.stderr)
                continue

            # Compare the current day with the target day
            if current_day == target_day:

                if cookie in frequencies:
                    frequencies[cookie] += 1
                else:
                    frequencies[cookie] = 1

    return frequencies

def get_most_active_cookie(frequencies: dict) -> list:
    
    if not frequencies:
        return []

    # Get count for most active cookie
    max_frequency = max(frequencies.values())

    most_active = []

    # Loop through the frequencies dictionary to find all cookies with the maximum frequency
    for k, v in frequencies.items():

        if v == max_frequency:
            most_active.append(k)

    return most_active

def main():

    args = build_parser().parse_args()

    filename = args.file
    target_day = args.date

    # print most active cookies
    try:
        frequencies = get_active_frequencies(filename, target_day)
    except FileNotFoundError:
        print(f"Error: file {filename} not found.", file=sys.stderr)
        sys.exit(1)
    except (csv.Error, UnicodeDecodeError) as e:
        print(f"Error reading CSV file: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error opening file: {e}", file=sys.stderr)
        sys.exit(1)

    for cookie in get_most_active_cookie(frequencies):
        print(cookie)

if __name__ == "__main__":
    main()

