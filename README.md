# The `gnip_analysis_tools` Package

This package provides useful class definitions for configuring scripts in the
[Gnip-Analysis-Pipeline](https://github.com/tw-ddis/Gnip-Analysis-Pipeline) package.
The intention is that you work from a working directory (we'll call this "TEST"), and that 
both `gnip_analysis_pipeline` and `gnip_analysis_tools` are installed as packages.
Remember that these packages can be installed from the cloned repo location with:

```bash
[REPO] $ pip install -e .
```

## Enrichments

According to the Gnip-Analysis-Pipeline 
[docs](https://github.com/tw-ddis/Gnip-Analysis-Pipeline/blob/master/README.md), 
we configure enrichments by defining
the `enrichment_class_list` variable in a configuration file.

The `enrichments` directory in this package contains files that define a base enrichment class along with
some other helpful enrichment classes, including a simple example. To use the test enrichment
from your working directory, you would create an enrichments configuration file 
(called `my_enrichments.py`):

```python

from gnip_analysis_tools.enrichments import test_enrichment

parallel_factor = 1
enrichment_class_list = [(test_enrichment.TestEnrichment,parallel_factor)]
```

We can the enrich the Tweets in `my_tweets.json` as follows:

```bash

[TEST] $ cat my_tweets.json | tweet_enricher.py -c my_enrichments.py > my_enriched_tweets.json

```

To configure an NLP enrichment with NLTK, we provide `nltk_enrichment.py`, which can be configured like:

```python

from gnip_analysis_tools.enrichments import nltk_enrichment

enrichment_class_list = nltk_enrichment.nltk_enrichments_list
```

Notice that this module has conveniently defined the list of enrichment classes.

A custom enrichment class can be defined locally:

```python

from gnip_analysis_tools.enrichments import base_enrichment

class MyEnrichment(enrichment_base.BaseEnrichment):
    def enrichment_value(self,tweet):
        return "my_test_enrichment_value"

parallel_factor = 1
enrichment_class_list = [(MyEnrichment,parallel_factor)] 
```

## Measurements

According to the Gnip-Analysis-Pipeline 
[docs](https://github.com/tw-ddis/Gnip-Analysis-Pipeline/blob/master/README.md), 
we configure measurementss by defining
the `measurements_class_list` variable in a configuration file.

The `measurements` directory in this package contains files that contain a variety of base/helper 
classes for construction measurement classes. To use the test measurement
from your working directory, you would create an enrichments configuration file 
(called `my_measurements.py`):

```python

from gnip_analysis_tools.measurements.test_measurements import TweetCounter,ReTweetCounter

measurement_class_list = [TweetCounter,ReTweetCounter]
```

We can the build time series from the Tweets in `my_enriched_tweets.json` as follows:

```bash

[TEST] $ cat my_enriched_tweets.json | tweet_time_series_builder.py -c my_measurements.py > time_series.csv

```

(Note that none of the enrichments we added in the previous section 
are required to build the specified time series.)

To construct a time series for each observed hashtag, we can define a class locally that inherits
key functionality from classes in `measurement_base.py`:

```python

from gnip_analysis_tools.measurements.measurement_base import Counters

class HashtagCounters(Counters):
    def update(self,tweet):
        for item in tweet['twitter_entities']['hashtags']:
        # put a # in from of the term,
        # since they've been removed in the payload
        self.counters['#'+item['text']] += 1

measurement_class_list = [ HashtagCounters ]
```

See `measurement_base.py` for a full description of how to create custom measurement classes. 

