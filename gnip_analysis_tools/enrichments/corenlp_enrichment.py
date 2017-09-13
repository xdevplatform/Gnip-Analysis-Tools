from .enrichments import BaseEnrichment
from pycorenlp import StanfordCoreNLP

nlp = StanfordCoreNLP('http://localhost:9000')

class TokenizeBody(BaseEnrichment):
    """Use the NLTK SpaceTokenizer to parse the Tweet body."""
    def __init__(self):
        self.tokenizer = SpaceTokenizer()
    def enrichment_value(self,tweet):
        return self.tokenizer.tokenize(tweet['body'])


corenlp_enrichments_list = [
        NLTKSpaceTokenizeBody,
        ]
