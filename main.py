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


def get_string_between(haystack, start, end, trim):
    string_start = haystack.find(start)
    if string_start == -1:
        log('Error: get_current_booking: start not found, did page html format change?')
        return None
    else:
        smaller_haystack = haystack[string_start:]
        string_end = smaller_haystack.find(end)
        if string_start == -1 or string_end == -1:
            log('Error: get_current_booking: booking not found, did page html format change?')
            return None
        else:
            string_return = smaller_haystack[trim:string_end]
            return string_return


def compose_tweet(first, second, tweet_time, website=''):
    # compose tweet text and ensure it is under 280 characters
    # note that twitter changes URLs to make them 26 char count always
    # also we need to use a time stamp, so we don't get flagged a duplicate tweet

    hashtags = '#sk #sask #GetVaccinatedSK'
    the_time = tweet_time.strftime('%m/%d %I:%M %p CST')
    short = first.replace('(online and call centre booking available).', '')

    # check if second has content and add line breaks
    if second is None or second == '':
        second = ''
    else:
        second = f'\n\n{second}'

    # list of possible tweets in order of preference
    possible_tweets = [
        f'{first}{second}\n\n{hashtags} {the_time}',
        f'{short}{second}\n\n{hashtags} {the_time}',
        f'{short}{second}\n\n{the_time}',
        f'{first}\n\n{hashtags} {the_time}',
        f'{first}\n\n{the_time}',
        f'{short}\n\n{the_time}',
    ]

    for each_tweet in possible_tweets:
        #  253 = 280 - 1 space - 26 char URL
        if len(each_tweet) < 253:
            return each_tweet + ' ' + website

    print('compose_tweet: all options are over 280 characters')
    return None


def get_previous(file_name='previous.json'):
    read_json = ''
    if os.path.exists(file_name):
        file = open(file_name, 'r')
        read_json = json.load(file)
        file.close()
    return read_json


def set_previous(first, second, file_name='previous.json'):
    file = open(file_name, 'w')
    write = {
        'first': first,
        'second': second,
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


def should_tweet(first_info, second_info, previous, current_time):
    # check if there is a change and if we have already tweeted today
    log('should_tweet: should we tweet?')
    if previous == '':
        log('should_tweet: no previous data, we should tweet')
        return True
    else:
        previous_time = datetime.datetime.strptime(previous['time'], '%Y-%m-%dT%H:%M:%SZ')
        # is the data different than what we have stored?
        if first_info != previous['first'] or second_info != previous['second']:
            log(f'should_tweet: data has changed, we should tweet: {first_info} {second_info}')
            return True
        # is it after 8:01 AM CST and we haven't tweeted today?
        elif current_time.hour >= 8 and current_time.minute >= 1 and previous_time.day != current_time.day:
            log(f'should_tweet: later than 8 and have not tweeted today, we should tweet: {first_info} {second_info}')
            return True
        # we've already tweeted this info
        else:
            log(f'should_tweet: we already tweeted this data: {first_info} {second_info}')
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
    must_have_one = ['eligib', 'immuniz']
    should_have_one = [
        'are now',
        'is now',
        'moves to',
        'as of',
        'update for',
        'remains at',
        'remain at',
        'remains unchanged',
        'remain unchanged',
        '1st dose:',
        '2nd dose:',
        'drops to',
        'no changes',
        'moving down',
    ]

    for must_have in must_have_one:
        if tweet_text.lower().find(must_have) > 0:
            for should_have in should_have_one:
                if tweet_text.lower().find(should_have) >= 0:
                    log(f'should_retweet: matches found {should_have}, we should retweet', tweet_text)
                    return True

    log('should_retweet: no matching strings found', tweet_text)
    return False


def clean_string(dirty):
    strip = [
        '<strong>',
        '</strong>',
        '<span style="font-size: 36px;">',
        '</span>',
        '&nbsp;',
    ]
    clean = dirty
    for item in strip:
        clean = clean.replace(item, '')
    return clean


if __name__ == '__main__':
    log('Sask Vaccine Bot is now running...')
    load_dotenv()
    while True:
        log('Checking for updates...')
        vaccine_website = "https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility"
        html = get_html(vaccine_website)
        if html is not None:
            current_booking = get_string_between(html, '<blockquote><strong>Currently Booking:', '</strong></blockquote>', 20)
            second_booking = get_string_between(html, '<h2>2nd Doses Eligibility:', '</h2>', 4)

            if current_booking is None and second_booking is None:
                current_booking = get_string_between(html, '<span style="font-size: 36px;">Currently Booking Online:', '</strong></span>', 31)

            if current_booking is not None:
                current_booking = clean_string(current_booking)
                if should_tweet(current_booking, second_booking, get_previous(), datetime.datetime.now()):
                    tweet = compose_tweet(current_booking, second_booking, datetime.datetime.now(), vaccine_website)
                    if tweet is not None:
                        update_status(tweet)
                        set_previous(current_booking, second_booking)
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
