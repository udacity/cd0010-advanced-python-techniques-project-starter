from models import OrbitPath, NearEarthObject
import pandas as pd


class NEODatabase(object):
    """
    Object to hold Near Earth Objects and their orbits.

    To support optimized date searching, a dict mapping of all orbit date paths to the Near Earth Objects
    recorded on a given day is maintained. Additionally, all unique instances of a Near Earth Object
    are contained in a dict mapping the Near Earth Object name to the NearEarthObject instance.
    """

    def __init__(self, filename):
        """
        :param filename: str representing the pathway of the filename containing the Near Earth Object data
        """
        # TODO: What data structures will be needed to store the NearEarthObjects and OrbitPaths?
        # TODO: Add relevant instance variables for this.
        self.filename = filename
        self.neo_dict = {}      #by id
        self.orbit_dict = {}        #by date


    def load_data(self, filename=None):
        """
        Loads data from a .csv file, instantiating Near Earth Objects and their OrbitPaths by:
           - Storing a dict of orbit date to list of NearEarthObject instances
           - Storing a dict of the Near Earth Object name to the single instance of NearEarthObject

        :param filename:
        :return:
        """

        if not (filename or self.filename):
            raise Exception('Cannot load data, no filename provided')

        filename = filename or self.filename

        # Load data from csv file.
        df = pd.read_csv(filename)
        # Where will the data be stored?
        dict_list = df.to_dict(orient="records")
        for item in dict_list: 
            if item['close_approach_date_full'] not in self.orbit_dict:
                self.orbit_dict[item['close_approach_date_full']] = {}
            if item['kilometers_per_second']+item['miss_distance_kilometers'] not in self.orbit_dict[item['close_approach_date_full']]:
                self.orbit_dict[item['close_approach_date_full']][item['kilometers_per_second']+item['miss_distance_kilometers']] = OrbitPath(**item)
            current_orbit = self.orbit_dict[item['close_approach_date_full']][item['kilometers_per_second']+item['miss_distance_kilometers']]

            if item['id'] not in self.neo_dict:
                self.neo_dict[item['id']] = NearEarthObject(**item)
            self.neo_dict[item['id']].update_orbits(current_orbit)
        return None