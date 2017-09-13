from .enrichment_base import BaseEnrichment

class TestEnrichment(BaseEnrichment):
    """
    This class demonstrates the use of BaseEnrichment
    """
    def enrichment_value(self,tweet):
        return 1
