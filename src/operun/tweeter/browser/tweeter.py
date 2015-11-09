from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from twitter import *
import re

TOKEN_KEY = '3946834222-BbW0VMZ0T4RzTxkIIzcjigt5PnefIq8bRBu5IcE'
TOKEN_KEY_SECRET = 'nPfoG90sn7lAfjdCIX5GKvy1jgt53EtlpCbDL6lD1BUgG'
CONSUMER_KEY = 'AxyyP3DfR6bXb4h3PJ3at5pzJ'
CONSUMER_KEY_SECRET = 'ILBuekpLusqOd8b51lFx5hagX4chua9NB1OYDf1tk7R6RZU7Oj'

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

    """
    # Recompile string with link tags.

    def tweet_link_recompile(self):
        tweet_text = self.twitter_tweets()
        recompile = re.compile(r"(http://[^ ]+)")

        if recompile.endswith('.png', '.jpg'):
            return recompile.sub(r'<img src="\1">', tweet_text)
        elif:
            return recompile.sub(r'<a href="\1">\1</a>', tweet_text)
    """

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
        t = Twitter(auth=OAuth(TOKEN_KEY, TOKEN_KEY_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET))
        name = self.twitter_user()

        if name:
            all_tweets = t.statuses.user_timeline(screen_name='%s' % (name))
            tweet_list = all_tweets[:self.tweet_count()]

            return all_tweets[:self.tweet_count()]
        else:
            """
            If no name available, pass variable and wait for call.
            """
            pass
