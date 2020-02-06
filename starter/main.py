#!/usr/bin/env python
#  -*- coding: utf-8 -*-

"""
Script to run the Near Earth Object database.

You can run from the commandline with: main.py [args]
Example: main.py display -n 10 -d 2020-01-10

Search options:
- Find N NEOs by date e.g. main.py display --return NEO -n 10 -d 2020-01-10
- Find N NEOs between start_date and end_date  e.g. main.py display --return NEO -n 10 --start_date 2020-01-01 --end_date 2020-01-10
- Find N NEOs between start_date and end_date with filters and output to csvfile with name 'neo_neo_data' e.g. csvfile -n 10 -f new_neo_data --start_date 2020-01-01 --end_date 2020-01-10 --filter "is_hazardous:=:False" "diameter:>:0.02" "distance:>=:50000

Output options: Required.
- display: prints to stdout
- csv_file: exports data to a csv

Filters options: Optional. Input as: option:operation:value e.g. diameter:>=:0.042
- is_hazardous:[=]:bool
- diameter:[>=|=|<=]:float
- distance:[>=|=|<=]:float

Return objects options: Optional, defaults to NEO if not specified.
- NEO
- Path

Filename: Optional, used for specifying a filename for a csv to load data from. By default project looks for a csv in: data/neo_data.csv.
"""

import argparse
import pathlib
import sys
from datetime import datetime

from exceptions import UnsupportedFeature
from database import NEODatabase
from search import Query, NEOSearcher
from writer import OutputFormat, NEOWriter

PROJECT_ROOT = pathlib.Path(__file__).parent.absolute()


def verify_date(datetime_str):
    """
    Function that verifies datetime strings in YYYY-MM-DD format are valid dates.

    :param datetime_str:    String representing datetime in %Y-%m-%d format
    :return: str:           String representing datetime in %Y-%m-%d format
    """
    try:
        date_time_obj = datetime.strptime(datetime_str, "%Y-%m-%d")
        return datetime_str
    except ValueError:
        error_message = f'Not a valid date: "{datetime_str}"'
        raise argparse.ArgumentTypeError(error_message)


def verify_output_choice(choice):
    """
    Function that verifies output choice is a supported OutputFormat.

    :param choice:    String representing an OutputFormat
    :return: str:     String representing an OutputFormat
    """
    options = OutputFormat.list()

    if choice not in options:
        error_message = f'Not a valid output option: "{choice}"'
        raise argparse.ArgumentTypeError(error_message)

    return options[options.index(choice)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Near Earth Objects (NEOs) Database')
    parser.add_argument('output', choices=OutputFormat.list(), type=verify_output_choice,
                        help='Select option for how to output the search results.')
    parser.add_argument('-r', '--return_object', choices=['NEO', 'Path'],
                        default='NEO', type=str,
                        help='Select entity data to return.')
    parser.add_argument('-d', '--date', type=verify_date, help='YYYY-MM-DD format to find NEOs on the given date')
    parser.add_argument('-s', '--start_date', type=verify_date,
                        help='YYYY-MM-DD format to find NEOs on the provided start date')
    parser.add_argument('-e', '--end_date', type=verify_date,
                        help='YYYY-MM-DD format to find NEOs up to the end date')
    parser.add_argument('-n', '--number', type=int, help='Int representing max number of NEOs to return')
    parser.add_argument('-f', '--filename', type=str, help='Name of input csv data file')
    parser.add_argument('--filter', nargs='+', help='Select filter options with filter value: '
                                                    'is_hazardous:[=]:bool, '
                                                    'diameter:[>=|=|<=]:float, '
                                                    'distance:[>=|=|<=]:float.'
                                                    'Input as: [option:operation:value] '
                                                    'e.g. diameter:>=:0.042')

    args = parser.parse_args()
    var_args = vars(args)

    # Load Data
    if args.filename:
        filename = args.filename
    else:
        filename = f'{PROJECT_ROOT}/data/neo_data.csv'

    db = NEODatabase(filename=filename)

    try:
        db.load_data()
    except FileNotFoundError as e:
        print(f'File {var_args.get("filename")} not found, please try another file name.')
        sys.exit()
    except Exception as e:
        print(Exception)
        sys.exit()

    # Build Query
    query_selectors = Query(**var_args).build_query()

    # Get Results
    try:
        results = NEOSearcher(db).get_objects(query_selectors)
    except UnsupportedFeature as e:
        print('Unsupported Feature; Write unsuccessful')
        sys.exit()

    # Output Results
    try:
        result = NEOWriter().write(
            data=results,
            format=args.output,
        )
    except Exception as e:
        print(e)
        print('Write unsuccessful')
        sys.exit()

    if result:
        print('Write successful.')
    else:
        print('Write unsuccessful.')

