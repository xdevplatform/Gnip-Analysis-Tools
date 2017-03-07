import fileinput
from gnip_analysis_config.measurements.measurement_base import MeasurementBase, TokenizedBody

class CountVolumeNormalizedTerms(MeasurementBase, TokenizedBody):
    """
    create time series of term volumes normalized 
    by platform volume by country
    """
    def __init__(self, **kwargs):
        """initialize the measurement object"""
        super().__init__(**kwargs)
        # the terms that we want to track are in self.terms
        # get the outside information about decahose volumes that we will normalize by
        datekey_fp = self._datekey[0:4]+"/"+self._datekey[4:6]+"/"+self._datekey[6:8]
        self.normalizing_volumes = self.get_normalization_info(datekey_fp)
        # initialize the dictionary where we will store term volume by category
        self.token_volumes_by_category = {}
        for category in self.normalizing_volumes:
            self.token_volumes_by_category[category] = {k:0 for k in self.terms}
    def update(self,tweet):
        """add a Tweet to the measurement"""
        # count the tokens in the Tweet
        # for each token, augment the appropriate counter
        for token in self.get_tokens(tweet):
            if token in self.terms:
                category = self.get_category_key(tweet)
                # if that category is not in self.token_volumes_by_categroy, it isn't recorded
                if category in self.token_volumes_by_category:
                    self.token_volumes_by_category[category][token] += 1
                self.token_volumes_by_category["total"][token] += 1
    def combine(self,new_counters):
        """combine two CountVolumeNormalizedTerms objects"""
        for new_catagory,new_category_dict in new_counters.token_volumes_by_category.items():
            if new_category in self.token_volumes_by_category:
                for new_category,new_count in new_counters.items():
                    if new_token in self.token_volumes_by_category[new_category]:
                        self.token_volumes_by_category[new_category][new_token] += new_count
                    else:
                        self.token_volumes_by_category[new_category][new_token] = new_count
            else:
                self.token_volumes_by_category[new_category] = new_category_dict
    def get(self):
        """return time series for each category, 
           scaled by that category volume in the decahose"""
        # I want the results to be ~O(1), so lets come up with a scaling const for all of them
        # scaling const = normalizing_volumes[total]/token_volumes_by_category[total]
        total_norm_vols = self.normalizing_volumes["total"]
        total_all_tokens = sum(self.token_volumes_by_category["total"].values())
        results = []
        for category in self.token_volumes_by_category:
            category_vol = self.normalizing_volumes[category]
            for token in self.token_volumes_by_category[category]:
                count = self.token_volumes_by_category[category][token]
                name = token + "/" + category + "*" + str(total_norm_vols) + "/" + str(total_all_tokens)
                if category_vol == 0:
                    results.append((0.0, name))
                else:
                    results.append(((count*total_norm_vols)/(category_vol*total_all_tokens), name))
        return results
    def get_normalization_info(self,date_key):
        raise NotImplementedError
    def get_category_key(self,tweet):
        raise NotImplementedError
        
