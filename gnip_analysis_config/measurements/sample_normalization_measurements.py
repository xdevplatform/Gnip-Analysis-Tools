import fileinput
from implemented_volume_normalizations import CountVolumeCountryNormalizedTerms
from CountUniqueUsersPerTerm import CountUniqueUsersPerTerm

#terms_list = []
#for line in fileinput.FileInput("./terms_to_count.txt"):
#    terms_list.append(line.strip())

terms_list = ["people","young","love"]

config_kwargs  = {
    # list of terms to count
    "terms": terms_list,
    # (only relevant for CountUniqueUsersPerTerm) if true, use HLL to count cardinality of user sets, if false, count exactly
    "hll": True,
    # (only relevant for CountUniqueUsersPerTerm) size of the HLL obj, bigger == more memory usage, more accuracy
    "hll_size": 5
    }

measurements_list = [
        CountVolumeCountryNormalizedTerms, 
        CountUniqueUsersPerTerm
        ]
