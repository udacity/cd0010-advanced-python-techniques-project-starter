# Near Earth Object Database

The Near Earth Object database is a searchable Python 3 command-line interface (CLI) project.

# Install

A Python 3.6+ project, no external dependencies are required as all libraries used are a part of the Python standard library.

If you have multiple versions of Python installed on your machine, please be mindful [to set up a virtual environment with Python 3.6+](https://docs.python.org/3/library/venv.html).

## To Setup a Python 3  Virtual  Environment

```python3 -m venv /path/to/new/virtual/environment```

# Usage

To use the project:

1. Clone the project to your local machine
2. Create a virtual environment, named `env`, with `python3 -m env /env` in project root
3. Activate the virtual environment with `source env/bin/activate`
4. Navigate to the `/starter` directory
5. Run `python main.py -h` or `./main.py -h` for an explanation of how to run the project
6. Or try it out yourself!

Example of how to use the interface:

1. Find up to 10 NEOs on Jan 1, 2020 displaying output to terminal

`./main.py display -n 10 --date 2020-01-01`

2. Find up to 10 NEOs from input file 'new_neo_data.csv' between Jan 1, 2020 and Jan 10, 2020 within 5 km from Earth,
exporting to a csv file

`./main.py csvfile -n 10 -f new_neo_data.csv --start_date 2020-01-01 --end_date 2020-01-10 --filter distance:>=:5`

## Requirements

The Near Earth Object Database you are creating is a searchable database that, given a csv file of Near Earth Objects data, can perform
data searches. All data results should be able to be displayed to the terminal or output to a csv file.

Search Requirements:

   1.  Find up to some number of unique NEOs on a given date or between start date and end date.
   2.  Find up to some number of unique NEOs on a given date or between start date and end date larger than X kilometers.
   3.  Find up to some number of unique NEOs on a given date or between start date and end date larger than X kilometers
       that were hazardous.
   4.  Find up to some number of unique NEOs on a given date or between start date and end date larger than X kilometers
       that were hazardous and within X kilometers from Earth.

To achieve this functionality the project should include Python objects that represent:
- Near Earth Objects
- Orbit Paths
- A container object for the Near Earth Objects and Orbit Paths
- An object to perform the data search on the container
- An object to write the output format of the search results

## Near Earth Object Data

Each row in the `neo_data.csv` represents a single orbit path for a Near Earth Object on a given date.

<details>
 <summary> Each row includes the following attributes: </summary>

```
- id: unique id of the NEO 
- neo_reference_id: NEO reference id 
- name: NEO name 
- nasa_jpl_url: url with NASA info on the NEO 
- absolute_magnitude_h: height of NEO 
- estimated_diameter_min_kilometers: diameter in km min 
- estimated_diameter_max_kilometers: diameter in km max 
- estimated_diameter_min_meters: diameter in m min  
- estimated_diameter_max_meters: diameter in m max  
- estimated_diameter_min_miles: diameter in mi min  
- estimated_diameter_max_miles: diameter in mi max  
- estimated_diameter_min_feet: diameter in ft min  
- estimated_diameter_max_feet: diameter in ft max  
- is_potentially_hazardous_asteroid: true/false if hazaradous  
- kilometers_per_second: km pr s 
- kilometers_per_hour: km per hr 
- miles_per_hour: mi per hr 
- close_approach_date: str of NEO orbit close approach date 
- close_approach_date_full: : str of NEO orbit close approach date 
- miss_distance_astronomical: : how far NEO miss in astronomical units 
- miss_distance_lunar: how far NEO miss in lunar units  
- miss_distance_kilometers: how far NEO miss in km 
- miss_distance_miles: how far NEO miss in mi 
- orbiting_body: body orbiting around 
```

</details>

## Project Organization

The project is broken into the following files:

- `main.py`: Python main script to run the project. **This is the completed file that provides the command-line interface. You will not need to modify this file.**
- `database.py`: Python module with database logic (e.g. reading the data, storing the data)
- `exceptions.py`: Python module with any custom exceptions logic
- `models.py` Python module with models -- objects representing `NearEarthObject` and `OrbitPath`
- `search.py`: Python module with search logic (e.g. the different date searchers)
- `writer.py`: Python module with write logic (e.g. write to file, print to terminal)

The project additionally has prewritten tests that will be used to help you during the completion of task three (defined below):

- `tests/test_neo_database.py`: Python unittest module with 8 tests, each requirement has 2 tests.

## Tasks to Complete

You **must** complete the search requirements in order. You will be asked for certain documentation after you complete each search task, so **do not** skip to search requirement 4. Starting with **search requirement 1**, *Find up to some number of NEOs on a given date or between start date and end date. *, complete the following tasks.

To run your implementation, you can run `main.py` which has been provided to you. Examples of how to run it are below:

```
# For running an example of requirement 1: find a unique number of NEOs on a date that will be displayed to stdout

./main.py display -n 10 --date 2020-01-01

# For running an example of requirement 2: find a unique number of NEOs between dates that are not hazardous. Results will be output to a csv.

./main.py csv_file -n 10 --start_date 2020-01-01 --end_date 2020-01-10 --filter "is_hazardous:=:False"

# For running an example of requirement 3: find a unique number of NEOs between dates that are not hazardous, have a diameter greater than 0.02 units. Results will be output to a csv.

./main.py csv_file -n 10 --start_date 2020-01-01 --end_date 2020-01-10 --filter "is_hazardous:=:False" "diameter:>:0.02"

# For running an example of requirement 4: find a unique number of NEOs between dates that are not hazardous, have a diameter greater than 0.02 units, that were more than 50000 units away. Results will be output to a csv.

./main.py csv_file -n 10 --start_date 2020-01-01 --end_date 2020-01-10 --filter "is_hazardous:=:False" "diameter:>:0.02" "distance:>=:50000"
```

You don't need to write code that asks the user for input, `main.py` will accept arguments from the user and pass them to the appropriate Python objects you will create. As you properly implement the tasks below, another step in main.py will execute without error.

Please look at `main.py` to gain an understanding of how it works; you will not need to edit this file. This contains the command-line interface and is already completed.

### Task 0: Debugging and Error Fixes

As you implement your program, you will run into bugs or errors in your code. At some point in your program, you must provide a Git commit which includes a new markdown or .txt file with an explanation of a bug solved, the tools used to resolve the bug, and please provide a link to the source code where the bug was located to help explain what bug arose and how you solved it.

### Task 1: Design your objects

In this task we will want to create our models, to be stored in `models.py` for:
- NearEarthObject
- OrbitalPath

To do this you will need to:

1. Determine what data is needed to represent each object by reviewing the data in `data/neo_data.csv`.
2. Determine how the objects will interact with one another.
  - Will the object(s) have a reference to one another?
  - If so, how?
3. Write the models.
  - Each Near Earth Object must know about each of its orbit paths from the data provided (e.g. If a NEO orbited Earth three times, it should know each of those dates).
  - Each Near Earth Object should have information that defines what the Near Earth Object is (this may change based on the search requirement you are implementing).
 - Each Orbit Path Object should have information that defines what the Orbit Path Object is (this may change based on the search requirement you are implementing).
  - All Near Earth Objects and Orbit Paths should be able to print relevant information about itself.
  - **Note:** you may change these implementations as you progress through the project.
4. Make sure to manually test your implementations.

### Task 2: Load your objects

Great! Now that you have defined the base objects in your `models.py`, let's do the data loading!

In this task, we will want to create our database, to be stored in `database.py`. You will be loading your objects into a `NEODatabase` object in `database.py`.

To do this you need to:

1. Write a `NEODatabase` object with a `load_data` function that reads from a `data/neo_data.csv`.
  - In `main.py`, the file location of "neo_data.csv" is passed directly into your `NEODatabase` object as a String.
2. Determine how, when the function `database.load_data()` is called, the `Database` object will store the relevant data for search requirement 1.
  - Your database should not just store raw data, it should also store objects you have created. You will load data into your Near Earth or Orbit Path objects and then store instances of those objects in your `Database` object.
  - What Python data structure(s) will you use to implement your database and store your `NearEarthObject` and `OrbitPath` instances?
  - Your database should include only one unique instance of each `NearEarthObject`.
  - Make sure you write functions to retrieve information from your database as well.
  - **Note:** you may change this implementation as you progress through the project.
3. Make sure to manually test your implementations.

### Task 3: Implement Search

You're making some real progress! Now that we can read the data, create `NearEarthObject` and `OrbitPath` instances, and store them in the `Database`, we need to provide an ability to search data!

In this task, we will write this logic in a `NEOSearcher` object in `search.py`.

Defined above are the four search use cases ([requirements](https://github.com/udacity/nd303-c1-advanced-python-techniques-project-starter/blob/master/starter/README.md#requirements))
you will eventually need to provide. To start, write a `NEOSearcher` object that can `get_objects` based on the first search requirement.

1. Begin implementing your `NEOSearcher` object.
  - In `main.py` an instance of your `NEODatabase` object is passed directly into your `NEOSearch` object.
  - The`get_objects` instance method should accept a `Query` object and return a list of NEOs that meet the requirements you read from your `Query` object.

2. Design your `Query` object in `search.py` with the parameters and filters it needs for each search requirement.
  - In `main.py`, the arguments passed in through the command line are passed directly to a Query object. They are passed in as a dictionary of parameters (i.e. "number" is a key in the parameter dictionary with the associated parameter/value being an int which represents the number of objects to find).
  - What parameters are needed to support search for requirement one?
  - The query object will store all of the parameters given by a user (e.g what type of date search is the query?)

3. Finish implementing your `NEOSearcher` object.
  - Your `NEOSearcher` will read the search parameters from the `Query` object it accepts as a parameter.
  - Your `NEOSearcher` object should not be parsing user input from the command line.

Try running your tests from the root of your project with: `python -m unittest discover`! Does your code pass the first two test cases in `tests/test_neo_database.py`? Great! If not, what is not passing? Read the error. Remember, you won't need to change this test file.

As you solve each requirement and pass the accompanying tests (specified in the definiton of `TestNEOSearchUseCases`), create a Git commit detailing:
   - The requirement number you solved
   - Why you chose the strategy you did
   - The data structures you used to implement that search case and why

Now, let's go to the second functionality requirement. Specifically what changes? **Reminder:** You must work through all of the requirements in order, gradually expanding your implementation. **You should update your implementations**, not have four different versions of every object to implement all of the search cases. Your final code must be able to fulfill all of the search requirements.

4. Starting with requirement two, you will need to start filtering your search results based on additional user input. You will need to design a `Filter` object in `search.py`.
  - The `Filter` object will transform user input into an object representing optional filter options that may be used to search for NEOs.
 - You will use your `Filter` object as a tool inside of your `Query` object to parse the optional filter options that may be used to search for NEOs.
  - You will likely use the `Operators` library to implement the filter operation (e.g. [operator.eq is a function that allows you to find an object with a specific value](https://docs.python.org/3/library/operator.html)).

As you implement search, some tips to consider:
- You may want to change how you store your data in the `Database`.
- You may want to add functionality to `NearEarthObject` and `OrbitPath`.

Continue to develop and test until you reach the final requirement, requirement four. This requirement asks you to consider
information about the distance the `NearEarthObject` is from the orbiting body during its `OrbitalPath`.

What changes? Do we still want to return only data on the `NearEarthObject` itself or the `OrbitPath`? How can we quickly access all the information we need for this search requirement?

### Task 4: Output the results

You've got results! How are we going to output them to the user? We've got two display formats to support: print to the terminal and output to a csv file.

In this task, you will need to create a `NEOWriter` in your `writper.py` that can `write` those output formats.

1. Create a `NEOWriter` object.
  - Add a `write` instance method that accepts two parameters:
    -  one parameter specifying the output format (terminal or csv). Receiving the String `"display"` will designate the method should print to terminal and receiving the String `"csvfile"` will designate the method should ouput to a csv file.
    - one parameter that will be a list of NEO or Orbital Paths to output.    
 - The `write` instance method should be able to print in a human-readable format to the terminal and output properly-formatted text to a csv file
  - Your `NearEarthObject` should always output their id, name, orbits, and orbit dates, and your`OrbitPath` should output name, miss distance in km, and orbit date.
  - Your `NEOWriter` must always print something, regardless of the size of the data to print.
  - In `main.py`, the script will call the `write` method to output your results in the format specified by the command line.

Hint: What can you use from your `NearEarthObject` and `OrbitPath` to customize the printed representation of those objects?
