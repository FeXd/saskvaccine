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


def test_should_retweet():
    inputs = [
        {'expect': False, 'tweet': ''},
        {'expect': False, 'tweet': '⚠️PSA: Regina adjusts Level 3 visitor restrictions in long-term care to allow limited outdoor visitation.\n\nOutdoor visits in Regina, Emerald Park, Lumsden &amp; Cupar care homes can occur w/up to 2 support people from the same household at one time.\n\nMore: https://t.co/LK335Oen8C https://t.co/p7NUGhyeb3'},
        {'expect': False, 'tweet': "Don't take the chance of passing COVID-19 on. Stay home if ill even if symptoms mild &amp; don't wait to get tested. COVID-19 spreads easily.\n\nFollow public health orders &amp; public health advice. Call 911 in emergencies or HealthLine 811 for advice and/or to arrange COVID-19 testing. https://t.co/g8OiSubAny"},
        {'expect': True, 'tweet': 'COVID-19 immunization age eligibility for May 5 remains at 37+ provincially &amp; 18+ for those living in the NSAD. Reminder to residents that clinic availability is based on vaccine availability, and demand for appointments outweighs the current supply. More: https://t.co/oVigqgV0sB https://t.co/yuaCUWhRrX'},
        {'expect': True, 'tweet': 'Happy #StarWarsDay2021. #COVID19sk vaccine eligibility is now 37 yrs+ provincially &amp; 18 yrs+ in the NSAD. Are you wearing your best Star Wars apparel to your COVID-19 vaccination appointment/drive-thru site today to celebrate? Tag us with your photos! #MayThe4thBeWithYou https://t.co/Kf5e4VCM41'},
        {'expect': True, 'tweet': 'Saskatchewan residents 40+ and remaining prioritized front-line workers are now eligible to book their #COVID19SK vaccination. \n\nView a list of vaccination pilot pharmacies at https://t.co/ZM7z12jaHR. https://t.co/ZjfcWCVN5O'},
        {'expect': False, 'tweet': '#COVID19SK Update for April 30: 427,739 Vaccines Administered, 264 New Cases, 252 Recoveries, 173 in Hospital, Four New Deaths\n\nCurrent 7-Day Average: 241 (19.7 per 100,000).\n\nFull details:  https://t.co/hkLRB0Taa0\n\nCOVID-19 Dashboard: https://t.co/kvBuGtZGWW https://t.co/TFieqT8mBP'},
        {'expect': False, 'tweet': 'One of the most common angling infractions in #SK is improper packaging when transporting fish. Understand the regulations, such as proper packaging, by reviewing the 2021-22 Anglers Guide on https://t.co/xo7kt3o1FY. https://t.co/P6yf0JH5zB'},
        {'expect': True, 'tweet': 'Saskatchewan residents 37+ are now eligible to book their #COVID19SK vaccination. \n\nBook online: https://t.co/OK1ksAAjQc\n\nOr by phone: 1-833-SASK-VAX (1-833-727-5829) https://t.co/Fr9BO3jxaf'},
        {'expect': True, 'tweet': '⚠️Effective 8 am May 6 eligibility in the provincial immunization program moves to 35+, except for residents living in the NSAD where it remains 18+. Applies to all immunization clinics: booked appointments, pharmacies, drive-thru/walk-in & mobile.\nMore: https://saskhealthauthority.ca/news/releases/Pages/2021/May/COVID-19-Immunization-update-effective-May-6.aspx'},
        {'expect': True, 'tweet': 'COVID-19 immunization age eligibility for May 5 remains at 37+ provincially & 18+ for those living in the NSAD. Reminder to residents that clinic availability is based on vaccine availability, and demand for appointments outweighs the current supply. More: https://saskhealthauthority.ca/news/releases/Pages/2021/May/COVID-19-immunization-alert-effective-May-5.aspx'},
        {'expect': True, 'tweet': '⚠️Effective 8am May 4, 2021 eligibility for immunization across SK moves to age 37+ except for the Northern Saskatchewan Administration District where it moves to 18+. This applies to all clinics: booked appts, drive-thru/walk-in, mobile & pharmacy. \n\nhttps://saskhealthauthority.ca/news/releases/Pages/2021/May/COVID-19-Immunization-Alert-Effective-May-4.aspx'},
        {'expect': False, 'tweet': 'Starting TOMORROW, Saturday, May 1 @Prairieland COVID-19 vaccine drive-thru (entry off St. Henry Ave) from 8:30 a.m. to 8:00 p.m. for anyone who meets current vaccine eligibility. The drive-thru will be open through the weekend and into next week as vaccine supplies allow.'},
    ]

    for i in inputs:
        result = main.should_retweet(i['tweet'])
        assert result == i['expect'], f'should_retweet() failed, {i["tweet"]} should have been {i["expect"]}'


if __name__ == '__main__':
    print('Running Tests')
    test_get_html()
    test_get_current_booking()
    test_compose_tweet()
    test_should_tweet()
    test_should_retweet()
    print('All Tests Passed')
