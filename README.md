# Explore Close Approaches of Near-Earth Objects

In this project, you'll use Python - and the skills we've developed throughout this course - to search for and explore close approaches of near-Earth objects (NEOs), using data from NASA/JPL's Center for Near Earth Object Studies.

## Overview

At a high-level, you'll create Python code that implements a command-line tool to inspect and query a dataset of NEOs and their close approaches to Earth.

Concretely, you'll have to read data from both a CSV file and a JSON file, convert that data into structured Python objects, perform filtering operations on the data, limit the size of the result set, and write the results to a file in a structured format, such as CSV or JSON.

When complete, you'll be able to inspect the properties of the near-Earth objects in the data set and query the data set of close approaches to Earth using any combination of the following filters:

- Occurs on a given date.
- Occurs on or after a given start date.
- Occurs on or before a given end date.
- Approaches Earth at a distance of at least (or at most) X astronomical units.
- Approaches Earth at a relative velocity of at least (or at most) Y kilometers per second.
- Has a diameter that is at least as large as (or at least as small as) Z kilometers.
- Is marked by NASA as potentially hazardous (or not).

### Learning Objectives

By completing this project, you'll have demonstrated an ability to:

- Represent structured data in Python.
- Extract data from structured files into Python.
- Transform the data within Python according to some desired behavior.
- Save the results in a structured way to a file.

Along the way, you'll have to be able to:

- Write Python functions to transform data and perform algorithms.
- Design Python classes to encapsulate useful data types.
- Provide interface abstractions for complex implementations.

It's normal to encounter bugs along the way, so in all likelihood, you'll also gain practice with valuable debugging skills, whether interpreting stack traces, chasing down system errors, handling and raising appropriate errors, walking through code with `pdb`, checking preconditions with `assert`, or simply displaying internal state with `print`.

## Understanding the Near-Earth Object Close Approach Datasets

This project contains two important data sets, and our first step will be to explore and understand the data containing within these structured files.

