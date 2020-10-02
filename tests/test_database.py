"""Check that an `NEODatabase` can be constructed and responds to inspect queries.

The `NEODatabase` constructor should cross-link NEOs and their close approaches,
as well as prepare any additional metadata needed to support the `get_neo_by_*`
methods.

To run these tests from the project root, run:

    $ python3 -m unittest --verbose tests.test_database

These tests should pass when Task 2 is complete.
"""
import pathlib
import math
import unittest


from extract import load_neos, load_approaches
from database import NEODatabase


# Paths to the test data files.
TESTS_ROOT = (pathlib.Path(__file__).parent).resolve()
TEST_NEO_FILE = TESTS_ROOT / 'test-neos-2020.csv'
TEST_CAD_FILE = TESTS_ROOT / 'test-cad-2020.json'


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.neos = load_neos(TEST_NEO_FILE)
        cls.approaches = load_approaches(TEST_CAD_FILE)
        cls.db = NEODatabase(cls.neos, cls.approaches)

    def test_database_construction_links_approaches_to_neos(self):
        for approach in self.approaches:
            self.assertIsNotNone(approach.neo)

    def test_database_construction_ensures_each_neo_has_an_approaches_attribute(self):
        for neo in self.neos:
            self.assertTrue(hasattr(neo, 'approaches'))

    def test_database_construction_ensures_neos_collectively_exhaust_approaches(self):
        approaches = set()
        for neo in self.neos:
            approaches.update(neo.approaches)
        self.assertEqual(approaches, set(self.approaches))

    def test_database_construction_ensures_neos_mutually_exclude_approaches(self):
        seen = set()
        for neo in self.neos:
            for approach in neo.approaches:
                if approach in seen:
                    self.fail(f"{approach} appears in the approaches of multiple NEOs.")
                seen.add(approach)

    def test_get_neo_by_designation(self):
        cerberus = self.db.get_neo_by_designation('1865')
        self.assertIsNotNone(cerberus)
        self.assertEqual(cerberus.designation, '1865')
        self.assertEqual(cerberus.name, 'Cerberus')
        self.assertEqual(cerberus.diameter, 1.2)
        self.assertEqual(cerberus.hazardous, False)

        adonis = self.db.get_neo_by_designation('2101')
        self.assertIsNotNone(adonis)
        self.assertEqual(adonis.designation, '2101')
        self.assertEqual(adonis.name, 'Adonis')
        self.assertEqual(adonis.diameter, 0.60)
        self.assertEqual(adonis.hazardous, True)

        tantalus = self.db.get_neo_by_designation('2102')
        self.assertIsNotNone(tantalus)
        self.assertEqual(tantalus.designation, '2102')
        self.assertEqual(tantalus.name, 'Tantalus')
        self.assertEqual(tantalus.diameter, 1.649)
        self.assertEqual(tantalus.hazardous, True)

    def test_get_neo_by_designation_neos_with_year(self):
        bs_2020 = self.db.get_neo_by_designation('2020 BS')
        self.assertIsNotNone(bs_2020)
        self.assertEqual(bs_2020.designation, '2020 BS')
        self.assertEqual(bs_2020.name, None)
        self.assertTrue(math.isnan(bs_2020.diameter))
        self.assertEqual(bs_2020.hazardous, False)

        py1_2020 = self.db.get_neo_by_designation('2020 PY1')
        self.assertIsNotNone(py1_2020)
        self.assertEqual(py1_2020.designation, '2020 PY1')
        self.assertEqual(py1_2020.name, None)
        self.assertTrue(math.isnan(py1_2020.diameter))
        self.assertEqual(py1_2020.hazardous, False)

    def test_get_neo_by_designation_missing(self):
        nonexistent = self.db.get_neo_by_designation('not-real-designation')
        self.assertIsNone(nonexistent)

    def test_get_neo_by_name(self):
        lemmon = self.db.get_neo_by_name('Lemmon')
        self.assertIsNotNone(lemmon)
        self.assertEqual(lemmon.designation, '2013 TL117')
        self.assertEqual(lemmon.name, 'Lemmon')
        self.assertTrue(math.isnan(lemmon.diameter))
        self.assertEqual(lemmon.hazardous, False)

        jormungandr = self.db.get_neo_by_name('Jormungandr')
        self.assertIsNotNone(jormungandr)
        self.assertEqual(jormungandr.designation, '471926')
        self.assertEqual(jormungandr.name, 'Jormungandr')
        self.assertTrue(math.isnan(jormungandr.diameter))
        self.assertEqual(jormungandr.hazardous, True)

    def test_get_neo_by_name_missing(self):
        nonexistent = self.db.get_neo_by_name('not-real-name')
        self.assertIsNone(nonexistent)


if __name__ == '__main__':
    unittest.main()
