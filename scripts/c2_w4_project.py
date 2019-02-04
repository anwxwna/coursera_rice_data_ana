"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
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
            if keyfield.capitalize() in row:
                
                rowid = row[keyfield.capitalize()]
                table[rowid] = row
            elif keyfield.lower() in row:
                rowid = row[keyfield.lower()]
                table[rowid] = row
            elif keyfield.upper() in row:
                rowid = row[keyfield.upper()]
                table[rowid] = row
            elif 'Country' in row:
                rowid = row['Country']
                table[rowid] = row
            elif 'Country Name' in row:
                rowid = row['Country Name']
                table[rowid] = row
    
    return table

def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    table=read_csv_as_nested_dict(codeinfo['codefile'],
                                  'name',
                                  codeinfo['separator'],
                                  codeinfo['quote'])
    plot_to_gdp={}
    for country in table:
        plot_to_gdp[table[country][codeinfo['plot_codes']]]=table[country][codeinfo['data_codes']]
#    print(plot_to_gdp)
    return plot_to_gdp


def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    rec_plots={}
    plot_set=set()
    conv_plot_gdpc=build_country_code_converter(codeinfo)
    
#    plot_countries =  {k.upper(): v for k, v in plot_countries.items()}
    for ccode in plot_countries:
        if ccode.upper() in plot_countries:
            
            if ccode.upper() in conv_plot_gdpc:
                ccode=ccode.upper()
                if conv_plot_gdpc[ccode] in gdp_countries:
                    rec_plots[ccode]=conv_plot_gdpc[ccode]
                else:
                    plot_set.add(ccode.upper())
            elif ccode.lower() in conv_plot_gdpc:
                ccode=ccode.lower()
                if conv_plot_gdpc[ccode] in gdp_countries:
                    rec_plots[ccode]=conv_plot_gdpc[ccode]
                else:
                    plot_set.add(ccode.upper())
            else:
                plot_set.add(ccode.upper())
            rec_plots =  {k.upper(): v for k, v in rec_plots.items()}
        elif ccode.lower() in plot_countries:
            
            if ccode.upper() in conv_plot_gdpc:
                ccode=ccode.upper()
                if conv_plot_gdpc[ccode] in gdp_countries:
                    rec_plots[ccode]=conv_plot_gdpc[ccode]
                else:
                    plot_set.add(ccode.lower())
            elif ccode.lower() in conv_plot_gdpc:
                ccode=ccode.lower()
                if conv_plot_gdpc[ccode] in gdp_countries:
                    rec_plots[ccode]=conv_plot_gdpc[ccode]
                else:
                    plot_set.add(ccode.lower())
            else:
                plot_set.add(ccode.lower())
            rec_plots =  {k.lower(): v for k, v in rec_plots.items()}
        
#    print(rec_plots,plot_set)
    return rec_plots, plot_set


def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

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
    
    gdpdata1=read_csv_as_nested_dict(gdpinfo['gdpfile'], gdpinfo['country_code'],
                            gdpinfo['separator'],gdpinfo['quote'])
    key_yrs=list(range(gdpinfo['min_year'],(gdpinfo['max_year']+1)))
    gdpdata={}    
    for ccode in gdpdata1:
        gdpdata[ccode]={k: gdpdata1[ccode][str(k)] for k in key_yrs}
#    print(gdpdata)
        
    rec_plots,plot_set=reconcile_countries_by_code(codeinfo, plot_countries, gdpdata)
    conv_plot_gdpc=build_country_code_converter(codeinfo)
#    plot_countries =  {k.upper(): v for k, v in plot_countries.items()}
    for ccode in plot_countries:
        if ccode.lower() in plot_countries:
#            print('entered lower plot')
            ccode=ccode.lower()
            if conv_plot_gdpc[ccode] in gdpdata:
                ccode=ccode.lower()
                if gdpdata[rec_plots[ccode]][int(year)] != '':
                    cc_gdp[ccode]=math.log10(float(gdpdata[rec_plots[ccode]][int(year)]))
                    print(cc_gdp)
                else:
                    set1.add(ccode.lower())
#        ccode=ccode.lower()
        elif ccode.upper() in plot_countries:
#            print('entered upper plot')
            if ccode.upper() in conv_plot_gdpc:
                ccode=ccode.upper()
                if conv_plot_gdpc[ccode] in gdpdata:
    #                ccode=ccode.lower()
                    if gdpdata[rec_plots[ccode]][int(year)] != '':
                        cc_gdp[ccode]=math.log10(float(gdpdata[rec_plots[ccode]][int(year)]))
                        print(cc_gdp)
                    else:
                        set1.add(ccode.upper())
            elif ccode.lower() in conv_plot_gdpc:
                ccode=ccode.lower()
                if conv_plot_gdpc[ccode] in gdpdata:
                    ccode=ccode.upper()
                    if gdpdata[rec_plots[ccode]][int(year)] != '':
                        cc_gdp[ccode]=math.log10(float(gdpdata[rec_plots[ccode]][int(year)]))
                        print(cc_gdp)
                    else:
                        set1.add(ccode.lower())
        else:
            set2.add(ccode)
#    print(cc_gdp, plot_set, set1)
    return cc_gdp, plot_set, set1


def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    cc_gdp, set1, set2=build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)
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
    Test the project code for several years
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

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

#test_render_world_map()


