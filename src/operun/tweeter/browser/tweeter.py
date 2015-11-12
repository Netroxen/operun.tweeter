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
        #Get number of tweets from formula and return as integer.
        form = self.request.form
        this_result = int(form.get('tweet_count', '6'))

        return this_result

    def twitter_tweets(self):
        t = Twitter(auth=OAuth(TOKEN_KEY, TOKEN_KEY_SECRET, CONSUMER_KEY, CONSUMER_KEY_SECRET))
        name = self.twitter_user()

        if name:
            if '#' in name:
                all_tweets = t.search.tweets(q="%s" % (name))
                status_tweets = all_tweets['statuses']
                tweet_list = status_tweets[:self.tweet_count()]

                return tweet_list
            if '@' in name:
                all_tweets = t.statuses.user_timeline(screen_name='%s' % (name))
                tweet_list = all_tweets[:self.tweet_count()]

                return tweet_list
            else:
                all_tweets = t.statuses.user_timeline(screen_name='%s' % (name))
                tweet_list = all_tweets[:self.tweet_count()]

                return tweet_list
        else:
            return []

    def replace_url_to_link(self, value):
        #URL method.
        urls = re.compile(r"((https?):((//)|(\\\\))+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE|re.UNICODE)
        value = urls.sub(r'<a href="\1">\1</a>', value)

        #E-Mail method.
        urls = re.compile(r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)", re.MULTILINE|re.UNICODE)
        value = urls.sub(r'<a href="mailto:\1">\1</a>', value)

        return value

    def replace_hash_word_col(self, value):
        value = re.findall(r'#\w*', value)

        return value

    def tweet_data(self):
        #Useable info from tweet data.
        data_list = []

        for tweet in self.twitter_tweets():
            user = tweet['user']

            #Error handling.
            if 'profile_banner_url' in user:
                profile_banner_url = user['profile_banner_url']
            else:
                profile_banner_url = ''

            if 'location' in user:
                user_location = user['location']
            else:
                user_location = ''

            #Variables to pass through page template.
            profile_bigger = user['profile_image_url'].replace('_normal', '')
            profile_color = 'background-color:' + ' #' + user['profile_link_color'] + ';'
            profile_border_color = 'border: 1px solid #' + user['profile_link_color'] + ';'
            profile_link_color = 'color:' + ' #' + user['profile_link_color'] + ';'

            tweet_dict = {
            #User tweet variables.
            'tweet_text': tweet['text'], #self.replace_url_to_link(tweet['text'])
            'user_nick': user['name'],
            'user_location': user_location,
            'user_acc_name': '@' + user['screen_name'],
            'follow_count': user['followers_count'],
            'profile_link': 'https://twitter.com/' + user['screen_name'],
            'profile_follow_link': 'https://twitter.com/' + user['screen_name'] + '/following',
            #User image variables.
            'background_color': user['profile_background_color'],
            'link_color': user['profile_link_color'],
            #User image link variables.
            'profile_image': profile_bigger,
            'profile_banner': profile_banner_url,
            'profile_color': profile_color,
            'profile_border_color': profile_border_color,
            'profile_link_color': profile_link_color,
            }
            data_list.append(tweet_dict)

        return data_list
