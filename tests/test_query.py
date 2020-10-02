"""Check that `query`ing an `NEODatabase` accurately produces close approaches.

There are a plethora of ways to combine the arguments to `create_filters`, which
correspond to different command-line options. This modules tests the options in
isolation, in pairs, and in more complicated combinations. Althought the tests
are not entirely exhaustive, any implementation that passes all of these tests
is most likely up to snuff.

To run these tests from the project root, run::

    $ python3 -m unittest --verbose tests.test_query

These tests should pass when Tasks 3a and 3b are complete.
"""
import datetime
import pathlib
import unittest

from database import NEODatabase
from extract import load_neos, load_approaches
from filters import create_filters


TESTS_ROOT = (pathlib.Path(__file__).parent).resolve()
TEST_NEO_FILE = TESTS_ROOT / 'test-neos-2020.csv'
TEST_CAD_FILE = TESTS_ROOT / 'test-cad-2020.json'


class TestQuery(unittest.TestCase):
    # Set longMessage to True to enable lengthy diffs between set comparisons.
    longMessage = False

    @classmethod
    def setUpClass(cls):
        cls.neos = load_neos(TEST_NEO_FILE)
        cls.approaches = load_approaches(TEST_CAD_FILE)
        cls.db = NEODatabase(cls.neos, cls.approaches)

    def test_query_all(self):
        expected = set(self.approaches)
        self.assertGreater(len(expected), 0)

        filters = create_filters()
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    ###############################################
    # Single filters and pairs of related filters #
    ###############################################

    def test_query_approaches_on_march_2(self):
        date = datetime.date(2020, 3, 2)

        expected = set(
            approach for approach in self.approaches
            if approach.time.date() == date
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(date=date)
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_approaches_after_april(self):
        start_date = datetime.date(2020, 4, 1)

        expected = set(
            approach for approach in self.approaches
            if start_date <= approach.time.date()
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(start_date=start_date)
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_approaches_before_july(self):
        end_date = datetime.date(2020, 6, 30)

        expected = set(
            approach for approach in self.approaches
            if approach.time.date() <= end_date
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(end_date=end_date)
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_approaches_in_march(self):
        start_date = datetime.date(2020, 3, 1)
        end_date = datetime.date(2020, 3, 31)

        expected = set(
            approach for approach in self.approaches
            if start_date <= approach.time.date() <= end_date
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(start_date=start_date, end_date=end_date)
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_conflicting_date_bounds(self):
        start_date = datetime.date(2020, 10, 1)
        end_date = datetime.date(2020, 4, 1)

        expected = set()

        filters = create_filters(start_date=start_date, end_date=end_date)
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_bounds_and_a_specific_date(self):
        start_date = datetime.date(2020, 2, 1)
        date = datetime.date(2020, 3, 2)
        end_date = datetime.date(2020, 4, 1)

        expected = set(
            approach for approach in self.approaches
            if approach.time.date() == date
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(date=date, start_date=start_date, end_date=end_date)
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_max_distance(self):
        distance_max = 0.4

        expected = set(
            approach for approach in self.approaches
            if approach.distance <= distance_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(distance_max=distance_max)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_min_distance(self):
        distance_min = 0.1

        expected = set(
            approach for approach in self.approaches
            if distance_min <= approach.distance
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(distance_min=distance_min)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_max_distance_and_min_distance(self):
        distance_max = 0.4
        distance_min = 0.1

        expected = set(
            approach for approach in self.approaches
            if distance_min <= approach.distance <= distance_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(distance_min=distance_min, distance_max=distance_max)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_max_distance_and_min_distance_conflicting(self):
        distance_max = 0.1
        distance_min = 0.4

        expected = set()

        filters = create_filters(distance_min=distance_min, distance_max=distance_max)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_max_velocity(self):
        velocity_max = 20

        expected = set(
            approach for approach in self.approaches
            if approach.velocity <= velocity_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(velocity_max=velocity_max)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_min_velocity(self):
        velocity_min = 10

        expected = set(
            approach for approach in self.approaches
            if velocity_min <= approach.velocity
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(velocity_min=velocity_min)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_max_velocity_and_min_velocity(self):
        velocity_max = 20
        velocity_min = 10

        expected = set(
            approach for approach in self.approaches
            if velocity_min <= approach.velocity <= velocity_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(velocity_min=velocity_min, velocity_max=velocity_max)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_max_velocity_and_min_velocity_conflicting(self):
        velocity_max = 10
        velocity_min = 20

        expected = set()

        filters = create_filters(velocity_min=velocity_min, velocity_max=velocity_max)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_max_diameter(self):
        diameter_max = 1.5

        expected = set(
            approach for approach in self.approaches
            if approach.neo.diameter <= diameter_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(diameter_max=diameter_max)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_min_diameter(self):
        diameter_min = 0.5

        expected = set(
            approach for approach in self.approaches
            if diameter_min <= approach.neo.diameter
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(diameter_min=diameter_min)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_max_diameter_and_min_diameter(self):
        diameter_max = 1.5
        diameter_min = 0.5

        expected = set(
            approach for approach in self.approaches
            if diameter_min <= approach.neo.diameter <= diameter_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(diameter_min=diameter_min, diameter_max=diameter_max)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_max_diameter_and_min_diameter_conflicting(self):
        diameter_max = 0.5
        diameter_min = 1.5

        expected = set()

        filters = create_filters(diameter_min=diameter_min, diameter_max=diameter_max)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_hazardous(self):
        expected = set(
            approach for approach in self.approaches
            if approach.neo.hazardous
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(hazardous=True)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_with_not_hazardous(self):
        expected = set(
            approach for approach in self.approaches
            if not approach.neo.hazardous
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(hazardous=False)
        received = set(self.db.query(filters))

        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    ###########################
    # Combinations of filters #
    ###########################

    def test_query_approaches_on_march_2_with_max_distance(self):
        date = datetime.date(2020, 3, 2)
        distance_max = 0.4

        expected = set(
            approach for approach in self.approaches
            if approach.time.date() == date
            and approach.distance <= distance_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(date=date, distance_max=distance_max)
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_approaches_on_march_2_with_min_distance(self):
        date = datetime.date(2020, 3, 2)
        distance_min = 0.1

        expected = set(
            approach for approach in self.approaches
            if approach.time.date() == date
            and distance_min <= approach.distance
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(date=date, distance_min=distance_min)
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_approaches_in_march_with_min_distance_and_max_distance(self):
        start_date = datetime.date(2020, 3, 1)
        end_date = datetime.date(2020, 3, 31)
        distance_max = 0.4
        distance_min = 0.1

        expected = set(
            approach for approach in self.approaches
            if start_date <= approach.time.date() <= end_date
            and distance_min <= approach.distance <= distance_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(
            start_date=start_date, end_date=end_date,
            distance_min=distance_min, distance_max=distance_max,
        )
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_approaches_in_march_with_distance_bounds_and_max_velocity(self):
        start_date = datetime.date(2020, 3, 1)
        end_date = datetime.date(2020, 3, 31)
        distance_max = 0.4
        distance_min = 0.1
        velocity_max = 20

        expected = set(
            approach for approach in self.approaches
            if start_date <= approach.time.date() <= end_date
            and distance_min <= approach.distance <= distance_max
            and approach.velocity <= velocity_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(
            start_date=start_date, end_date=end_date,
            distance_min=distance_min, distance_max=distance_max,
            velocity_max=velocity_max
        )
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_approaches_in_march_with_distance_and_velocity_bounds(self):
        start_date = datetime.date(2020, 3, 1)
        end_date = datetime.date(2020, 3, 31)
        distance_max = 0.4
        distance_min = 0.1
        velocity_max = 20
        velocity_min = 10

        expected = set(
            approach for approach in self.approaches
            if start_date <= approach.time.date() <= end_date
            and distance_min <= approach.distance <= distance_max
            and velocity_min <= approach.velocity <= velocity_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(
            start_date=start_date, end_date=end_date,
            distance_min=distance_min, distance_max=distance_max,
            velocity_min=velocity_min, velocity_max=velocity_max
        )
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_approaches_in_spring_with_distance_and_velocity_bounds_and_max_diameter(self):
        start_date = datetime.date(2020, 3, 1)
        end_date = datetime.date(2020, 5, 31)
        distance_max = 0.5
        distance_min = 0.05
        velocity_max = 25
        velocity_min = 5
        diameter_max = 1.5

        expected = set(
            approach for approach in self.approaches
            if start_date <= approach.time.date() <= end_date
            and distance_min <= approach.distance <= distance_max
            and velocity_min <= approach.velocity <= velocity_max
            and approach.neo.diameter <= diameter_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(
            start_date=start_date, end_date=end_date,
            distance_min=distance_min, distance_max=distance_max,
            velocity_min=velocity_min, velocity_max=velocity_max,
            diameter_max=diameter_max
        )
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_approaches_in_spring_with_distance_velocity_and_diameter_bounds(self):
        start_date = datetime.date(2020, 3, 1)
        end_date = datetime.date(2020, 5, 31)
        distance_max = 0.5
        distance_min = 0.05
        velocity_max = 25
        velocity_min = 5
        diameter_max = 1.5
        diameter_min = 0.5

        expected = set(
            approach for approach in self.approaches
            if start_date <= approach.time.date() <= end_date
            and distance_min <= approach.distance <= distance_max
            and velocity_min <= approach.velocity <= velocity_max
            and diameter_min <= approach.neo.diameter <= diameter_max
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(
            start_date=start_date, end_date=end_date,
            distance_min=distance_min, distance_max=distance_max,
            velocity_min=velocity_min, velocity_max=velocity_max,
            diameter_min=diameter_min, diameter_max=diameter_max
        )
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_approaches_in_spring_with_all_bounds_and_potentially_hazardous_neos(self):
        start_date = datetime.date(2020, 3, 1)
        end_date = datetime.date(2020, 5, 31)
        distance_max = 0.5
        distance_min = 0.05
        velocity_max = 25
        velocity_min = 5
        diameter_max = 1.5
        diameter_min = 0.5

        expected = set(
            approach for approach in self.approaches
            if start_date <= approach.time.date() <= end_date
            and distance_min <= approach.distance <= distance_max
            and velocity_min <= approach.velocity <= velocity_max
            and diameter_min <= approach.neo.diameter <= diameter_max
            and approach.neo.hazardous
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(
            start_date=start_date, end_date=end_date,
            distance_min=distance_min, distance_max=distance_max,
            velocity_min=velocity_min, velocity_max=velocity_max,
            diameter_min=diameter_min, diameter_max=diameter_max,
            hazardous=True
        )
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")

    def test_query_approaches_in_spring_with_all_bounds_and_not_potentially_hazardous_neos(self):
        start_date = datetime.date(2020, 3, 1)
        end_date = datetime.date(2020, 5, 31)
        distance_max = 0.5
        distance_min = 0.05
        velocity_max = 25
        velocity_min = 5
        diameter_max = 1.5
        diameter_min = 0.5

        expected = set(
            approach for approach in self.approaches
            if start_date <= approach.time.date() <= end_date
            and distance_min <= approach.distance <= distance_max
            and velocity_min <= approach.velocity <= velocity_max
            and diameter_min <= approach.neo.diameter <= diameter_max
            and not approach.neo.hazardous
        )
        self.assertGreater(len(expected), 0)

        filters = create_filters(
            start_date=start_date, end_date=end_date,
            distance_min=distance_min, distance_max=distance_max,
            velocity_min=velocity_min, velocity_max=velocity_max,
            diameter_min=diameter_min, diameter_max=diameter_max,
            hazardous=False
        )
        received = set(self.db.query(filters))
        self.assertEqual(expected, received, msg="Computed results do not match expected results.")


if __name__ == '__main__':
    unittest.main()
