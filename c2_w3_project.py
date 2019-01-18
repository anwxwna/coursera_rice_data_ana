"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.
"""
import csv
import math
import pygal


#import pygal.maps.world

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    
    return table

def build_plot_values(gdpinfo, gdpdata):
    """
    Inputs:
      gdpinfo - GDP data information dictionary
      gdpdata - A single country's GDP stored in a dictionary whose
                keys are strings indicating a year and whose values
                are strings indicating the country's corresponding GDP
                for that year.

    Output: 
      Returns a list of tuples of the form (year, GDP) for the years
      between "min_year" and "max_year", inclusive, from gdpinfo that
      exist in gdpdata.  The year will be an integer and the GDP will
      be a float.
    """
    keysyrs=sorted(gdpdata.keys())
    tuplist1=[(k, gdpdata[k]) for k in keysyrs if int(k)>= gdpinfo['min_year'] and 
              int(k)<=gdpinfo['max_year']]
    tuplist=[(int(k[0]),float(k[1])) for k in tuplist1 if k[1] != '']
    return tuplist

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    rec_plots={}
    plot_set=set()
    for ccode in plot_countries:
        if plot_countries[ccode] in gdp_countries:
            rec_plots[ccode]=plot_countries[ccode]
        else:
            plot_set.add(ccode)
    return rec_plots, plot_set


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    cc_gdp={}
    set1=set()
    set2=set()
    
    gdpdata1=read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo['country_name'],
                            gdpinfo['separator'],gdpinfo['quote'])
    key_yrs=list(range(gdpinfo['min_year'],(gdpinfo['max_year']+1)))
    gdpdata={}    
    for country in gdpdata1:
        gdpdata[country]={k: gdpdata1[country][str(k)] for k in key_yrs}
#    print(gdpdata)
        
    rec_plots,plot_set=reconcile_countries_by_name(plot_countries, gdpdata)
    
    for ccode in plot_countries:
        if plot_countries[ccode] in gdpdata:
            if gdpdata[rec_plots[ccode]][int(year)] != '':
                cc_gdp[ccode]=math.log10(float(gdpdata[rec_plots[ccode]][int(year)]))
            else:
                set1.add(ccode)
        else:
            set2.add(ccode)
            
    
    return cc_gdp, set2, set1


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    cc_gdp, set1, set2=build_map_dict_by_name(gdpinfo, plot_countries, year)
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title="GDP of Countries in Log scale"
    worldmap_chart.add(year,cc_gdp )
    worldmap_chart.add("Missing From World Bank Data",set1)
    worldmap_chart.add("GDP Data Missing",set2)
    worldmap_chart.render()
    worldmap_chart.render_to_file(map_file)
    

    return


def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

#test_render_world_map()

build_plot_dict({'gdpfile': 'gdptable3.csv', 'max_year': 20017, 
                 'country_name': 'ID', 'quote': "'", 
                 'country_code': 'CC', 'separator': ';', 'min_year': 20010}, 
                    ['A 5 '])