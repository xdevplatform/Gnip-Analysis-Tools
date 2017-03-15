import fileinput
from gnip_analysis_config.measurements.implemented_volume_normalizations import CountVolumeCountryNormalizedTerms
from gnip_analysis_config.measurements.CountUniqueUsersPerTerm import CountUniqueUsersPerTerm

#terms_list = []
#for line in fileinput.FileInput("./terms_to_count.txt"):
#    terms_list.append(line.strip())

terms_list = ["people","young","love"]

config_kwargs  = {
    # list of terms to count
    "terms": terms_list,
    # (only relevant for CountVolumeNormalizedTerms-derived classes)
    # diving the count of the word "love" by the count of all Tweets can result in an extremely small number
    # if you like, multiply the result by a constant factor to avoid results on the order 10^-6
    # if not, it will be "1" (no multiplier on the result)
    "constant_multiplier": 1000000,
    # (only relevant for CountUniqueUsersPerTerm) 
    # if true, use HLL to count cardinality of user sets, if false, count exactly
    "hll": True,
    # (only relevant for CountUniqueUsersPerTerm) 
    # size of the HLL obj, bigger == more memory usage, more accuracy
    "hll_size": 5
    }

measurement_class_list = [
        CountVolumeCountryNormalizedTerms, 
        CountUniqueUsersPerTerm
        ]
