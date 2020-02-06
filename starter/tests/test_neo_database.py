import pathlib
import unittest

from database import NEODatabase
from search import Query, NEOSearcher


PROJECT_ROOT = pathlib.Path(__file__).parent.parent


class TestNEOSearchUseCases(unittest.TestCase):
    """
    Test Class with test cases for covering the core search functionality
    in the README.md#Requirements cases:

    1.  Find up to some number of unique NEOs on a given date or between start date and end date.
    2.  Find up to some number of unique NEOs on a given date or between start date and end date larger than X kilometers.
    3.  Find up to some number of unique NEOs on a given date or between start date and end date larger than X kilometers
        that were hazardous.
    4.  Find up to some number of unique NEOs on a given date or between start date and end date larger than X kilometers
        that were hazardous and within X kilometers from Earth.

    Requirement one is tested in `test_find_unique_number_neos_on_date` and `test_find_unique_number_between_dates`
    Requirement two is tested in `test_find_unique_number_neos_on_date_with_diameter`
    and `test_find_unique_number_between_dates_with_diameter`
    Requirement three is tested in `test_find_unique_number_neos_on_date_with_diameter_and_hazardous` and
    `test_find_unique_number_neos_on_date_with_diameter_and_hazardous`
    Requirement four is tested in `test_find_unique_number_neos_on_date_with_diameter_and_hazardous_and_distance` and
    `test_find_unique_number_between_dates_with_diameter_and_hazardous_and_distance`
    """

    def setUp(self):
        self.neo_data_file = f'{PROJECT_ROOT}/data/neo_data.csv'

        self.db = NEODatabase(filename=self.neo_data_file)
        self.db.load_data()

        self.start_date = '2020-01-01'
        self.end_date = '2020-01-10'

    def test_find_unique_number_neos_on_date(self):
        self.db.load_data()
        query_selectors = Query(number=10, date=self.start_date, return_object='NEO').build_query()
        results = NEOSearcher(self.db).get_objects(query_selectors)

        # Confirm 10 results and 10 unique results
        self.assertEqual(len(results), 10)
        neo_ids = set(map(lambda neo: neo.name, results))
        self.assertEqual(len(neo_ids), 10)

    def test_find_unique_number_between_dates(self):
        self.db.load_data()
        query_selectors = Query(
            number=10, start_date=self.start_date, end_date=self.end_date, return_object='NEO'
        ).build_query()
        results = NEOSearcher(self.db).get_objects(query_selectors)

        # Confirm 10 results and 10 unique results
        self.assertEqual(len(results), 10)
        neo_ids = set(map(lambda neo: neo.name, results))
        self.assertEqual(len(neo_ids), 10)

    def test_find_unique_number_neos_on_date_with_diameter(self):
        self.db.load_data()
        query_selectors = Query(
            number=10, date=self.start_date, return_object='NEO', filter=["diameter:>:0.042"]
        ).build_query()
        results = NEOSearcher(self.db).get_objects(query_selectors)

        # Confirm 4 results and 4 unique results
        self.assertEqual(len(results), 4)
        neo_ids = list(filter(lambda neo: neo.diameter_min_km > 0.042, results))
        neo_ids = set(map(lambda neo: neo.name, results))
        self.assertEqual(len(neo_ids), 4)

    def test_find_unique_number_between_dates_with_diameter(self):
        self.db.load_data()
        query_selectors = Query(
            number=10, start_date=self.start_date, end_date=self.end_date,
            return_object='NEO', filter=["diameter:>:0.042"]
        ).build_query()
        results = NEOSearcher(self.db).get_objects(query_selectors)

        # Confirm 10 results and 10 unique results
        self.assertEqual(len(results), 10)
        neo_ids = list(filter(lambda neo: neo.diameter_min_km > 0.042, results))
        diameter = set(map(lambda neo: neo.diameter_min_km, results))
        neo_ids = set(map(lambda neo: neo.name, results))
        self.assertEqual(len(neo_ids), 10)

    def test_find_unique_number_neos_on_date_with_diameter_and_hazardous(self):
        self.db.load_data()
        query_selectors = Query(
            number=10, date=self.start_date, return_object='NEO', filter=["diameter:>:0.042", "is_hazardous:=:True"]
        ).build_query()
        results = NEOSearcher(self.db).get_objects(query_selectors)

        # Confirm 0 results and 0 unique results
        self.assertEqual(len(results), 0)
        neo_ids = list(filter(
            lambda neo: neo.diameter_min_km > 0.042 and neo.is_potentially_hazardous_asteroid, results
        ))
        neo_ids = set(map(lambda neo: neo.name, results))
        self.assertEqual(len(neo_ids), 0)

    def test_find_unique_number_between_dates_with_diameter_and_hazardous(self):
        self.db.load_data()
        query_selectors = Query(
            number=10, start_date=self.start_date, end_date=self.end_date,
            return_object='NEO', filter=["diameter:>:0.042", "is_hazardous:=:True"]
        ).build_query()
        results = NEOSearcher(self.db).get_objects(query_selectors)

        # Confirm 10 results and 10 unique results
        self.assertEqual(len(results), 10)
        neo_ids = list(filter(
            lambda neo: neo.diameter_min_km > 0.042 and neo.is_potentially_hazardous_asteroid, results)
        )
        neo_ids = set(map(lambda neo: neo.name, results))
        self.assertEqual(len(neo_ids), 10)

    def test_find_unique_number_neos_on_date_with_diameter_and_hazardous_and_distance(self):
        self.db.load_data()
        query_selectors = Query(
            number=10, date=self.start_date, return_object='NEO',
            filter=["diameter:>:0.042", "is_hazardous:=:True", "distance:>:234989"]
        ).build_query()
        results = NEOSearcher(self.db).get_objects(query_selectors)

        # Confirm 0 results and 0 unique results
        self.assertEqual(len(results), 0)
        neo_ids = list(filter(
            lambda neo: neo.diameter_min_km > 0.042 and neo.is_potentially_hazardous_asteroid, results
        ))
        neo_ids = set(map(lambda neo: neo.name, results))
        self.assertEqual(len(neo_ids), 0)

    def test_find_unique_number_between_dates_with_diameter_and_hazardous_and_distance(self):
        self.db.load_data()
        query_selectors = Query(
            number=10, start_date=self.start_date, end_date=self.end_date,
            return_object='NEO',
            filter=["diameter:>:0.042", "is_hazardous:=:True", "distance:>:234989"]
        ).build_query()
        results = NEOSearcher(self.db).get_objects(query_selectors)

        # Confirm 4 results and 4 unique results
        self.assertEqual(len(results), 10)

        # Filter NEOs by NEO attributes
        neo_ids = list(filter(
            lambda neo: neo.diameter_min_km > 0.042 and neo.is_potentially_hazardous_asteroid, results)
        )

        # Filter to NEO Orbit Paths with Matching Distance
        all_orbits = []
        for neo in neo_ids:
            all_orbits += neo.orbits
        unique_orbits = set()
        filtered_orbits = []
        for orbit in all_orbits:
            date_name = f'{orbit.close_approach_date}.{orbit.neo_name}'
            if date_name not in unique_orbits:
                if orbit.miss_distance_kilometers > 234989.0:
                    filtered_orbits.append(orbit)

        # Grab the requested number
        orbits = filtered_orbits[0:10]
        self.assertEqual(len(orbits), 10)


if __name__ == '__main__':
    unittest.main()