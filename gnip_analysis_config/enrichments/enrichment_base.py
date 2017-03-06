class GenericModelEnrichment(object):
    """
    An enrichment base class for a generic model.
    Derived classes need only define a constructor that
    points the 'model' attribute to a model object.
    This object must have an 'evaluate' method
    that acts on a Tweet dictionary.

    """
    def enrich(self,tweet): 
        """ this function is called by tweet_enricher.py"""
        enrichment_value = self.model.evaluate(tweet) 
        if "enrichments" not in tweet:
            tweet['enrichments'] = {}
        tweet['enrichments'][self.__class__.__name__] = enrichment_value


class BaseEnrichment(object):
    """ 
    A simple enrichment base class that does not
    require a 'model' attribute, as in GenericModelEnrichment.
    Enrichment classes derived from this class 
    must implement the function 'enrichment value', which
    accepts a tweet dictionary as the single argument, and
    returns the enrichment value. This value must be JSON-
    serializable.
    """
    def enrich(self,tweet):
        """ this function is called by tweet_enricher.py"""
        if "enrichments" not in tweet:
            tweet['enrichments'] = {}
        tweet['enrichments'][self.__class__.__name__] = self.enrichment_value(tweet)


