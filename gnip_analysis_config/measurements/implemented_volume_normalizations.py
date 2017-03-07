from datetime import datetime
import fileinput
import os
from gnip_analysis_config.measurements.CountVolumeNormalizedTerms import CountVolumeNormalizedTerms   

class CountVolumeCountryNormalizedTerms(CountVolumeNormalizedTerms):
    # helper functions 
    def get_normalization_info(self,date_key):
        """
        grab the decahose counts normalization info
        keys of the returned dict are categories; should also include a 'total' category
        """
        # the date_key == the filepath
        decahose_info = "/home/fiona/Gnip-Analysis-Tools/decahose/" + date_key + "/"
        # grab the first line of the country summary files
        summary_files = [x for x in os.listdir(decahose_info) if "summary." in x and len(x) > 13]
        country_volumes = {}
        for summary_file in summary_files:
            with open(decahose_info + summary_file , "r") as f:
                first_line = f.readline()
                country_volumes[summary_file.split(".")[1]] = int(first_line.split(" ")[0])
        # now get the "other" volume category
        with open(decahose_info + "counts.txt", "r") as f:
            first_line = f.readline()
            country_volumes["total"] = int(first_line.split(" ")[0])
        # get the "other" category
        all_countries = 0
        for key in country_volumes:
            if key != "total":
                all_countries += country_volumes[key]
        country_volumes["other"] = country_volumes["total"] - all_countries 
        return country_volumes
    
    def get_category_key(self,tweet):
        """
        input: a Tweet dictionary
        output: a single hashable type category label 
                must correspond to normalizing info categories
        """
        try:
            return tweet["gnip"]["profileLocations"][0]["address"]["countryCode"]
        except KeyError:
            return "_other"
