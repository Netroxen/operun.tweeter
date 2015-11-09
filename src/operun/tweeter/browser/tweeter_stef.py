from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from twitter import *
import re

TOKEN_KEY = '137801279-8MHnU3G6TD4M4Gpg2AoTSbUeP2bPMNub9X17nfCe'
TOKEN_KEY_SECRET = 'Ss1PU6Z5A7Ni1UjTegiNrG0oywF2mF30ChNhCN8xtlBUC'
CONSUMER_KEY = 'KVaBDUyINB6guHwvhKRxUg'
CONSUMER_KEY_SECRET = 'GGbEWYUqQQAgAOpmZFzBgqA9YgZ23P5s5lhI5Uv1Hdc'

class TweeterView(BrowserView):

    template = ViewPageTemplateFile('templates/tweeter.pt')

    def __call__(self):
        return self.template()

    def twitter_user(self):
        form = self.request.form
        this_result = form.get('form_name', None)

        return this_result

    def tweet_count(self):
        """
        Get number of tweets from formula and return as integer.
        """
        form = self.request.form
        this_result = int(form.get('tweet_count', '5'))

        return this_result

    def tweet_dict(self):
        """
        Take tweets and append to dictionary,
        also increase value by '1' if already present.
        """
        tweet_d = {}

        for tweet in self.twitter_tweets():
            if not tweet in tweet_d:
                tweet_d[tweet] = 1
            else:
                tweet_d[tweet] += 1

    def twitter_tweets(self):
        """
        fetch tweets from twitter and return them
        """
        t = Twitter(auth=OAuth(TOKEN_KEY, TOKEN_KEY_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET))
        name = self.twitter_user()

        if name:
            all_tweets = t.statuses.user_timeline(screen_name='%s' % (name))
            tweets = all_tweets[:self.tweet_count()]
            return tweets
        else:
            return []

    def rip_operun(self, string):
        """
        get string and remove operun
        """
        new_string = string.replace('operun', 'purpix')
        return new_string

    def tweets_data(self):
        """
        return dictionary with tweets data
        """
        tweets_data = []
        for tweet in self.twitter_tweets():
            twitter_user = tweet['user']

            style_tag = 'margin-bottom: 20px; background-color: #' + twitter_user['profile_background_color']

            data = {
                    'id':tweet['id'],
                    'user_name': self.rip_operun(twitter_user['name']),
                    'user_image': twitter_user['profile_image_url'],
                    'user_bg_color': style_tag,
                    'text':tweet['text']
                    }
            tweets_data.append(data)

        return tweets_data
