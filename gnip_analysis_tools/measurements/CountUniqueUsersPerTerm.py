import fileinput
from HLL import HyperLogLog
from gnip_analysis_tools.measurements.measurement_base import MeasurementBase, TokenizedBody

# have to define these at the top level of the module, so that they will be pickleable
# create a private _set or _HyperLogLog class that defines the same API for interacting
# with sets and HLL objects
class _HyperLogLog(HyperLogLog):
    def update(self,elements):
        for element in elements:
            self.add(element)
    def count(self):
        return round(self.cardinality(),3)
class _set(set):
    def count(self):
        return len(self)
    def merge(self,new_set):
        self.update(new_set)

class CountUniqueUsersPerTerm(MeasurementBase, TokenizedBody):
    """
    create time series of the number of unique users
    Tweeting a term by unit time
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # get the list of terms to count
        self.users_per_term = {}
        if self.hll:
            for term in self.terms:
                self.users_per_term[term] = _HyperLogLog(self.hll_size)
        else:
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
        return [(user_set.count(), "unique users tweeting '" + name + "'") 
                for name, user_set in self.users_per_term.items()]
    def combine(self,new_counters):
        # combine the objects
        for key in new_counters.users_per_term:
            if key in self.users_per_term:
                self.users_per_term[key].merge(new_counters.users_per_term[key])
