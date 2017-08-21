# before importing this enrichment, run the adjacent bash script from within an 
#   appropriate python environment in order to install all of the dependencies 
#   and download the model weights and labels. this will take a minute or two, 
#   depending on the speed of your network. 
#
# (env) $ bash image-build.sh 

from gnip_analysis_config.enrichments import enrichment_base

import logging
from io import BytesIO
import numpy as np
from PIL import Image
import requests
from keras.preprocessing import image as keras_image
from keras.applications.vgg16 import VGG16
from keras.applications.vgg16 import preprocess_input as vgg16_preprocess_input
from keras.applications.vgg16 import decode_predictions as vgg16_decode_predictions


class MyEnrichment(enrichment_base.BaseEnrichment):
    def enrichment_value(self, tweet):
        return "my_test_enrichment_value"


class ImageLabelVGG16(enrichment_base.BaseEnrichment):
    def __init__(self):
        self.model = VGG16(weights='imagenet')
        # note: topk is hard-coded for now. the model will always return 
        #   `topk` predictions, regardless of the probability score 
        self.topk = 5 

    def enrichment_value(self, tweet):
        img = self._get_image_from_tweet(tweet)
        if img:
            predictions = self._make_predictions(img, topk=self.topk)
            output = self._format_output(predictions)
        else:
            output = None
        return output

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

    def _make_predictions(self, img, topk):
        """
        Use `self.model` to generate image label predictions on `img` binary.
        This method follows the examples from the Keras image classification
        documentation. See also:
        https://keras.io/applications/#usage-examples-for-image-classification-models
        This method overlaps with keras.preprocessing.image.load_img(), but
        decouples the file read from the image resizing. See also:
        https://github.com/fchollet/keras/blob/master/keras/preprocessing/image.py

        Parameters
        ----------
        img : PIL-formatted image binary file-like object
        topk : int
            Top-`k` predictions which will be included in results

        Returns
        -------
        output : list
            Named model predictions and confidence scores
        """
        # ensure 3-channel image
        img = img.convert('RGB')
        # resize image according to model specs
        target_size = (224, 224)
        img = img.resize((target_size[1], target_size[0]))
        x = keras_image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = vgg16_preprocess_input(x)

        # models return a numpy array of predictions
        preds = self.model.predict(x)
        # lookup for translattion to named labels
        output = vgg16_decode_predictions(preds, top=topk)[0]
        return output

    def _format_output(self, predictions):
        """Make the output nice.

        Parameters
        ----------
        predictions : list
            List of top (code, description, probability) tuples from model

        Returns
        -------
        output : dict
            Organized version of predictions. List of tuples:
            (label, probability, lookup code)
        """
        # decimals aren't well json-encoded, convert to str
        output = []
        for item in predictions:
            output.append((str(item[1]), str(item[2]), str(item[0])))
        return output


image_enrichments_list = [ImageLabelVGG16]
