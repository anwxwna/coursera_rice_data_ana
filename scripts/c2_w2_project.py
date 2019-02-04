"""
Project for Week 2 of "Python Data Visualization".
Read World Bank GDP data and create some basic XY plots.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import pygal

#from pylab import plot, title, xlabel, ylabel, savefig, legend, array
#from matplotlib import pyplot as plt
#import ast
#import json


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
    tuplist=sorted(tuplist, key= lambda x:x[0])
    return tuplist


def build_plot_dict(gdpinfo, country_list):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names

    Output:
      Returns a dictionary whose keys are the country names in
      country_list and whose values are lists of XY plot values 
      computed from the CSV file described by gdpinfo.

      Countries from country_list that do not appear in the
      CSV file should still be in the output dictionary, but
      with an empty XY plot value list.
    """
    country_dict=read_csv_as_nested_dict(gdpinfo['gdpfile'], 
                                         gdpinfo['country_name'] , 
                                         gdpinfo['separator'],
                                         gdpinfo['quote'])

    key_yrs=list(range(gdpinfo['min_year'],(gdpinfo['max_year']+1)))

    country_dict_yrs={}
    
    for country in country_dict:
        country_dict_yrs[country]={k: country_dict[country][str(k)] for k in key_yrs}

    
    plot_values={}
    for country in country_dict_yrs:
        plot_values[country]=build_plot_values(gdpinfo,country_dict_yrs[country])
        
    plot_dict={}
    for country in country_list:

        if country in country_dict_yrs.keys():
            plot_dict[country]=plot_values[country]

        else:
            plot_dict[country]=[]

    return plot_dict


def render_xy_plot(gdpinfo, country_list, plot_file):
    """
    Inputs:
      gdpinfo      - GDP data information dictionary
      country_list - List of strings that are country names
      plot_file    - String that is the output plot file name

    Output:
      Returns None.

    Action:
      Creates an SVG image of an XY plot for the GDP data
      specified by gdpinfo for the countries in country_list.
      The image will be stored in a file named by plot_file.
    """
    plot_dict=build_plot_dict(gdpinfo, country_list)
    for country in country_list:
        xy_chart=pygal.XY()
        xy_chart.title='GDP DATA'
        xy_chart.add(country, *zip(*plot_dict[country]))
    xy_chart.render()
    xy_chart.render_to_file(plot_file)
    
#        plt.plot(*zip(*plot_dict[country]),label=country)
#        plt.xlabel('Years')
#        plt.ylabel('GDP in current US Dollars')

#    plt.savefig(plot_file)
    return


def test_render_xy_plot():
    """
    Code to exercise render_xy_plot and generate plots from
    actual GDP data.
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

    render_xy_plot(gdpinfo, [], "isp_gdp_xy_none.svg")
    render_xy_plot(gdpinfo, ["China"], "isp_gdp_xy_china.svg")
    render_xy_plot(gdpinfo, ["United Kingdom", "United States"],
                   "isp_gdp_xy_uk+usa.svg")


# Make sure the following call to test_render_xy_plot is commented out
# when submitting to OwlTest/CourseraTest.

#test_render_xy_plot()

#gdpinfo = {
#        "gdpfile": "isp_gdp.csv",
#        "separator": ",",
#        "quote": '"',
#        "min_year": 1960,
#        "max_year": 2015,
#        "country_name": "Country Name",
#        "country_code": "Country Code"
#    }
#
#country_list=['Armenia','France','China','India','Pakistan']
#plot_dict=build_plot_dict(gdpinfo, country_list)
#for country in country_list:


