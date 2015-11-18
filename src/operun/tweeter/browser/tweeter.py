from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage  # Error messages.  # noqa

from twitter import *  # Twitter API module.
import re  # File string handling.
import ipdb  # Debugging.

TOKEN_KEY = '3946834222-BbW0VMZ0T4RzTxkIIzcjigt5PnefIq8bRBu5IcE'
TOKEN_KEY_SECRET = 'nPfoG90sn7lAfjdCIX5GKvy1jgt53EtlpCbDL6lD1BUgG'
CONSUMER_KEY = 'AxyyP3DfR6bXb4h3PJ3at5pzJ'
CONSUMER_KEY_SECRET = 'ILBuekpLusqOd8b51lFx5hagX4chua9NB1OYDf1tk7R6RZU7Oj'


class TweeterView(BrowserView):

    template = ViewPageTemplateFile('templates/tweeter.pt')

    def __call__(self):
        self.tweet_loader = self.tweet_data()

        return self.template()

    def twitter_user(self):
        # Grabs the text input from page-template.
        form = self.request.form
        this_result = form.get('form_name', None)

        return this_result

    def tweet_count(self):
        # Get number of tweets from formula and return as integer.
        form = self.request.form
        this_result = int(form.get('tweet_count', '6'))

        return this_result

    def spawn_message(self, msg, kind):
        # Creates an error message within Plone environment.
        message = IStatusMessage(self.request)
        message.add(msg, type=kind)

    def twitter_tweet_errors(self, value):
        # For hash search.
        if len(value) and len(value) < self.tweet_count():
            self.spawn_message(
                'Search returned less than ' + str(self.tweet_count()) + ' tweets.', 'info')

        # For user search.
        if len(value) and len(value) < self.tweet_count():
            self.spawn_message(
                'User has less than ' + str(self.tweet_count()) + ' tweets or doesn\'t exist.', 'info')

        # No result error.
        if len(value) == 0:
            self.spawn_message(
                'Search returned no results.', 'warning')

    ipdb.set_trace()

    def twitter_tweets(self):
        t = Twitter(auth=OAuth(TOKEN_KEY, TOKEN_KEY_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET))  # noqa
        name = self.twitter_user()

        if name:
            if '#' in name:
                all_tweets = t.search.tweets(q="%s" % (name))
                status_tweets = all_tweets['statuses']
                tweet_list = status_tweets[:self.tweet_count()]
                self.twitter_tweet_errors(status_tweets)

                return tweet_list
            if '@' in name:
                all_tweets = t.statuses.user_timeline(screen_name='%s' % (name))  # noqa
                tweet_list = all_tweets[:self.tweet_count()]
                self.twitter_tweet_errors(all_tweets)

                return tweet_list
            else:
                all_tweets = t.statuses.user_timeline(screen_name='%s' % (name))  # noqa
                tweet_list = all_tweets[:self.tweet_count()]
                self.twitter_tweet_errors(all_tweets)

                return tweet_list
        else:
            return []

    def replace_url_to_link(self, value):
        # URL method.
        urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE | re.UNICODE)  # noqa
        value = urls.sub(r'<a href="\1" style="color: #606060;">\1</a>', value)

        # E-Mail method.
        urls = re.compile(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", re.MULTILINE | re.UNICODE)  # noqa
        value = urls.sub(r'<a href="mailto:\1">\1</a>', value)

        return value

    def replace_hashat_word_color(self, value, color):
        # Replaces words from tweeted text with user specific color styling.
        word_color = re.compile(r"([#@]\w+)", re.MULTILINE | re.UNICODE).sub(r'<span style="color: #replace_hashat_word_color">\1</span>', value)  # noqa
        word_color = word_color.replace('replace_hashat_word_color', color)

        return word_color

    def tweet_data(self):
        # Useable info from tweet data.
        data_list = []

        for tweet in self.twitter_tweets():
            user = tweet['user']
            text = tweet['text']

            # Error handling.
            if 'profile_banner_url' in user:
                profile_banner_url = user['profile_banner_url']
            else:
                profile_banner_url = ''

            if 'location' in user:
                user_location = user['location']
            else:
                user_location = ''

            # Variables to pass through page template.
            hashat_color = user['profile_link_color']
            profile_bigger = user['profile_image_url'].replace('_normal', '')
            profile_color = 'background-color:' + ' #' + hashat_color + ';'
            profile_link_color = 'color:' + ' #' + hashat_color + ';'
            profile_border_color = 'border: 1px solid #' + hashat_color + ';'

            text = self.replace_hashat_word_color(text, hashat_color)
            text = self.replace_url_to_link(text)

            tweet_dict = {
                # User tweet variables.
                'tweet_text': text,
                'user_nick': user['name'],
                'user_location': user_location,
                'user_acc_name': '@' + user['screen_name'],
                'follow_count': user['followers_count'],
                'tweets_count': user['statuses_count'],
                'following_count': user['friends_count'],
                'profile_link': 'https://twitter.com/' + user['screen_name'],
                'profile_follow_link': 'https://twitter.com/' + user['screen_name'] + '/followers',
                # User image variables.
                'background_color': user['profile_background_color'],
                'link_color': hashat_color,
                # User image link variables.
                'profile_image': profile_bigger,
                'profile_banner': profile_banner_url,
                'profile_color': profile_color,
                'profile_border_color': profile_border_color,
                'profile_link_color': profile_link_color,
            }
            data_list.append(tweet_dict)

        return data_list
