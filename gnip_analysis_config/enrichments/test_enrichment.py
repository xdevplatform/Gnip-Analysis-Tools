from .enrichments import BaseEnrichment

class TestEnrichment(BaseEnrichment):
    def enrichment_value(self,tweet):
        return 1
