import urllib.request
import datetime
import json
import time
import tweepy
import os
import random
from dotenv import load_dotenv


def update_status(status):
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    try:
        api = tweepy.API(auth)
        api.update_status(status)
        log('Tweet:', status)
    except tweepy.TweepError as error:
        log('Error: update_status: Something went wrong!', error)


def get_html(url):
    try:
        response = urllib.request.urlopen(url)
        return str(response.read())
    except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as error:
        log('Error: get_html:', error)
        return None


def get_current_booking(haystack):
    header = haystack.find('<h2 id="check-your-eligibility">1. Check Your Eligibility</h2>')
    if header == -1:
        log('Error: get_current_booking: header not found, did page html format change?')
        return None
    else:
        header_to_end = haystack[header:]
        start = '<blockquote><strong>'
        end = '</strong></blockquote>'
        booking_start = header_to_end.find(start)
        booking_end = header_to_end.find(end)
        if booking_start == -1 or booking_end == -1:
            log('Error: get_current_booking: booking not found, did page html format change?')
            return None
        else:
            booking_text = header_to_end[booking_start + len(start):booking_end]
            return booking_text


def compose_tweet(content, tweet_time, website=''):
    hashtags = '#sk #sask #GetVaccinatedSK'
    the_time = tweet_time.strftime('(%m/%d %I:%M %p CST)')
    if len(website) > 0:
        website = f'c/o: {website}'
    return f'{content} {website} {hashtags} {the_time}'


def get_previous(file_name='previous.json'):
    read_json = ''
    if os.path.exists(file_name):
        file = open(file_name, 'r')
        read_json = json.load(file)
        file.close()
    return read_json


def set_previous(data, file_name='previous.json'):
    file = open(file_name, 'w')
    write = {
        'data': data,
        'time': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    }
    file.write(json.dumps(write))
    file.close()
    log(f'{file_name} updated: {write}')

def get_last_tweet_id(account_name):
    # Default tweet_id of SaskHealth tweet from May 5, 2021
    read_json = '1390055318491582465'
    file_name = f'{account_name}.txt'
    if os.path.exists(file_name):
        file = open(file_name, 'r')
        read_json = json.load(file)
        file.close()
    return int(read_json)


def set_last_tweet_id(account_name, tweet_id):
    file_name = f'{account_name}.txt'
    file = open(file_name, 'w')
    file.write(str(tweet_id))
    file.close()
    log(f'{file_name} updated: {str(tweet_id)}')


def should_tweet(booking_info, previous, current_time):
    # check if there is a change and if we have already tweeted today
    log('should_tweet: should we tweet?')
    if previous == '':
        log('should_tweet: no previous data, we should tweet')
        return True
    else:
        previous_time = datetime.datetime.strptime(previous['time'], '%Y-%m-%dT%H:%M:%SZ')
        # is the data different than what we have stored?
        if booking_info != previous['data']:
            log(f'should_tweet: data has changed, we should tweet: {booking_info}')
            return True
        # is it after 8:01 AM CST and we haven't tweeted today?
        elif current_time.hour >= 8 and current_time.minute >= 1 and previous_time.day != current_time.day:
            log(f'should_tweet: later than 8 and have not tweeted today, we should tweet: {booking_info}')
            return True
        # we've already tweeted this info
        else:
            log(f'should_tweet: we already tweeted this data: {booking_info}')
            return False


def log(text, more_text=''):
    print(f"{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')}: {text} {more_text}")


def check_tweets():
    auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
    auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET'))

    accounts = [
        {'name': 'SaskHealth', 'id': 134198093},
        {'name': 'SKGov', 'id': 281756281}
    ]

    for account in accounts:
        try:
            api = tweepy.API(auth)
            since_id = get_last_tweet_id(account['name'])
            timeline = api.user_timeline(user_id=account['id'], since_id=int(since_id), include_rts=False, exclude_replies=False, trim_user=True, tweet_mode='extended')
            tweet_ids = []
            for t in timeline:
                tweet_ids.append(t.id)
                if should_retweet(t.full_text):
                    api.retweet(t.id)
                    log('Retweet:', t)
            tweet_ids.sort(reverse=True)
            if len(tweet_ids) > 0:
                set_last_tweet_id(account['name'], tweet_ids[0])

        except tweepy.TweepError as error:
            log('Error: dev_checktweets: Something went wrong!', error)


def should_retweet(tweet_text):
    log('should_retweet: should we retweet?')
    must_have_all = ['eligib']
    should_have_one = [
        'are now',
        'is now',
        'moves to',
        'as of',
        'remains at',
        'remains unchanged',
        'book',
    ]

    for must_have in must_have_all:
        if tweet_text.lower().find(must_have) < 0:
            log('should_retweet: no matching strings found', tweet_text)
            return False

    for should_have in should_have_one:
        if tweet_text.lower().find(should_have) >= 0:
            log('should_retweet: matches found, we should retweet', tweet_text)
            return True

    log('should_retweet: no matching strings found', tweet_text)
    return False


if __name__ == '__main__':
    log('Sask Vaccine Bot is now running...')
    load_dotenv()
    while True:
        log('Checking for updates...')
        vaccine_site = "https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility"
        html = get_html(vaccine_site)
        if html is not None:
            current_booking = get_current_booking(html)
            if current_booking is not None:
                if should_tweet(current_booking, get_previous(), datetime.datetime.now()):
                    tweet = compose_tweet(current_booking, datetime.datetime.now(), vaccine_site)
                    if tweet is not None:
                        update_status(tweet)
                        set_previous(current_booking)
                    else:
                        log('Error: main: tweet is None')
                else:
                    log("Ok, I won't tweet anything...")
            else:
                log('Error: main: current_booking is None')
        else:
            log('Error: main: html is None')
        check_tweets()
        time.sleep(random.randint(60, 120))  # wait 1 minute