One dataset (`neos.csv`) contains information about semantic, physical, orbital, and model parameters for certain small bodies (asteroids and comets, mostly) in our solar system. The other dataset (`cad.json`) contains information about NEO close approaches - moments in time when the orbit of an astronomical body brings it close to Earth. NASA helpfully provides a [glossary](https://cneos.jpl.nasa.gov/glossary/) to define any unfamiliar terms you might encounter.

Importantly, these datasets come directly from NASA - we haven't dressed them up for you at all.

### Small-Bodies Dataset

NASA's Jet Propulsion Laboratory (JPL) provides [a web interface](https://ssd.jpl.nasa.gov/sbdb_query.cgi) to their database of "small bodies" - mostly asteroids and comets - in the solar system. A subset of these small bodies are near-Earth objects (NEOs): "comets and asteroids that have been nudged by the gravitational attraction of nearby planets into orbits that allow them to enter the Earth's neighborhood." [1]

From this dataset, you can answer questions such as "what is the diameter of the Halley's Comet?" or "is the near-Earth object named 'Eros' potentially hazardous?".

NASA's web service lets you download their data on near-Earth objects in a CSV format. For this project, the data set we've provided (`neos.csv`) comes directly from a query in which we limited the "Object Group" to NEOs and in which we selected _every_ output field. That's a _lot_ of columns (75, to be exact)!

Let's take an initial look at the first three rows of `neos.csv`:

```
id,spkid,full_name,pdes,name,prefix,neo,pha,H,G,M1,M2,K1,K2,PC,diameter,extent,albedo,rot_per,GM,BV,UB,IR,spec_B,spec_T,H_sigma,diameter_sigma,orbit_id,epoch,epoch_mjd,epoch_cal,equinox,e,a,q,i,om,w,ma,ad,n,tp,tp_cal,per,per_y,moid,moid_ld,moid_jup,t_jup,sigma_e,sigma_a,sigma_q,sigma_i,sigma_om,sigma_w,sigma_ma,sigma_ad,sigma_n,sigma_tp,sigma_per,class,producer,data_arc,first_obs,last_obs,n_obs_used,n_del_obs_used,n_dop_obs_used,condition_code,rms,two_body,A1,A2,A3,DT
a0000433,2000433,"   433 Eros (A898 PA)",433,Eros,,Y,N,10.4,0.46,,,,,,16.84,34.4x11.2x11.2,0.25,5.270,4.463e-04,0.921,0.531,,S,S,,0.06,"JPL 658",2459000.5,59000,20200531.0000000,J2000,.2229512647434284,1.458045729081037,1.132972589728666,10.83054121829922,304.2993259000444,178.8822959227224,271.0717325705167,1.783118868433408,.5598186418120109,2459159.351922368362,20201105.8519224,643.0654021001488,1.76061711731731,.148623,57.83961291,3.2865,4.582,9.6497E-9,2.1374E-10,1.4063E-8,1.1645E-6,3.8525E-6,4.088E-6,1.4389E-6,2.6139E-10,1.231E-10,2.5792E-6,1.414E-7,AMO,Giorgini,46330,1893-10-29,2020-09-03,8767,4,2,0,.28397,,,,,
a0000719,2000719,"   719 Albert (A911 TB)",719,Albert,,Y,N,15.5,,,,,,,,,,5.801,,,,,S,,,,"JPL 214",2459000.5,59000,20200531.0000000,J2000,.5465584653041263,2.63860206439375,1.196451769530403,11.56748478123323,183.8669499802364,156.17633771,140.2734217745985,4.080752359257098,.2299551959241748,2458390.496728663387,20180928.9967287,1565.522355575327,4.28616661348481,.203482,79.18908994,1.41794,3.140,2.1784E-8,2.5313E-9,5.8116E-8,2.9108E-6,1.6575E-5,1.6827E-5,2.5213E-6,3.9148E-9,3.309E-10,1.0306E-5,2.2528E-6,AMO,"Otto Matic",39593,1911-10-04,2020-02-27,1874,,,0,.39148,,,,,
```

Before we're able to write Python code to process this data, we'll need to understand what this data represents.

In this CSV file, the first row is a header, containing names for each of the columns. Each subsequent row represents a single NEO. There are too many columns to understand fully (although we encourage you to learn more by searching NASA's website!), so we'll focus on just a few of them:

```
pdes - the primary designation of the NEO. This is a unique identifier in the database, and its "name" to computer systems.
name - the International Astronomical Union (IAU) name of the NEO. This is its "name" to humans.
pha - whether NASA has marked the NEO as a "Potentially Hazardous Asteroid," roughly meaning that it's large and can come quite close to Earth.
diameter - the NEO's diameter (from an equivalent sphere) in kilometers.
```

So, the first NEO described in the CSV file has a primary designation of 433 and an IAU name "Eros". It is ('Y') an NEO, but it is not ('N') potentially hazardous. It has a diameter of 16.84km.

Every NEO has a primary designation, but there exist NEOs without names (in fact, having an IAU name is relatively rare!). Some IAU names are reused for several NEOs. For some NEOs, the data doesn't include information about a diameter, because NASA does not have enough observations to make a reasonably-accurate estimate.

If you'd like to explore individual NEOs in more detail (and perhaps interpret a few of the rest of the columns), NASA also provides a [web interface to search for a single small body](https://ssd.jpl.nasa.gov/sbdb.cgi) as well as [an API](https://ssd-api.jpl.nasa.gov/doc/sbdb.html).

[1]: https://cneos.jpl.nasa.gov/about/basics.html

### Close Approach Dataset

NASA's Center for Near-Earth Object Studies (CNEOS) also provides data about close approaches of NEOs to Earth. A close approach occurs when an NEO's orbit path brings it near Earth - although, "near" in astronomical terms can be quite far in human-scale units, such as kilometers. Instead of kilometers, astronomical distances within the solar system are often measured with the astronomical unit (au) - the mean distance between the Earth and the sun - although sometimes you'll see distances measured with the lunar distance (ld) - the mean distance between the Earth and the moon - or even plain old kilometers.

From this dataset, you can answer questions such as "On which date(s) does Halley's Comet pass near to Earth?" or "How fast does Eros pass by Earth, on average?"

The data is JSON-formatted, and we've downloaded it from NASA's public API. A description of the API, as well as details about the query parameters and the scheme of the returned data, can be found [here](https://ssd-api.jpl.nasa.gov/doc/cad.html). Concretely, we asked NASA for this data by querying the API at `https://ssd-api.jpl.nasa.gov/cad.api?date-min=1900-01-01&date-max=2100-01-01&dist-max=1`. In other words, our data set contains all currently known close approaches that have happened or will happen in the 20th and 21st centuries! Additionally, NASA provides the data is chronological order.

Let's take an initial look at the data in `cad.json`.

```json
{
  "signature":{
    "source":"NASA/JPL SBDB Close Approach Data API",
    "version":"1.1"
  },
  "count":"406785",
  "fields":["des", "orbit_id", "jd", "cd", "dist", "dist_min", "dist_max", "v_rel", "v_inf", "t_sigma_f", "h"],
  "data":[
    [
       "170903",
       "105",
       "2415020.507669610",
       "1900-Jan-01 00:11",
       "0.0921795123769547",
       "0.0912006569517418",
       "0.0931589328621254",
       "16.7523040362574",
       "16.7505784933163",
       "01:00",
       "18.1"
    ],
    [
       "2005 OE3",
       "52",
       "2415020.606013490",
       "1900-Jan-01 02:33",
       "0.414975519685102",
       "0.414968315685577",
       "0.414982724454678",
       "17.918395877175",
       "17.9180375373357",
       "< 00:01",
       "20.3"
    ],
    ...
  ]
}
```

It certainly looks different from the CSV data!

The top-level JSON payload is a dictionary with keys "signature", "count", "fields", and "data". The "signature" field shows where this data came from - in this case, from the API provided by NASA/JPL. The "count" field tells us how many entries to expect in the "data" section. The "fields" key maps to a list of strings describing how we should interpret the entries in the "data" section. Lastly, the "data" section itself maps to a list of lists - each element is a list of data for a single close approach, corresponding (by order) with the "fields" key.

What do each of the fields mean? [NASA's API documentation](https://ssd-api.jpl.nasa.gov/doc/cad.html) provides the answer:

> * des - primary designation of the asteroid or comet (e.g., 443, 2000 SG344)
> * orbit_id - orbit ID
> * jd - time of close-approach (JD Ephemeris Time)
> * cd - time of close-approach (formatted calendar date/time, in UTC)
> * dist - nominal approach distance (au)
> * dist_min - minimum (3-sigma) approach distance (au)
> * dist_max - maximum (3-sigma) approach distance (au)
> * v_rel - velocity relative to the approach body at close approach (km/s)
> * v_inf - velocity relative to a massless body (km/s)
> * t_sigma_f - 3-sigma uncertainty in the time of close-approach (formatted in days, hours, and minutes; days are not included if zero; example "13:02" is 13 hours 2 minutes; example "2_09:08" is 2 days 9 hours 8 minutes)
> * h - absolute magnitude H (mag)

With this in mind, we can interpret that the first close approach contained in the dataset is:

* an asteroid or comet with primary designation "170903"
* an orbit ID of 105
* a close approach time of 2415020.507669610 (in JD Ephemeris time) or 1900-Jan-01 00:11 (in a normal format)
* an approach distance of 0.0921795123769547 astronomical units (with 3-sigma bounds of (0.0912006569517418au, 0.0931589328621254au))
* an approach velocity of 16.7523040362574 km/s (relative to Earth) or 16.7505784933163 km/s (relative to a massless body)
* 3-sigma uncertainty in the time of close approach of 1 hour
* an absolute magnitude of 18.1

The second close approach contained in the dataset is:

* an asteroid or comet with primary designation "2005 OE3"
* an orbit ID of 52
* a close approach time of 2415020.606013490 (in JD Ephemeris time) or 1900-Jan-01 02:33 (in a normal format)
* an approach distance of 0.414975519685102 astronomical units (with 3-sigma bounds of (0.414968315685577au, 0.414982724454678au))
* an approach velocity of 17.918395877175 km/s (relative to Earth) or 17.9180375373357 km/s (relative to a massless body)
* 3-sigma uncertainty in the time of close approach of less than 1 minute.
* an absolute magnitude of 20.3

As before, this data set contains more information than we need. For this project, we'll make use of the `des`, `cd`, `dist`, and `v_rel` measurements - although the other attributes can be useful if you wish to extend the project! Fortunately, each entry has well-formatted data for each of these attributes.

### Visual Exploration

If you're someone who prefers to explore data sets by poking around a web site, NASA has [a tutorial video](https://www.youtube.com/watch?v=UA6voCyCW1g) on how to effectively navigate the CNEOS website, and an [interactive close approach data table](https://cneos.jpl.nasa.gov/ca/) that you can investigate.

Also, it's important to realize that NASA is discovering new NEOs, and potential forecasting new close approaches, every week, so their web-based UI might contain updated information that isn't represented in the data files included with this project.

## Project Interface

Now that we understand the data with which we'll be working, let's dive into what our program will actually do

This project is driven by the `main.py` script. That means that you'll run `python3 main.py ... ... ...` at the command line to invoke the program that will call your code.

At a command line, you can run `python3 main.py --help` for an explanation of how to invoke the script.

```python
usage: main.py [-h] [--neofile NEOFILE] [--cadfile CADFILE] {inspect,query,interactive} ...

Explore past and future close approaches of near-Earth objects.

positional arguments:
  {inspect,query,interactive}

optional arguments:
  -h, --help            show this help message and exit
  --neofile NEOFILE     Path to CSV file of near-Earth objects.
  --cadfile CADFILE     Path to JSON file of close approach data.
```

There are three subcommands: `inspect`, `query`, and `interactive`. Let's take a look at the interfaces of each of these subcommands.

### `inspect`

The `inspect` subcommand inspects a single NEO, printing its details in a human-readable format. The NEO is specified with exactly one of the `--pdes` option (the primary designation) and the `--name` option (the IAU name). The `--verbose` flag additionally prints out, in a human-readable form, all known close approaches to Earth made by this NEO. Each of these options has an abbreviated version. To remind yourself of the full interface, you can run `python3 main.py inspect --help`:

```
$ python3 main.py inspect --help
usage: main.py inspect [-h] [-v] (-p PDES | -n NAME)

Inspect an NEO by primary designation or by name.

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Additionally, print all known close approaches of this NEO.
  -p PDES, --pdes PDES  The primary designation of the NEO to inspect (e.g. '433').
  -n NAME, --name NAME  The IAU name of the NEO to inspect (e.g. 'Halley').
```

Here are a few examples of the `inspect` subcommand in action:

```
# Inspect the NEO with a primary designation of 433 (that's Eros!)
$ python3 main.py inspect --pdes 433
NEO 433 (Eros) has a diameter of 16.840 km and is not potentially hazardous.

# Inspect the NEO with an IAU name of "Halley" (that's Halley's Comet!)
$ python3 main.py inspect --name Halley
NEO 1P (Halley) has a diameter of 11.000 km and is not potentially hazardous.

# Attempt to inspect an NEO that doesn't exist.
$ python3 main.py inspect --name fake-comet
No matching NEOs exist in the database.

# Verbosely list information about Ganymed and each of its known close approaches.
# For the record, Ganymed is HUGE - it's the largest known NEO.
$ python3 main.py inspect --verbose --name Ganymed
NEO 1036 (Ganymed) has a diameter of 37.675 km and is not potentially hazardous.
- On 1911-10-15 19:16, '1036 (Ganymed)' approaches Earth at a distance of 0.38 au and a velocity of 17.09 km/s.
- On 1924-10-17 00:51, '1036 (Ganymed)' approaches Earth at a distance of 0.50 au and a velocity of 19.36 km/s.
- On 1998-10-14 05:12, '1036 (Ganymed)' approaches Earth at a distance of 0.46 au and a velocity of 13.64 km/s.
- On 2011-10-13 00:04, '1036 (Ganymed)' approaches Earth at a distance of 0.36 au and a velocity of 14.30 km/s.
- On 2024-10-13 01:56, '1036 (Ganymed)' approaches Earth at a distance of 0.37 au and a velocity of 16.33 km/s.
- On 2037-10-15 18:31, '1036 (Ganymed)' approaches Earth at a distance of 0.47 au and a velocity of 18.68 km/s.
```

For an NEO to be found with the `inspect` subcommand, the given primary designation or IAU name must match the data exactly, so if an NEO is mysteriously missing, double-check the spelling and capitalization.

### `query`

The `query` subcommand is more significantly more advanced - a `query` generates a collection of close approaches that match a set of specified filters, and either displays a limited set of those results to standard output or writes the structured results to a file.

```
$ python3 main.py query --help
usage: main.py query [-h] [-d DATE] [-s START_DATE] [-e END_DATE] [--min-distance DISTANCE_MIN] [--max-distance DISTANCE_MAX]
                     [--min-velocity VELOCITY_MIN] [--max-velocity VELOCITY_MAX] [--min-diameter DIAMETER_MIN]
                     [--max-diameter DIAMETER_MAX] [--hazardous] [--not-hazardous] [-l LIMIT] [-o OUTFILE]

Query for close approaches that match a collection of filters.

optional arguments:
  -h, --help            show this help message and exit
  -l LIMIT, --limit LIMIT
                        The maximum number of matches to return. Defaults to 10 if no --outfile is given.
  -o OUTFILE, --outfile OUTFILE
                        File in which to save structured results. If omitted, results are printed to standard output.

Filters:
  Filter close approaches by their attributes or the attributes of their NEOs.

  -d DATE, --date DATE  Only return close approaches on the given date, in YYYY-MM-DD format (e.g. 2020-12-31).
  -s START_DATE, --start-date START_DATE
                        Only return close approaches on or after the given date, in YYYY-MM-DD format (e.g. 2020-12-31).
  -e END_DATE, --end-date END_DATE
                        Only return close approaches on or before the given date, in YYYY-MM-DD format (e.g. 2020-12-31).
  --min-distance DISTANCE_MIN
                        In astronomical units. Only return close approaches that pass as far or farther away from Earth as the given
                        distance.
  --max-distance DISTANCE_MAX
                        In astronomical units. Only return close approaches that pass as near or nearer to Earth as the given
                        distance.
  --min-velocity VELOCITY_MIN
                        In kilometers per second. Only return close approaches whose relative velocity to Earth at approach is as fast
                        or faster than the given velocity.
  --max-velocity VELOCITY_MAX
                        In kilometers per second. Only return close approaches whose relative velocity to Earth at approach is as slow
                        or slower than the given velocity.
  --min-diameter DIAMETER_MIN
                        In kilometers. Only return close approaches of NEOs with diameters as large or larger than the given size.
  --max-diameter DIAMETER_MAX
                        In kilometers. Only return close approaches of NEOs with diameters as small or smaller than the given size.
  --hazardous           If specified, only return close approaches of NEOs that are potentially hazardous.
  --not-hazardous       If specified, only return close approaches of NEOs that are not potentially hazardous.
```

Here are a few examples of the `query` subcommand in action:

```
# Show (the first) two close approaches in the data set.
$ python3 main.py query --limit 2
On 1900-01-01 00:11, '170903' approaches Earth at a distance of 0.09 au and a velocity of 16.75 km/s.
On 1900-01-01 02:33, '2005 OE3' approaches Earth at a distance of 0.41 au and a velocity of 17.92 km/s.

# Show (the first) three close approaches on July 29th, 1969.
$ python3 main.py query --date 1969-07-29 --limit 3
On 1969-07-29 01:47, '408982' approaches Earth at a distance of 0.36 au and a velocity of 24.24 km/s.
On 1969-07-29 13:33, '2010 MA' approaches Earth at a distance of 0.21 au and a velocity of 8.80 km/s.
On 1969-07-29 19:56, '464798' approaches Earth at a distance of 0.10 au and a velocity of 8.02 km/s.

# Show (the first) three close approaches in 2050.
$ python3 main.py query --start-date 2050-01-01 --limit 3
On 2050-01-01 04:18, '2019 AY9' approaches Earth at a distance of 0.31 au and a velocity of 8.31 km/s.
On 2050-01-01 06:00, '162361' approaches Earth at a distance of 0.19 au and a velocity of 9.08 km/s.
On 2050-01-01 09:55, '2009 LW2' approaches Earth at a distance of 0.04 au and a velocity of 19.02 km/s.

# Show (the first) four close approaches in March 2020 that passed at least 0.4au of Earth.
$ python3 main.py query --start-date 2020-03-01 --end-date 2020-03-31 --min-distance 0.4 --limit 4
On 2020-03-01 00:28, '152561' approaches Earth at a distance of 0.42 au and a velocity of 11.23 km/s.
On 2020-03-01 09:28, '462550' approaches Earth at a distance of 0.47 au and a velocity of 17.19 km/s.
On 2020-03-02 21:41, '2020 QF2' approaches Earth at a distance of 0.45 au and a velocity of 8.79 km/s.
On 2020-03-03 00:49, '2019 TU' approaches Earth at a distance of 0.49 au and a velocity of 5.92 km/s.

# Show (the first) three close approaches that passed at most 0.0025au from Earth with a relative speed of at most 5 km/s.
# That's slightly less than the average distance between the Earth and the moon.
$ python3 main.py query --max-distance 0.0025 --max-velocity 5 --limit 3
On 1949-01-01 02:53, '2003 YS70' approaches Earth at a distance of 0.00 au and a velocity of 3.64 km/s.
On 1954-03-13 00:00, '2013 RZ53' approaches Earth at a distance of 0.00 au and a velocity of 3.04 km/s.
On 1979-09-02 00:16, '2014 WX202' approaches Earth at a distance of 0.00 au and a velocity of 1.79 km/s.

# Show (the first) three close approaches in the 2000s of NEOs with a known diameter of least 6 kilometers that passed Earth at a relative velocity of at least 15 km/s.
$ python3 main.py query --start-date 2000-01-01 --min-velocity 15 --min-diameter 6 --limit 3
On 2000-05-21 10:08, '7092 (Cadmus)' approaches Earth at a distance of 0.34 au and a velocity of 28.46 km/s.
On 2004-05-25 03:54, '7092 (Cadmus)' approaches Earth at a distance of 0.41 au and a velocity of 30.52 km/s.
On 2006-06-10 20:04, '1866 (Sisyphus)' approaches Earth at a distance of 0.49 au and a velocity of 26.81 km/s.

# Show (the first) two close approaches in January 2030 of NEOs that are at most 50m in diameter and are marked not potentially hazardous.
$ python3 main.py query --start-date 2030-01-01 --end-date 2030-01-31 --max-diameter 0.05 --not-hazardous --limit 2
On 2030-01-07 20:59, '2010 GH7' approaches Earth at a distance of 0.46 au and a velocity of 18.84 km/s.
On 2030-01-13 07:29, '2010 AE30' approaches Earth at a distance of 0.06 au and a velocity of 14.00 km/s.

# Show (the first) three close approaches in 2021 of potentially hazardous NEOs at least 100m in diameter that pass within 0.1au of Earth at a relative velocity of at least 15 kilometers per second.
$ python3 main.py query --start-date 2021-01-01 --max-distance 0.1 --min-velocity 15 --min-diameter 0.1 --hazardous --limit 3
On 2021-01-21 22:56, '363024' approaches Earth at a distance of 0.07 au and a velocity of 15.31 km/s.
On 2021-02-01 22:26, '2016 CL136' approaches Earth at a distance of 0.04 au and a velocity of 18.06 km/s.
On 2021-08-21 15:10, '2016 AJ193' approaches Earth at a distance of 0.02 au and a velocity of 26.17 km/s.

# Save, to a CSV file,  all close approaches.
$ python3 main.py query --outfile results.csv

# Save, to a JSON file, all close approaches in the 2020s of NEOs at least 1km in diameter that pass between 0.01 au and 0.1 au away from Earth.
$ python3 main.py query --start-date 2020-01-01 --end-date 2029-12-31 --min-diameter 1 --min-distance 0.01 --max-distance 0.1 --outfile results.json
```

### `interactive`

There's a third useful subcommand named `interactive`. This subcommand first loads the database and then starts a command loop so that you can repeatedly run `inspect` and `query` subcommands on the database without having to wait to reload the data each time you want to run a new command, which saves an extraordinary amount of time. This can be extremely helpful, as it lets you speed up your development cycle and even show off the project more easily to friends.

Here's what an example session might look like:

```
$ python3 main.py interactive
Explore close approaches of near-Earth objects. Type `help` or `?` to list commands and `exit` to exit.

(neo) inspect --pdes 433
NEO 433 (Eros) has a diameter of 16.840 km and is not potentially hazardous.
(neo) help i
Shorthand for `inspect`.
(neo) i --name Halley
NEO 1P (Halley) has a diameter of 11.000 km and is not potentially hazardous.
(neo) query --date 2020-12-31 --limit 2
On 2020-12-31 05:48, '2010 PQ10' approaches Earth at a distance of 0.45 au and a velocity of 21.69 km/s.
On 2020-12-31 16:00, '2015 YA' approaches Earth at a distance of 0.17 au and a velocity of 5.65 km/s.
(neo) q --date 2021-3-14 --min-velocity 10
On 2021-03-14 06:17, '2019 DS1' approaches Earth at a distance of 0.39 au and a velocity of 20.17 km/s.
On 2021-03-14 20:19, '483656' approaches Earth at a distance of 0.06 au and a velocity of 12.09 km/s.
...
```

The prompt is `(neo) `. At the prompt, you can enter either an `inspect` or a `query` subcommand, with the exact same options and behavior as you would on the command line. You can use the special command `quit`, `exit`, or `CTRL+D` to exit this session and return to the command line. The command `help` or `?` shows a help menu, and `help <command>` (e.g. `help query`) shows a help menu specific to that command. In this environment only, you can also use the short forms `i` and `q` for `inspect` and `query` (e.g. `(neo) i --verbose --name Ganymed)`).

Importantly, **the `interactive` session doesn't automatically update when you update your code.** This means that, if you make a meaningful change to your Python files, you should exit and restart the session. If the interactive session detects that any Python files have changed since it began, it will warn you before it runs each new command. The `interactive` subcommand takes an optional argument `--aggressive` - if specified, the interactive session will instead preemptively exit whenever it notices any changes to any Python files.

All in all, the `interactive` subcommand has the following options:

```
$ python3 main.py interactive --help
usage: main.py interactive [-h] [-a]

Start an interactive command session to repeatedly run `interact` and `query` commands.

optional arguments:
  -h, --help        show this help message and exit
  -a, --aggressive  If specified, kill the session whenever a project file is modified.
```

## Project Scaffolding

Upon starting, the project contains several files and folders to help you get up and running:

```
.
├── README.md       # This file.
├── main.py
├── models.py       # Task 1.
├── read.py         # Task 2a.
├── database.py     # Task 2b and Task 3b.
├── filters.py      # Task 3a and Task 3c.
├── write.py        # Task 4.
├── helpers.py
├── data
│   ├── neos.csv
│   └── cad.json
└── tests
    ├── test-neos-2020.csv
    ├── test-cad-2020.json
    ├── test_*.py
    ├── ...
    └── test_*.py
```

Let's take a closer look at the purpose of each of these files and folders:

- `main.py`: The main Python script that wraps the command-line tool, orchestrates the data pipeline by invoking the functions and classes that you'll write. **You will not need to modify this file.**
- `models.py`: In this file, you'll define Python objects to represent a `NearEarthObject` and a `CloseApproach`. These objects will have a few attributes, a human-readable string representatino, and perhaps a property or a method here or there.
- `extract.py`: In this file, you'll write functions to read information from data files, creating `NearEarthObject`s and `CloseApproaches` from the data.
- `database.py`: In this file, you'll define an `NEODatabase` class to encapsulate the entire data set (connecting NEOs and close approaches) and write methods to get NEOs by primary designation and by name, as well as to query the dataset with a collection of user-specified filters to generate an iterable stream of matching results.
- `filters.py`: In this file, you'll create a plethora of filters to be used in conjuction with the `NEODatabase` to query for a stream of matching close approaches. You'll also write a utility function to limit the number of results produced from a stream.
- `write.py`: Finally, in this file, you'll implement functions to write a stream of results (the `CloseApproach` objects generated by the `NEODatabase`) to a file either in JSON format or in CSV format.
- `helpers.py`: A simple module that provides a few helpful utility functions to convert to and from datetime objects.

The data files are located in the `data/` folder.

Additionally, the starter code includes unit tests that will help you check your progress as you advance through this project. The unit tests all live in the `tests/` folder. When the project is fully implemented, all of the unit tests should pass. To run all of the tests, you can use `python3 -m unittest --verbose` at the command line, although many tests will currently fail since the project isn't yet finished.

## Tasks to Complete

### Overview

At a high-level, we'll break down this project into a few manageable tasks.

- Task 0: Inspect the data. (`data/neos.csv` and `data/cad.json`)
- Task 1: Build models to represent the data. (`models.py`)
- Task 2: Extract the data into a custom database (`extract.py` and `database.py`)
- Task 3: Create filters to query the database to generate a stream of matching `CloseApproach` objects, and limit the result size. (`filters.py` and `database.py`)
- Task 4: Save the data to a file. (`write.py`)

As you implement these tasks, you'll unlock more and more functionality. When Task 2 is complete, you'll be able to run the `inspect` subcommand. When Task 3 is complete, you'll be able to run the `query` subcommand without the `--outfile` argument. When Task 4 is complete, you'll be able to run everything.

Remember, in this project you won't need to write any code that prompts the user for input - the `main.py` script will accept arguments from the command line or the interactive session and pass that information to the appropriate Python classes and functions that you create.

### Task 0: Inspect the data set.

The very first step of any project involving known data should _always_ be to manually explore the data set. With any tool you'd like (Excel, a text editor, NASA's online browsers, etc), attempt to answer the following questions before you move on.

- How many NEOs are in the `neos.csv` data set?
  - Hint: Count the number of rows in the `neos.csv` file.
  - Answer: 23967
- What is the primary designation of the first Near Earth Object in the `neos.csv` data set?
  - Hint: Look at the first row of the CSV, under the header "pdes"
  - Answer: 433
- What is the diameter of the NEO whose name is "Apollo"?
  - Hint: Look for the row of the CSV containing the name "Apollo" in the "name" column, and find the entry under the "diameter" column.
  - Answer: 1.5 kilometers
- How many NEOs have IAU names in the data set?
  - Hint: Count the number of rows that have nonempty entries in the "name" column.
  - Answer: 343
- How many NEOs have diameters in the data set?
  - Hint: Count the number of rows that have nonempty entries in the "diameter" column.
  - Answer: 1268
- How many close approaches are in the `cad.json` data set?
  - Hint: Instead of manually counting the entries, you can use the value of the "count" key.
  - Answer: 406785
- On January 1st, 2000, how close did the NEO whose primary designation is "2015 CL" pass by Earth?
  - Find entries whose date starts with '2000-Jan-01'. One of the lists represents the close approach of the NEO "2015 CL". What is the value corresponding to the distance from Earth?
  - Answer: About 0.145 au
- On January 1st, 2000, how fast did the NEO whose primary designation is "2002 PB" pass by Earth?
  - Hint: Find entries whose date starts with '2000-Jan-01'. One of the lists represents the close approach of the NEO "2002 PB". What is the value corresponding to the velocity relative to Earth?
  - Answer: About 29.39 km/s

For this task, you might decide to use the Python interpreter to quickly answer some of these queries if they're too hard to answer by hand.

Have any lingering curiosities about the dataset? You may be able to use bespoke Python scripts to answer these questions, either now or as they come up.

### Task 1: Design the objects that will store our data.

Well done! Now that we understand the project overview and our data set, it's time to start coding. The first thing we'll do is create Python objects to represent our data. In particular, we're going to create two classes in the `models.py` file:

- A `NearEarthObject` class, to represent the data for a single near-Earth object.
- A `CloseApproach` class, to represent the data for a single close approach of an NEO.

In doing so, we'll have to decide how to construct new instances of this class, which attributes from our dataset belong to each object, how to build a human-readable representation this object, and which additional methods or properties, if any, we want to include. We'll also have to plan for how these objects will interact with each other.

#### Designing the `NearEarthObject` class

The `models.py` file contains a starting template for the `NearEarthObject` class. This class object will represent a single near-Earth object.

```
class NearEarthObject:
    def __init__(self, ...):
        ...

    def __str__(self):
        ...
```

The `__init__` method is the constructor for the class. You will need to decide what arguments it should accept. If you make changes, you should also update the surrounding comments.

The `__str__` method will return a human-readable string that captures the contents of the class for a human audience. In contrast, the prewritten `__repr__` method is stylized to be machine-readable.

Each `NearEarthObject` must have attributes (or gettable properties) for the following names:

- `designation`: The primary designation for this `NearEarthObject`.
- `name`: The IAU name for this `NearEarthObject`.
- `diameter`: The diameter, in kilometers, of this `NearEarthObject`.
- `hazardous`: Whether or not this `NearEarthObject` is potentially hazardous.
- `approaches`: A collection of this `NearEarthObject`s close approaches to Earth.

The starter code contains default values for some of these attributes - you should decide how, and if, to replace that code.

Recall that, even though every NEO in the data set has a nonempty primary designation, some NEOs have no name, and some NEOs have no diameter (it's unknown to NASA).

The `designation` should resolve to a string, the `name` should resolve to either a nonempty string or the value `None`, the `diameter` should resolve to a float (you should use `float('nan')` to represent an undefined diameter), and the `hazardous` flag should resolve to a boolean.

The `approaches` attribute, for now, can be an empty collection. In Task 2, you'll use the real data set to populate this collection with the real `CloseApproach` data.

The `__str__` method that you write is up to you - it'll determine how this object is printed, and should be human-readable. For inspiration, we adopted the following format:

```
>>> neo = ...
>>> print(neo)
NEO {fullname} has a diameter of {diameter:.3f} km and [is/is not] potentially hazardous.
>>> halley = ...
>>> print(halley)
NEO 433 (Eros) has a diameter of 16.840 km and is not potentially hazardous.
```

In the above, `{fullname}` is either `{designation} ({name})` if the `name` exists or simply `{designation}` otherwise. As a hint, this is a great opportunity for a property named `fullname`!

#### Designing the `CloseApproach` class

The `models.py` file also contains a starting template for the `CloseApproach` class. This class object will represent a single close approach to Earth by a near-Earth object.

```
class CloseApproach:
    def __init__(self, ...):
        ...

    def __str__(self):
        ...
```

The `__init__` method is the constructor for the class. You will need to decide what arguments it should accept. If you make changes, you should also update the surrounding comments.

The `__str__` method will return a human-readable string that captures the contents of the class for a human audience. In contrast, the prewritten `__repr__` method is stylized to be machine-readable.

Each `CloseApproach` must have attributes (or gettable properties) for the following names:

- `time`: The date and time, in UTC, at which the NEO passes closest to Earth.
- `distance`: The nominal approach distance, in astronomical units, of the NEO to Earth at the closest point.
- `velocity`: The velocity, in kilometers per second, of the NEO relative to Earth at the closest point.
- `neo`: The `NearEarthObject` that is making a close approach to Earth.

The `date` should resolve to a Python datetime, the `distance` should resolve to a float, and the `velocity` should resolve to a float.

The `neo` attribute, for now, can be `None`. In its absence, you should include a `_designation` attribute with the primary designation of the close approach's NEO. In Task 2, you'll use the real data set and this `_designation` attribute to connect the `neo` attribute to a real `NearEarthObject` instance.

You can use the `cd_to_datetime` function in the `helpers` module to convert a calendar date from the format provided in `cad.json` (e.g. "1900-Jan-01 00:00") into a Python `datetime` object.

The `__str__` method that you write is up to you - it'll determine how this object is printed, and should be human-readable. For inspiration, we adopted the following format:

```
>>> ca = ...
>>> print(ca)
At {time_str}, '{neo.fullname}' approaches Earth at a distance of {distance:.2f} au and a velocity of {velocity:.2f} km/s.
>>> halley_approach = ...
>>> print(halley_approach)
On 1910-05-20 12:49, '1P (Halley)' approaches Earth at a distance of 0.15 au and a velocity of 70.56 km/s.
```

You should use the `datetime_to_str` function from the `helpers` module to format the `time` attribute to a string without seconds. This is another great opportunity for a property!

#### Testing

Make sure to manually test your implementation at an interactive interpreter. Your interactive session might look something like:

```
$ python3 -q
>>> from models import NearEarthObject, CloseApproach
>>> neo = NearEarthObject(...)  # Use any sample data here.
>>> print(neo.designation)
2020 FK
>>> print(neo.name)
One REALLY BIG fake asteroid
>>> print(neo.diameter)
12.345
>>> print(neo.hazardous)
True
>>> print(neo)
NEO 2020 FK (One REALLY BIG fake asteroid) has a diameter of 12.345 km and is potentially hazardous.
>>> ca = CloseApproach(...)  # Use any sample data here.
>>> print(type(ca.time))
datetime.datetime
>>> print(ca.time_str)
2020-01-01 12:30
>>> print(ca.distance)
0.25
>>> print(ca.velocity)
56.78
>>> print(ca)
On 2020-01-01 12:30, '2020 FK (One REALLY BIG fake asteroid)' approaches Earth at a distance of 0.25 au and a velocity of 56.78 km/s.
```

As you progress the the remaining tasks, you may have to revisit this file to adapt your implementation - that's expected!

### Task 2: Extract data from structures files into Python objects.

Wonderful! Now that we've defined Python objects in `models.py` that can represent our data, let's extract the real data from our data sets.

For this task, we'll make changes in two files:

- In `extract.py`, we'll write functions that takes the paths to our data files and extract structured data.
- In `database.py`, we'll capture this data in an `NEODatabase`, precompute auxiliary data structures, interconnect the `NearEarthObject`s and `CloseApproach`es, and provide the ability to fetch NEOs by designation or by name.

#### Task 2a: Extract data from data files.

In the `extract.py` file, you'll implement the `load_neos` and `load_approaches` functions:

```
def load_neos(neo_csv_path):
    ...
    return a collection of `NearEarthObject` instances.

def load_approaches(cad_json_path):
    ...
    return a collection of `CloseApproach` instances.
```

The `neo_csv_path` and `cad_json_path` arguments are Path-like objects corresponding either to the default `data/neos.csv` and `data/cad.json` or to some alternate location specifed by the user at the command line. You can `open(neo_csv_path)` or `open(cad_json_path)` as usual.

In this module, you'll have to use the built-in `csv` and `json` modules. You'll also need to rely on the `NearEarthObject` and `CloseApproach` classes you defined in Task 1, which you could end up adapting if needed.

The collections returned by `load_neos` and `load_approaches` are then used by the `main.py` script to create an `NEODatabase`.

#### Task 2b: Encapsulate the data in a `NEODatabase`.

In the `database.py` file, you'll implement the `__init__` constructor of the `NEODatabase` object and finish the `get_neo_by_designation` and `get_neo_by_name` methods. At the start, the `NEODatabase` class looks like:

```
class NEODatabase:
    def __init__(self, neos, approaches):
        ...
    def get_neo_by_designation(self, designation):
        ...
    def get_neo_by_name(self, name):
        ...
```

The `neos` and `approaches` arguments provided to the `NEODatabase` constructor are exactly the objects produced by the `load_neos` and `load_approaches` functions of the `extract` module.

In the `NEODatabase` constructor, you must connect together the collection of `NearEarthObject`s and the collection of `CloseApproach`es. Specifically, for each close approach, you should determine to which NEO its `_designation` corresponds, and assign that `NearEarthObject` to the `CloseApproach`'s `.neo` attribute (which we set to `None` in Task 1). Additionally, you should add this close approach to the `NearEarthObject`'s `.approaches` attribute, which represents a collection of `CloseApproach`es (which we initialized to an empty collection in Task 1).

In addition to storing the newly-connected NEOs and close approaches, you'll likely want to precompute some helpful auxiliary data structures that can speed up the `get_neo_by_designation` and `get_neo_by_name` methods. If you loop over every known NEO in those methods, the resulting code will be unnecessarily slow. What additional data structures can we attach to the `NEODatabase` that can assist with these methods?

Both the `get_neo_by_designation` and `get_neo_by_name` methods should return None if a matching NEO wasn't found in the database. For `get_neo_by_name`, in no case should the empty string nor the `None` singleton be associated to an NEO. Furthermore, in the relatively rare case that there are multiple NEOs with the same `name`, it's acceptable to return any of them.

#### Testing

It's always a good idea to manually test your implementation at an interactive interpreter. However, starting with Task 2, we provide additional tools for you to check your code.

You can use the pre-written unit tests to check that each of your functions and methods are working as required:

```
$ python3 -m unittest --verbose tests.test_extract tests.test_database
```

There are a total of 21 unit tests for this task. When Task 2 is complete, all of the unit tests in these two modules will pass.

Furthermore, after completing Task 2 entirely, the `inspect` subcommand will fully work. Therefore, you can use the command line to test your code as well:

```
$ python3 main.py inspect --name Halley
NEO 1P (Halley) has a diameter of 11.000 km and is not potentially hazardous.

# Inspect the NEO with a primary designation of 433 (that's Eros!)
$ python3 main.py inspect --pdes 433
NEO 433 (Eros) has a diameter of 16.840 km and is not potentially hazardous.

# Attempt to inspect an NEO that doesn't exist.
$ python3 main.py inspect --verbose --name Ganymed
NEO 1036 (Ganymed) has a diameter of 37.675 km and is not potentially hazardous.
- On 1911-10-15 19:16, '1036 (Ganymed)' approaches Earth at a distance of 0.38 au and a velocity of 17.09 km/s.
- On 1924-10-17 00:51, '1036 (Ganymed)' approaches Earth at a distance of 0.50 au and a velocity of 19.36 km/s.
- On 1998-10-14 05:12, '1036 (Ganymed)' approaches Earth at a distance of 0.46 au and a velocity of 13.64 km/s.
- On 2011-10-13 00:04, '1036 (Ganymed)' approaches Earth at a distance of 0.36 au and a velocity of 14.30 km/s.
- On 2024-10-13 01:56, '1036 (Ganymed)' approaches Earth at a distance of 0.37 au and a velocity of 16.33 km/s.
- On 2037-10-15 18:31, '1036 (Ganymed)' approaches Earth at a distance of 0.47 au and a velocity of 18.68 km/s.
```

Don't forget that you can use the `interactive` subcommand to repeatedly `inspect` NEOs without having to reload the database each time!

### Task 3: Query close approaches with user-specified criteria.

Woohoo! You're making real progress. We can extract data from structured files, create `NearEarthObject` and `CloseApproach` instances to represent that data, and capture the data in an `NEODatabase`. Now, we'll provide the ability to query the data set of close approaches for a limited size stream of matching results.

We'll split this task up into a few steps:

1. Create a collection of `Filter`s from the options given by the user at the command line.
2. Query the database's collection of close approaches to generate a stream of matching close approaches.
3. Limit the stream of results to at most some given maximum number.

There are several filters that we'll implementing, corresponding to options from the `query` subcommand:

- Date (`--date`, `--start-date`, `--end-date`)
- Distance (`--min-distance`, `--max-distance`)
- Velocity (`--min-velocity`, `--max-velocity`)
- Diameter (`--min-diameter`, `--max-diameter`)
- Hazardous (`--hazardous`, `--not-hazardous`)

Of these, the date, distance, and velocity filters apply to attributes of an instance of `CloseApproach`, whereas the diameter and hazardous filters apply to attributes of an instance of `NearEarthObject`. The date filter operates on Python date and datetime objects; the distance, velocity, and diameter filters operate on floats, and the hazardous filter operates on booleans.

You have a lot of design freedom in the first and second steps. They are closely related, so it's a good idea to start with just one filter type (distance, perhaps) in step 1, so that you can build and test step 2. Once step 1 and step 2 are working with a single filter type, you can expand to implement each of the rest of the filters. You can also leverage the tests (in `tests.test_query`, with `python3 -m unittest --verbose tests.test_query`) to measure your steady progress through the first two steps.

#### Task 3a: Creating filters.

For this step, you'll implement the `create_filters` function in the `filters.py` file. The `main.py` script calls this function with the options that the user provided at the command line.

```
def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):
```

If the user didn't provide an option, its value will be `None`. Note that, if the user specifies `--not-hazardous`, the value of the `hazardous` argument will be `False`, not to be confused with `None`.

You have tons of flexibility in what this object returns. The `main.py` script takes whatever it receives and passes it directly to the `query` method that you'll implement in Task 3b.

Designing a program with this much flexibility can be daunting, so we've prepared a first step for one possible approach (from which you can, and likely will, deviate) - under this plan, the `create_filters` function will produce a collection of instances of subclasses of `AttributeFilter` - a helper class we've already provided to you. You don't need to rely on `AttributeFilter` or even use it at all - you can delete it and pursue your own implementation design - but here's the idea:

What do these filters have in common? Each of them compares (with `<=`,`==`, or `>=`) some attribute (of a `CloseApproach` or a `NearEarthObject`) to a reference value. For example, the date filters check if the close approach date is equal to, less than or equal to, or greater than or equal to the date given on the command line. So, the three things that seem to be shared between all of our filters are (1) a way to get the attribute we're interested in and (2) a way to compare that attribute against (3) some reference value. Where there's shared behavior, there's an opportunity for decomposition.

```
class AttributeFilter:
    def __init__(self, op, value):
        self.op = op
        self.value = value

    def __call__(self, approach):
        return self.op(self.get(approach), self.value)

    @classmethod
    def get(cls, approach):
        raise UnsupportedCriterionError
```

The three elements are present in the `AttributeFilter` superclass - in (1) the class method `AttributeFilter.get`, (2) the `op` argument to the constructor, and (3) the `value` argument to the constructor.

This abstract superclass's `get` method raises `UnsupportedCriterionError`, a custom subclass of `NotImplementedError`, but concrete subclasses will be able to override this method to actually get a specific attribute of interest. The `op` argument will represent the operation corresponding to either `<=`, `==`, or `>=` - Python's `operator` module makes these available to us as `operator.le`, `operator.eq`, and `operator.ge`. That is, `operator.ge(a, b)` is the same as `a >= b`. Lastly, the `value` will just be our target value, as supplied by the user at the command line and fed to `create_filters` by the main module.

The `__call__` method makes instance objects of this type behave as callables - if we have an instance of a subclass of `AttributeFilter` named `f`, then the code `f(approach)` is really evaluating `f.__call__(approach)`. Specifically, "calling" the `AttributeFilter` with a `CloseApproach` object will get the attribute of interest (`self.get(approach)`) and compare it (via `self.op`) to the reference value (`self.value`), returning either True or False, representing whether that close approach satisfies the criterion.

As an example, suppose that we wanted to build an `AttributeFilter` that filtered on the `designation` attribute of the `NearEarthObject` attached to a `CloseApproach` (really, we wouldn't ever need this, because primary designations are unique and we already have `NEODatabase.get_neo_by_designation`). We could define a new subclass of `AttributeFilter`:

```
class DesignationFilter(AttributeFilter):
    @classmethod
    def get(cls, approach):
        return approach.neo.designation
```

We could then create and use an instance of this new class:

```
approach_433 = CloseApproach(...)
approach_other = CloseApproach(...)
f = DesignationFilter(operator.eq, '433')
f(approach_433)  # => True
f(approach_other)  # => True
```

This might seem complex - and it is. Are there different ways to do this? Well, yes. However, this is a relatively clean first approach, and the `AttributeFilter` is a first step towards unifying these filters, from which you can deviate freely.

##### On Comparing Dates

So far, we've been treating `date`s (naive Python objects that store a year, month, and day) and `datetime`s (naive Python objects that store a year, month, day, hour, minute, and seconds) as essentially interchangeable. Mostly, we haven't cared too much about the details. However, `date`s and `datetime`s are not comparable (would "May 1st" be before, after, or equal to "May 1st at noon"?).

The `date`, `start_date`, and `end_date` arguments supplied to `create_filters` are `date`s, but the `.time` attribute of a `CloseApproach` is a `datetime`. You can use the `.date()` method on `datetime` objects to get the corresponding moment as a `date`. That is, you aren't able to evaluate `start_date <= approach.time <= end_date` but you are able to evaluate `start_date <= approach.time.date() <= end_date`

#### Task 3b: Query the database of close approaches using user-specified criteria.

Let's turn our attention back to the `database.py` file. For this task, you'll implement the `query` method, which will generate a stream of `CloseApproach`es that match the user's criteria.

The `query` method accepts one argument - a collection of filters. The `main.py` script supplies to the `query` method whatever was returned from the `create_filters` function you implemented above.

You have a lot of freedom in how you implement this method - your implementation choice depends heavily on how you designed your filters in the previous section. In pseudo-code, we roughly expect the implementation to look something like the following:

```
define query(filters):
  for each approach in the database's collection of close approaches:
    if this close approach passes each of the criteria:
      yield this close approach
```

As before, you can certainly deviate from this pattern, especially depending on how you chose to implement the previous step.

Why `yield`? Recall that when we use `yield` in a Python function, it becomes a generator function, capable of pausing and resuming. Generators are often useful to represent sources of data streams. In our project, there might be thousands of close approaches matching the user's criteria, but we might only need to show the first ten (specified with the `--limit` command-line option). For these cases, we'll want the `query` function not to return a fully-computed collection of matching close approaches - which could take a while to compute - but rather to generate a stream of matching close approaches. In doing so, we'll make the `query` method almost instantaneous, and only do the work to determine the next element of the generator (the next matching `CloseApproach`) if another unit of code asks for it.

There are a plethora of other ways to optimize this method as well. For example, you could preprocess even more auxiliary data structures in the `NEODatabase` constructor to speed up specific queries. You might map dates to collections of close approaches that occurred on those dates, to speed up the `--date` criterion. You might order the close approaches by distance or velocity, or the NEOs by diameter, in order to more efficiently search for matches. Furthermore, you might be able to intelligently combine filters - for example, there are definitely no close approaches that are simulataneously closer than 0.1au (`--max-distance 0.1`) to Earth and further than 0.3au (`--max-distance 0.3`) from Earth. Depending on the exact approach you take, some of these changes may affect the design of your filters or the `create_filter` function, but there are many opportunities for performance improvements.

However, while these additional optimizations are certainly interesting - and in many cases can speed up the time it takes to perform complex queries - they are in no way necessary to successfully complete this task. By following the pseudocode given above, you can query the collection of close approaches to generate (with `yield`) a stream of results that match user-specified criteria.

#### Task 3c: Limit the results to at most some maximum number.

After the `main.py` script runs `.query` on the `NEODatabase` with the objects you produced in `create_filters`, it sends the stream of results through the `limit` function in the `filters` module. This is the next function that we'll write.

```
def limit(iterator, n):
    ...
```

The first argument - `iterator` - represents a stream of data, as an iterable. In our pipeline, it will be the stream of `CloseApproach`es produced by the `query` method. The second argument - `n`- represents the maximum number of elements from the stream that might be produced by the `limit` function. If `n` is `None` or zero, you shouldn't limit the results at all.

You should not treat the `iterator` argument as being an in-memory aggregate data type, such as a list or a tuple. In particular, you should not slice the `iterator` argument.

Why restrict ourselves in this way? With any sufficiently large dataset, we'd usually like to do the minimum number of operations necessary to achieve our goal. As just discussed, there are some queries for which, if we simply calculated and buffered all matching close approaches from the `query` method and sliced the result, the runtime would be just too slow. Although our data set may be small enough for the naive solution to be possible, it's still big enough to illustrate a noticeable improved performance by leveraging operations on iterators and generators.

As a hint, (although not necessary) you may find the [itertools.islice](https://docs.python.org/3/library/itertools.html#itertools.islice) function helpful.

#### Testing

It's getting a little harder to manually test your implementations.

At the command line, as you implement more and more individual filters (and their effect on `query`), you'll unlock more and more of the options of the `query` subcommand. When this task is finished, the `query` subcommand will work completely, with the exception of `--outfile`. Here are a few examples:

```
# Query for close approaches on 2020-01-01
$ python3 main.py query --date 2020-01-01

# Query for close approaches in 2020.
$ python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31

# Query for close approaches in 2020 with a distance of <=0.1 au.
$ python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --max-distance 0.1

# Query for close approaches in 2020 with a distance of >=0.3 au.
$ python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --min-distance 0.3

# Query for close approaches in 2020 with a velocity of <=50 km/s.
$ python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --max-velocity 50

# Query for close approaches in 2020 with a velocity of >=25 km/s.
$ python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --min-velocity 25

# Query for close approaches of not potentially-hazardous NEOs between 500m and 600m in diameter.
$ python3 main.py query --min-diameter 0.5 --max-diameter 0.6 --not-hazardous

# Query for close approaches of potentially-hazardous NEOs larger than 2.5km passing within 0.1 au at a speed of at least 35 km/s
# Hint: There's only one match in the whole dataset :)
$ python3 main.py query --max-distance 0.1 --min-velocity 35 --min-diameter 2.5 --hazardous
```

There are more examples at the start of this README and in the `main.py` file's module comment.

In some cases, you might want to `inspect` an NEO to check that the diameter and hazardous filters behave correctly.

Again, recall that you can use the `interactive` subcommand to load the database once and perform several `query` and `inspect` commands, which will avoid excessively waiting for your code to reload the database with each command.

Additionally, you can use the pre-written unit tests to exercise each of these steps. You can read the test files if you'd like to see exactly which test cases we use.

```
$ python3 -m unittest tests.test_query tests.test_limit
```

There are a total of 37 unit tests for this task. You can use these tests during development as well. As you implement individual filter types, you'll pass more and more of the tests.

When this task is complete, all tests should pass.

### Task 4: Report the results.

Fantastic! You've successfully written code to filter and limit the database of close approaches with user-specified criteria. So far, the results have been simply printed to standard output.

For this task, you'll implement functions in `write.py` to save these results to an output file. You'll write two functions:

- `write_to_csv`: Write a stream of `CloseApproach` objects to a specific CSV file.
- `write_to_json`: Write a stream of `CloseApproach` objects to a specific JSON file.

Each of these functions accepts two arguments: `results` and `filename`.

The `results` parameter is a stream of `CloseApproach` objects, as produced by the `limit` function. The `filename` parameter is a Path-like object with the name of the output file. You can `open(filename, 'w')` as usual.

If there are no results, then `write_to_csv` should just write a header row, and `write_to_json` should just write an empty list.

#### CSV Output Format

The `write_to_csv` method should write a stream of results to a CSV file and include a header row. Each row will represent one `CloseApproach` from the stream of `results`, and include information about the close approach as well as the associated NEO. The header columns should be: `'datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous'`.

As an example, consider the `CloseApproach` when the NEO Eros approaches Earth on 2025-11-30 02:18. For this close approach, the corresponding row would be:

```
datetime_utc,distance_au,velocity_km_s,designation,name,diameter_km,potentially_hazardous
...
2025-11-30 02:18,0.397647483265833,3.72885069167641,433,Eros,16.84,False
...
```

A missing name must be represented by the empty string (not `'None'`). A missing diameter must be represented either by the empty string or by the string `'nan'`. The `potentially_hazardous` flag should be either the string `'False'` or the string `'True'`.

#### JSON Output Format

The `write_to_json` method should write a stream of results to a JSON file. The top-level JSON object must be a list, with each entry representing one `CloseApproach` from the stream of `results`. Each entry should be a dictionary mapping the keys `'datetime_utc', 'distance_au', 'velocity_km_s'` to the associated values on the `CloseApproach` object and the key `neo` to a dictionary mapping the keys `'designation', 'name', 'diameter_km', 'potentially_hazardous'` to the associated values on the close approach's NEO.

As an example, consider the (same) `CloseApproach` when the NEO Eros approaches Earth on 2025-11-30 02:18. For this close approach, the corresponding entry would be:

```
[
  {...},
  {
    "datetime_utc": "2025-11-30 02:18",
    "distance_au": 0.397647483265833,
    "velocity_km_s": 3.72885069167641,
    "neo": {
      "designation": "433",
      "name": "Eros",
      "diameter_km": 16.84,
      "potentially_hazardous": false
    }
  },
  ...
]
```

The `datetime_utc` value should be a string formatted with `datetime_to_str` from the `helpers` module; the `distance_au` and `velocity_km_s` values should be floats; the `designation` and `name` should be strings (if the `name` is missing, it must be the empty string); the `diameter_km` should be a float (if the `diameter_km` is missing, it should be the JSON value `NaN`, which Python's `json` loader successfully rehydrates as `float('nan')`); and `potentially_hazardous` should be a boolean (i.e. the JSON literals `false` or `true`, not the strings `'False'` nor `'True'`).

#### Deduplicating Serialization

It can feel as though this output specification includes several edge cases. Fortunately, with the right design, Python's default behavior will handle these edge cases smoothly. While you are free to concretely implement these methods in any way you would like, we recommend that you add `.serialize()`methods to the `NearEarthObject` and `CloseApproach` classes that each produce a dictionary containing relevant attributes for CSV or JSON serialization. These methods can individually handle any edge cases, in a single place. For example:

```
>>> neo = NearEarthObject(...)
>>> approach = CloseApproach(...)
>>> print(neo.serialize())
{'designation': '433', 'name': 'Eros', 'diameter_km': 16.84, 'potentially_hazardous': False}
>>> print(approach.serialize())
{'datetime_utc': '2025-11-30 02:18', 'distance_au': 0.397647483265833, 'velocity_km_s': 3.72885069167641}
```

#### Testing

Congratulations! This was the final task for this project.

At this point, all of the unit tests should pass. You can run all of the unit tests:

```
$ python3 -m unittest
.........................................................................
----------------------------------------------------------------------
Ran 73 tests in 3.666s

OK
```

Heck, run it with `python3 -m unittest --verbose` to verbosely celebrate all of the test cases that you have now made pass.

Tests for this specific task are in the `tests.test_write` module.

Furthermore, the complete functional interface of the command line tool should now work. Therefore, you can now use `main.py` freely (including the --outfile argument). For example:

```
# Save (the first) five close approaches on 2020-01-01 to a CSV file.
$ python3 main.py query --date 2020-01-01 --limit 5 --outfile results.csv

# Save (the first) five close approaches on 2020-01-01 to a JSON file.
$ python3 main.py query --date 2020-01-01 --limit 5 --outfile results.json

# Putting it all together.
# Save (the first) ten close approaches between 2020-01-01 and 2020-12-31 of a potentially-hazardous NEO larger than 250m in diameter that passed within 0.1au of Earth to a JSON file.
$ python3 main.py query --start-date 2020-01-01 --end-date 2020-12-31 --hazardous --min-diameter 0.25 --max-distance 0.1 --limit 5 --outfile results.json
```

### Recap

We've reviewed a lot of information. Here's a high-level overview of the main parts of each task.

- Task 0: Inspect data. (`data/neos.csv` and `data/cad.json`)
- Task 1: Build models. (`models.py`)
  - Write `__init__` and `__str__` methods for `NearEarthObject` and `CloseApproach`
- Task 2a: Extract data. (`extract.py`)
  - Implement `load_neos` and `load_approaches` to read data from CSV and JSON files.
- Task 2b: Process data. (`database.py`)
  - Implement the constructor for `NEODatabase`, preprocessing the data to help with future queries.
  - Write methods to get NEOs by primary designation or by name.
- Task 3a: Create filters. (`filters.py`)
  - Define a hierarchy of `Filter`s.
  - Implement `create_filters` to create a collection of filters from user-specified criteria.
- Task 3b: Query matching close approaches (`database.py`)
  - Implement the `query` method to generate a stream of `CloseApproach`es that match the given filters.
- Task 3c: Limit results. (`filter.py`)
  - Write `limit` to produce only the first values from a generator.
- Task 4: Save data. (`write.py`)
  - Implement `write_to_csv` and `write_to_json` to save structured data to a formatted file.

## Development Environments

This project requires Python 3.6+. To see the version of your environment's Python 3, run `python3 -V` at the command line. You should see: `Python 3.X.Y` where X >= 6.

Fortunately, this project has no dependencies external to the Python standard library, so there's no need for virtual environments.

All of the examples use the `python3` executable. Only if your environment's `python -V` is also Python 3.6+ can you use `python` instead of `python3`.

There are two primary environments in which you might accomplish this project: (1) in a Udacity classroom workspace; (2) locally, on a machine you control.

### Udacity Workspace

Within the Udacity course, under the "Project: Exploring Near-Earth Objects" lesson, find the "Project Workspace" page and click on it. You'll be taken to a development environment with a file explorer, a code editor, and a command line. This workspace already contains all of the necessary files within the `/home/workspace` folder - you're ready to get started!

### Local Development

First, clone the project to your local machine with `git clone https://github.com/udacity/nd303-c1-advanced-python-techniques-project-starter.git`, and then navigate to the project directory (the one containing `main.py`).

### Check Your Setup

As you settle into your development environment, run the following unit tests to check that your environment is set up correctly. All of the tests should pass, even on the starter code.

```
$ python3 -m unittest --verbose tests.test_python_version
test_python_version_is_at_least_3_6 (tests.test_python_version.TestPythonVersion) ... ok

----------------------------------------------------------------------
Ran 1 test in X.XXXs

OK
$ python3 -m unittest --verbose tests.test_data_files
test_data_files_are_not_empty (tests.test_data_files.TestDataFiles) ... ok
test_data_files_are_readable (tests.test_data_files.TestDataFiles) ... ok
test_data_files_are_well_formatted (tests.test_data_files.TestDataFiles) ... ok
test_data_files_exist (tests.test_data_files.TestDataFiles) ... ok

----------------------------------------------------------------------
Ran 4 tests in X.XXXs

OK
```

If any of the tests fail, you should fix the causes of error before beginning this project.

## Deliverables

Upon completing this project, you'll have modified at least `database.py`, `extract.py`, `filters.py`, `models.py`, and `write.py`. If you went above-and-beyond with any Stand Out Suggestions, include your changes alongside an EXTENSIONS.md file describing your changes so that the reviewers can understand what you've done.

Over the course of this project (specifically, in Task 4), you've likely created several output files. You should remove these files before submitting your project.

### Rubric

In addition to the functionality requirements detailed above, your submission will be assessed on how well it follows best practices in Python. Roughly speaking, "best practices" can be divided into two categories - mechanics and design. Good Python mechanics adhere to [PEP 8](https://www.python.org/dev/peps/pep-0008/) - the style guide for Python code - and [PEP 257](https://www.python.org/dev/peps/pep-0257/) - docstring conventions. These address rules for naming, spacing, commenting, and several common programming patterns. Additionally, good general programming mechanics that you are expected to follow include removing starter code markings, removing extraneous print statements, and documenting your code. Python design refers to the higher-level organization of your code - the interfaces and implementation boundaries defined by your code objects. Many interface and implementation boundaries are already imposed by the organization of the starter code; however, there are still several situations (particularly in Tasks 3 and 4) in which the organization of your code can reflect poorly on or reflect well on the organization of the problem and your choice of solution.

Complete details on grading criteria are available in the attached rubric.
