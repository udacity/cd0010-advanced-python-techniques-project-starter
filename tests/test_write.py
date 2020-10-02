"""Check that streams of results can be written to files.

The `write_to_csv` and `write_to_json` methods should follow a specific output
format, described in the project instructions.

There's some sketchy file-like manipulation in order to avoid writing anything
to disk and avoid letting a context manager in the implementation eagerly close
the in-memory file - so be warned that the workaround is gnarly.

To run these tests from the project root, run:

    $ python3 -m unittest --verbose tests.test_write

These tests should pass when Task 4 is complete.
"""
import collections
import collections.abc
import contextlib
import csv
import datetime
import io
import json
import pathlib
import unittest
import unittest.mock


from extract import load_neos, load_approaches
from database import NEODatabase
from write import write_to_csv, write_to_json


TESTS_ROOT = (pathlib.Path(__file__).parent).resolve()
TEST_NEO_FILE = TESTS_ROOT / 'test-neos-2020.csv'
TEST_CAD_FILE = TESTS_ROOT / 'test-cad-2020.json'


def build_results(n):
    neos = tuple(load_neos(TEST_NEO_FILE))
    approaches = tuple(load_approaches(TEST_CAD_FILE))

    # Only needed to link together these objects.
    NEODatabase(neos, approaches)

    return approaches[:n]


@contextlib.contextmanager
def UncloseableStringIO(value=''):
    """A context manager for an uncloseable `io.StringIO`.

    This produces an almost-normal `io.StringIO`, except the `close` method has
    been patched out with a no-op. The context manager takes care of restoring
    the monkeypatch and closing the buffer, but this prevents other nested
    context managers (such as `open` from the implementation of `write_to_*`)
    from preemptively closing the `StringIO` before we can rewind it and read
    its value.
    """
    buf = io.StringIO(value)
    buf._close = buf.close
    buf.close = lambda: False
    yield buf
    buf.close = buf._close
    delattr(buf, '_close')
    buf.close()


class TestWriteToCSV(unittest.TestCase):
    @classmethod
    @unittest.mock.patch('write.open')
    def setUpClass(cls, mock_file):
        results = build_results(5)

        with UncloseableStringIO() as buf:
            mock_file.return_value = buf
            try:
                write_to_csv(results, None)
            except csv.Error as err:
                raise cls.failureException("Unable to write results to CSV.") from err
            except ValueError as err:
                raise cls.failureException("Unexpected failure while writing to CSV.") from err
            else:
                # Rewind the unclosed buffer to save its contents.
                buf.seek(0)
                cls.value = buf.getvalue()

    def test_csv_data_is_well_formed(self):
        # Now, we have the value in memory, and can _actually_ start testing.
        buf = io.StringIO(self.value)

        # Check that the output is well-formed.
        try:
            # Consume the output and immediately discard it.
            collections.deque(csv.DictReader(buf), maxlen=0)
        except csv.Error as err:
            raise self.failureException("write_to_csv produced an invalid CSV format.") from err

    def test_csv_data_has_header(self):
        try:
            self.assertTrue(csv.Sniffer().has_header(self.value))
            return
        except csv.Error as err:
            raise self.failureException("Unable to sniff for headers.") from err


    def test_csv_data_has_five_rows(self):
        # Now, we have the value in memory, and can _actually_ start testing.
        buf = io.StringIO(self.value)

        # Check that the output is well-formed.
        try:
            reader = csv.DictReader(buf)
            rows = tuple(reader)
        except csv.Error as err:
            raise self.failureException("write_to_csv produced an invalid CSV format.") from err

        self.assertEqual(len(rows), 5)

    def test_csv_data_header_matches_requirements(self):
        # Now, we have the value in memory, and can _actually_ start testing.
        buf = io.StringIO(self.value)

        # Check that the output is well-formed.
        try:
            reader = csv.DictReader(buf)
            rows = tuple(reader)
        except csv.Error as err:
            raise self.failureException("write_to_csv produced an invalid CSV format.") from err

        fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous')
        self.assertGreater(len(rows), 0)
        self.assertSetEqual(set(fieldnames), set(rows[0].keys()))


class TestWriteToJSON(unittest.TestCase):
    @classmethod
    @unittest.mock.patch('write.open')
    def setUpClass(cls, mock_file):
        results = build_results(5)

        with UncloseableStringIO() as buf:
            mock_file.return_value = buf
            try:
                write_to_json(results, None)
            except csv.Error as err:
                raise cls.failureException("Unable to write results to CSV.") from err
            except ValueError as err:
                raise cls.failureException("Unexpected failure while writing to CSV.") from err
            else:
                # Rewind the unclosed buffer to fetch the contents saved to "disk".
                buf.seek(0)
                cls.value = buf.getvalue()

    def test_json_data_is_well_formed(self):
        # Now, we have the value in memory, and can _actually_ start testing.
        buf = io.StringIO(self.value)
        try:
            json.load(buf)
        except json.JSONDecodeError as err:
            raise self.failureException("write_to_json produced an invalid JSON document") from err

    def test_json_data_is_a_sequence(self):
        buf = io.StringIO(self.value)
        try:
            data = json.load(buf)
        except json.JSONDecodeError as err:
            raise self.failureException("write_to_json produced an invalid JSON document") from err
        self.assertIsInstance(data, collections.abc.Sequence)

    def test_json_data_has_five_elements(self):
        buf = io.StringIO(self.value)
        try:
            data = json.load(buf)
        except json.JSONDecodeError as err:
            raise self.failureException("write_to_json produced an invalid JSON document") from err
        self.assertEqual(len(data), 5)

    def test_json_element_is_associative(self):
        buf = io.StringIO(self.value)
        try:
            data = json.load(buf)
        except json.JSONDecodeError as err:
            raise self.failureException("write_to_json produced an invalid JSON document") from err

        approach = data[0]
        self.assertIsInstance(approach, collections.abc.Mapping)

    def test_json_element_has_nested_attributes(self):
        buf = io.StringIO(self.value)
        try:
            data = json.load(buf)
        except json.JSONDecodeError as err:
            raise self.failureException("write_to_json produced an invalid JSON document") from err

        approach = data[0]
        self.assertIn('datetime_utc', approach)
        self.assertIn('distance_au', approach)
        self.assertIn('velocity_km_s', approach)
        self.assertIn('neo', approach)
        neo = approach['neo']
        self.assertIn('designation', neo)
        self.assertIn('name', neo)
        self.assertIn('diameter_km', neo)
        self.assertIn('potentially_hazardous', neo)

    def test_json_element_decodes_to_correct_types(self):
        buf = io.StringIO(self.value)
        try:
            data = json.load(buf)
        except json.JSONDecodeError as err:
            raise self.failureException("write_to_json produced an invalid JSON document") from err

        approach = data[0]
        try:
            datetime.datetime.strptime(approach['datetime_utc'], '%Y-%m-%d %H:%M')
        except ValueError:
            self.fail("The `datetime_utc` key isn't in YYYY-MM-DD HH:MM` format.")
        self.assertIsInstance(approach['distance_au'], float)
        self.assertIsInstance(approach['velocity_km_s'], float)

        self.assertIsInstance(approach['neo']['designation'], str)
        self.assertNotEqual(approach['neo']['name'], 'None')
        if approach['neo']['name']:
            self.assertIsInstance(approach['neo']['name'], str)
        self.assertIsInstance(approach['neo']['diameter_km'], float)
        self.assertIsInstance(approach['neo']['potentially_hazardous'], bool)


if __name__ == '__main__':
    unittest.main()
