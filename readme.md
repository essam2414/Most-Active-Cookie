# Most Active Cookie

A command line program to find the most active cookies for a given day (UTC) from a csv log.

## Requirements
- Python 3.11 or newer
- No third-party packages (only the Python standard library)

## Installation

From the project folder:

```
pip install .
```

This installs the `most-active-cookie` command.

## Usage

```
most-active-cookie -f cookie_log.csv -d 2018-12-09
```

Or, without installing:

```
python cookie_counter.py -f cookie_log.csv -d 2018-12-09
```

| Option | Description |
|---|---|
| `-f`, `--file` | Path to the cookie log CSV file |
| `-d`, `--date` | Date to search, in UTC, format `YYYY-MM-DD` |

### Exit codes

| Code | Meaning |
|---|---|
| `0` | Success (including when no cookies are found for the date) |
| `1` | The file could not be found or read |
| `2` | Invalid or missing arguments (e.g. a bad date) |

## Running the tests

From the project folder:

```
python -m unittest discover -s tests
```

## Assumptions

- The first line of the file is a header (`cookie,timestamp`).
- Timestamps are in ISO 8601 format and are converted to UTC before comparing with `-d`.
  Timestamps without a timezone are treated as UTC.
- Blank lines are ignored. Malformed rows (wrong number of columns, empty values,
  or invalid timestamps) are skipped and a warning is printed to stderr.
- If no cookies are found for the date, nothing is printed and the exit code is 0.
- Tied cookies are printed in the order they first appear in the file.
- The whole file fits in memory.

## Project structure

```
cookie_counter.py          # the program
cookie_log.csv             # sample log from the assignment
pyproject.toml             # packaging and the most-active-cookie command
tests/
    test_cookie_counter.py # unit and command-line tests
    test_log.csv           # sample log used by the tests
    test_bad_log.csv       # log with blank and malformed rows
```
