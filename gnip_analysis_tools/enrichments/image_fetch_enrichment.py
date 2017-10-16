import logging

from io import BytesIO
from PIL import Image
import requests
import jsonpickle

from gnip_analysis_tools.enrichments import enrichment_base

class GetImage(enrichment_base.BaseEnrichment):

    def _get_image_from_tweet(self, tweet):
        """
        Extract an image file from the URL in a given Tweet.

        Parameters
        ----------
        tweet : dict
            Tweet in JSON-formatted dict structure

        Returns
        -------
        image
            PIL-formatted image file (or None)
        """
        image = None
        img_url = self._get_img_url(tweet)
        if img_url:
            image = self._download_image(img_url)
        else:
            logging.info('failed to get image for tweet id={}'.format(tweet['id'])) 
        return image

    def _get_img_url(self, tweet):
        """
        Helper function to extract an image URL (or None) from a Tweet.
        Currently supports only Activity Streams format. Handles (potential non-)
            existance of relevant payload elements.

        Parameters
        ----------
        tweet : dict
            Tweet in JSON-formatted dict structure
        Returns
        -------
        url : str
            String URL to image location (on twitter.com server) (or None)
        """
        media_url = None
        if 'twitter_entities' not in tweet or 'media' not in tweet['twitter_entities']:
            logging.info('no image found in tweet id={}'.format(tweet['id']))
            return media_url
        try:
            media_url = tweet['twitter_entities']['media'][0]['media_url']
        except KeyError:
            logging.info('Failed to extract image URL for tweet id={}'.format(tweet['id']))
        return media_url

    def _download_image(self, img_url):
        """
        Download the image located at the given URL. This method overlaps with
        keras.preprocessing.image.load_img(), but does not look to a local file
        path. See also:
        https://github.com/fchollet/keras/blob/master/keras/preprocessing/image.py

        Parameters
        ----------
        img_url : str
            String URL to location of image.

        Returns
        -------
        image
            PIL-formatted image file (or None)
        """
        image = None
        response = requests.get(img_url)
        # convert binary data to PIL.Image
        if response.ok:
            image = Image.open(BytesIO(response.content))
        else:
            logging.info('HTTP error={} for URL={}'.format(response.status_code, img_url))
        return image
    
    def enrichment_value(self, tweet):
        image_obj = self._get_image_from_tweet(tweet)  
        return image_obj

class GetImageJSON(GetImage):
    
    def enrichment_value(self, tweet):
        image_obj = self._get_image_from_tweet(tweet)  
        return jsonpickle.dumps(image_obj)

