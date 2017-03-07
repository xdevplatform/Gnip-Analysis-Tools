import fileinput
from HLL import HyperLogLog
from gnip_analysis_config.measurements.measurement_base import MeasurementBase, TokenizedBody

class CountUniqueUsersPerTerm(MeasurementBase, TokenizedBody):
    """
    create time series of the number of unique users
    Tweeting a term by unit time
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # create a private _set class that defines the same API for interacting with
        # sets and HLL objects
        if self.hll:
            hll_size = self.hll_size
            class _set(HyperLogLog):
                def __init__(self):
                    super().__init__(hll_size)
                def update(self,elements):
                    for element in elements:
                        self.add(element)
                def size(self):
                    return round(self.cardinality(),3)
        else:
            class _set(set):
                def size(self):
                    return len(self)
                def merge(self,new_set):
                    self.update(new_set)
        # get the list of terms to count
        self.users_per_term = {}
        for term in self.terms:
            self.users_per_term[term] = _set()
    def update(self,tweet):
        # check if a term is in the list of terms to count
        # if it is, add the Tweeting user to the appropriate counter
        for token in self.get_tokens(tweet):
            if token in self.users_per_term:
                self.users_per_term[token].update([tweet["actor"]["id"].split(":")[-1]]) 
    def get(self):
        # return the counts/approximations from each HLL thing
        return [(user_set.size(), "unique users tweeting '" + name + "'") for name, user_set in self.users_per_term.items()]
    def combine(self,new_counters):
        # combine the objects
        for key in new_counters.users_per_term:
            if key in self.users_per_term:
                self.users_per_term[key].merge(new_counters.users_per_term[key])

