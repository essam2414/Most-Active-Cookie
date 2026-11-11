#!/usr/bin/env python3
import unittest
import subprocess
import sys
from datetime import date
from cookie_counter import get_active_frequencies, get_most_active_cookie, parse_utc_day

SCRIPT = "cookie_counter.py"
GOOD_LOG = "tests/test_log.csv"
BAD_LOG = "tests/test_bad_log.csv"

def run_program(*args):
    """Run cookie_counter.py from the command line and return the result."""
    return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True)

class TestParseUtcDay(unittest.TestCase):

    def test_utc_timestamp(self):
        self.assertEqual(parse_utc_day("2018-12-09T14:19:00+00:00"), date(2018, 12, 9))

    def test_positive_offset(self):
        # 01:00 at +05:00 is 20:00 on the previous day in UTC
        self.assertEqual(parse_utc_day("2018-12-09T01:00:00+05:00"), date(2018, 12, 8))

    def test_negative_offset(self):
        # 23:30 at -02:00 is 01:30 on the next day in UTC
        self.assertEqual(parse_utc_day("2018-12-09T23:30:00-02:00"), date(2018, 12, 10))

    def test_no_offset_is_utc(self):
        self.assertEqual(parse_utc_day("2018-12-09T00:30:00"), date(2018, 12, 9))

class TestGetActiveFrequencies(unittest.TestCase):

    def test_known_date(self):
        result = get_active_frequencies(GOOD_LOG, date(2018, 12, 9))
        self.assertEqual(result, {
            "AtY0laUfhglK3lC7": 2,
            "SAZuXPGUrfbcn5UA": 1,
            "5UAVanZf6UtGyKVS": 1,
        })

    def test_missing_date(self):
        result = get_active_frequencies(GOOD_LOG, date(2067, 12, 9))
        self.assertEqual(result, {})

    def test_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            get_active_frequencies("non_existent_file.csv", date(2018, 12, 9))

class TestGetMostActiveCookie(unittest.TestCase):

    def test_one_winner(self):
        self.assertEqual(get_most_active_cookie({"A": 3, "B": 1}), ["A"])

    def test_tie_returns_all(self):
        self.assertEqual(get_most_active_cookie({"A": 3, "B": 5, "C": 5, "D": 2}), ["B", "C"])

    def test_empty(self):
        self.assertEqual(get_most_active_cookie({}), [])

class TestCommandLine(unittest.TestCase):

    def test_spec_example(self):
        result = run_program("-f", GOOD_LOG, "-d", "2018-12-09")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "AtY0laUfhglK3lC7\n")

    def test_tie_prints_one_cookie_per_line(self):
        result = run_program("-f", GOOD_LOG, "-d", "2018-12-08")
        self.assertEqual(result.stdout, "SAZuXPGUrfbcn5UA\n4sMM2LxV07bPJzwf\nfbcn5UAVanZf6UtG\n")

    def test_date_not_in_log_prints_nothing(self):
        result = run_program("-f", GOOD_LOG, "-d", "2067-12-09")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_bad_rows_are_skipped(self):
        result = run_program("-f", BAD_LOG, "-d", "2018-12-09")
        self.assertEqual(result.stdout, "A\n")
        self.assertIn("Warning", result.stderr)

    def test_invalid_date(self):
        result = run_program("-f", GOOD_LOG, "-d", "09-12-2018")
        self.assertEqual(result.returncode, 2)

    def test_missing_file(self):
        result = run_program("-f", "non_existent_file.csv", "-d", "2018-12-09")
        self.assertEqual(result.returncode, 1)
        self.assertIn("not found", result.stderr)