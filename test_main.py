import main
import datetime


def test_get_html():
    successful_urls = [
        'https://google.com',
        'https://www.saskatchewan.ca/',
    ]
    for successful_url in successful_urls:
        assert main.get_html(successful_url) is not None, f'get_html({successful_url}) should NOT return None'

    failure_urls = [
        '',
        'https://',
        'https://abcsfaoawoinvowin.com',
        'http://google',
        'mailto://foo',
    ]
    for failure_url in failure_urls:
        assert main.get_html(failure_url) is None, f'get_html({failure_url}) should return None'


def test_get_current_booking():
    test_current_booking = [
        {'file': 'test_data/20210310vaccine.html',
         'booking': 'Online and telephone bookings open at 8 a.m. on March 11th for citizens 85 years and older (born on this day or earlier, 1935)'},
        {'file': 'test_data/20210311vaccine.html',
         'booking': 'Currently Booking: Citizens 85 years and older (born on this day or earlier, 1936)'},
        {'file': 'test_data/20210313vaccine.html',
         'booking': 'Currently Booking: Citizens 76 years and older (born on this day or earlier, 1945)'},
        {'file': 'test_data/20210315vaccine.html',
         'booking': 'Currently Booking: Citizens 70 years and older (born on this day or earlier, 1951) provincially (online and call centre booking available) and individuals 50 &ndash; 69 years of age living in the <a href="https://web.archive.org/web/20210315223936/https://www.saskatchewan.ca/business/first-nations-metis-and-northern-community-businesses/economic-development/northern-administration-district">Northern Administrative District</a>&nbsp;(call centre booking ONLY).'},
        {'file': 'test_data/20210319vaccine.html',
         'booking': 'Currently Booking: Citizens 67 years and older (born on this day or earlier, 1954) provincially (online and call centre booking available) and individuals 50 to 69 years of age living in the <a href="https://web.archive.org/web/20210319152842/https://www.saskatchewan.ca/business/first-nations-metis-and-northern-community-businesses/economic-development/northern-administration-district">Northern Administrative District</a>&nbsp;(call centre booking ONLY).'},
        {'file': 'test_data/20210327vaccine.html',
         'booking': 'Currently Booking: Citizens 62 years and older (born on this day in 1959 or earlier) provincially (online and call centre booking available)'},
        {'file': 'test_data/20210402vaccine.html',
         'booking': 'Currently Booking: Citizens 60 years and older (born on this day in 1961 or earlier) provincially (online and call centre booking available)'},
        {'file': 'test_data/20210404vaccine.html',
         'booking': 'Currently Booking: Citizens 58 years and older (born on this day in 1963 or earlier) provincially (online and call centre booking available)'},
        {'file': 'test_data/20210413vaccine.html',
         'booking': 'Currently Booking: Citizens 55 years and older (born on this day in 1966 or earlier) provincially (online and call centre booking available)'},
        {'file': 'test_data/20210416vaccine.html',
         'booking': 'Currently Booking: Citizens 48 years and older (born on this day in 1973 or earlier) provincially (online and call centre booking available)'},
        {'file': 'test_data/20210422vaccine.html',
         'booking': 'Currently Booking: Citizens 44 years and older (born on this day in 1977 or earlier) provincially (online and call centre booking available)'},
        {'file': 'test_data/20210427vaccine.html',
         'booking': 'Currently Booking: Citizens 44 years and older (born on this day in 1977 or earlier) provincially (online and call centre booking available)'},
        {'file': 'test_data/20210428vaccine.html',
         'booking': 'Currently Booking: Residents 42 years and older (born on this day in 1979 or earlier) provincially (online and call centre booking available)'},
    ]

    for current_booking in test_current_booking:
        file = open(current_booking['file'], "r")
        read = file.read().strip()
        file.close()
        result = main.get_current_booking(read)
        assert result == current_booking['booking'], f'get_current_booking() failed on {current_booking["file"]}, "{result}" does not equal "{current_booking["booking"]}"'


def test_compose_tweet():
    the_time = datetime.datetime.now()
    tweet_time = the_time.strftime('(%m/%d %I:%M %p CST)')

    tweets = [
        {'text': 'hello world',
         'website': 'google.com',
         'expect': 'hello world c/o: google.com #sk #sask #GetVaccinatedSK ' + tweet_time},
    ]

    for tweet in tweets:
        result = main.compose_tweet(tweet['text'], the_time, tweet['website'])
        assert result == tweet['expect'], f'compose_tweet() failed, {result} is not {tweet["expect"]}'


def test_should_tweet():
    inputs = [
        {
            'id': 'different data, same day',
            'booking_info': 'some booking info goes here',
            'previous': {'data': 'different', 'time': '2021-04-28T14:33:50Z'},
            'current_time': '2021-04-28T14:33:50Z',
            'expect': True,
         },
        {
            'id': 'different data, different day',
            'booking_info': 'some booking info goes here',
            'previous': {'data': 'different', 'time': '2021-04-28T14:33:50Z'},
            'current_time': '2021-05-05T01:00:03Z',
            'expect': True,
        },
        {
            'id': 'same data, new day, after 8 am',
            'booking_info': 'Booking information is here 123',
            'previous': {'data': 'Booking information is here 123', 'time': '2021-04-28T14:33:50Z'},
            'current_time': '2021-05-30T14:33:50Z',
            'expect': True,
        },
        {
            'id': 'same data, new day, before 8 am',
            'booking_info': 'Booking information is here 123',
            'previous': {'data': 'Booking information is here 123', 'time': '2021-04-28T14:33:50Z'},
            'current_time': '2021-05-30T07:33:50Z',
            'expect': False,
        },
        {
            'id': 'same data, same day, after 8 am',
            'booking_info': 'Booking information is here 123',
            'previous': {'data': 'Booking information is here 123', 'time': '2021-05-30T07:22:03Z'},
            'current_time': '2021-05-30T07:33:50Z',
            'expect': False,
        },
    ]

    for i in inputs:
        result = main.should_tweet(i['booking_info'], i['previous'], datetime.datetime.strptime(i['current_time'], '%Y-%m-%dT%H:%M:%SZ'))
        assert result == i['expect'], f'should_tweet() failed, {i["id"]}'


if __name__ == '__main__':
    print('Running Tests')
    test_get_html()
    test_get_current_booking()
    test_compose_tweet()
    test_should_tweet()
    print('All Tests Passed')
