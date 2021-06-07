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


def test_get_string_between():
    start = '<blockquote><strong>Currently Booking:'
    end = '</strong></blockquote>'
    trim = 20
    tests = [
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
        {'file': 'test_data/20210519vaccine.html',
         'booking': 'Currently Booking: 1st Dose: Residents 16 years and older (born on this day in 2005 or earlier) provincially (online and call centre booking available). '},
        # {'file': 'test_data/20210525vaccine.html',
        #  'booking': 'testing'},
    ]

    for test in tests:
        file = open(test['file'], "r")
        read = file.read().strip()
        file.close()
        result = main.get_string_between(read, start, end, trim)
        assert result == test['booking'], f'get_string_between() failed on {test["file"]}, "{result}" does not equal "{test["booking"]}"'


def test_compose_tweet():
    the_time = datetime.datetime.now()
    tweet_time = the_time.strftime('%m/%d %I:%M %p CST')

    tweets = [
        # normal tweet everything is short and fits
        {'first': 'hello',
         'second': 'world',
         'website': 'google.com',
         'expect': f'hello\n\nworld\n\n#sk #sask #GetVaccinatedSK {tweet_time} google.com'
         },
        # no second string passed in
        {'first': 'foo',
         'second': None,
         'website': 'google.com',
         'expect': f'foo\n\n#sk #sask #GetVaccinatedSK {tweet_time} google.com'
         },
        # blank second string passed in
        {'first': 'empty second',
         'second': '',
         'website': 'google.com',
         'expect': f'empty second\n\n#sk #sask #GetVaccinatedSK {tweet_time} google.com'
         },
        # possible_tweets array hit item 0 - full tweet
        {'first': '1st Dose: Residents 12 years and older provincially (online and call centre booking available).',
         'second': '2nd Dose: Residents 65+ or anyone who received their first dose before March 22',
         'website': 'https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility',
         'expect': f'1st Dose: Residents 12 years and older provincially (online and call centre booking available).\n\n2nd Dose: Residents 65+ or anyone who received their first dose before March 22\n\n#sk #sask #GetVaccinatedSK {tweet_time} https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility'
         },
        # possible_tweets array hit item 1 - short first
        {'first': '1st Dose: Residents 12 years and older (born on this day in 2009 or earlier) provincially (online and call centre booking available).',
         'second': '2nd Dose: Residents 65+ or anyone who received their first dose before March 22',
         'website': 'https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility',
         'expect': f'1st Dose: Residents 12 years and older (born on this day in 2009 or earlier) provincially \n\n2nd Dose: Residents 65+ or anyone who received their first dose before March 22\n\n#sk #sask #GetVaccinatedSK {tweet_time} https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility'
         },
        # possible_tweets array hit item 2 - short first, no hashtags
        {'first': 'Currently Booking: 1st Dose: Residents 12 years and older (born on this day in 2009 or earlier) provincially (online and call centre booking available).',
         'second': '2nd Doses Eligibility: Residents 65+ or anyone who received their first dose before March 22, 2021',
         'website': 'https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility',
         'expect': f'Currently Booking: 1st Dose: Residents 12 years and older (born on this day in 2009 or earlier) provincially \n\n2nd Doses Eligibility: Residents 65+ or anyone who received their first dose before March 22, 2021\n\n{tweet_time} https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility'
         },
        # possible_tweets array hit item 3 - long first, no second
        {'first': 'Currently Booking: 1st Dose: Residents 12 years and older (born on this day in 2009 or earlier) provincially (online and call centre booking available). This is a long tweet, so second might get bumped.',
         'second': '2nd Doses Eligibility: Residents 65+ or anyone who received their first dose before March 22, 2021',
         'website': 'https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility',
         'expect': f'Currently Booking: 1st Dose: Residents 12 years and older (born on this day in 2009 or earlier) provincially (online and call centre booking available). This is a long tweet, so second might get bumped.\n\n#sk #sask #GetVaccinatedSK {tweet_time} https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility'
         },
        # possible_tweets array hit item 4 - long first, no second, no hashtags
        {'first': 'Currently Booking: 1st Dose: Residents 12 years and older (born on this day in 2009 or earlier) provincially (online and call centre booking available). This is a long tweet, so second might get bumped. It is so long, we might not even get hashtags!?',
         'second': '2nd Doses Eligibility: Residents 65+ or anyone who received their first dose before March 22, 2021',
         'website': 'https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility',
         'expect': f'Currently Booking: 1st Dose: Residents 12 years and older (born on this day in 2009 or earlier) provincially  This is a long tweet, so second might get bumped. It is so long, we might not even get hashtags!?\n\n{tweet_time} https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility'
         },
        # possible_tweets array hit item 5 - short first, no second, no hashtags
        {'first': 'Currently Booking: 1st Dose: Residents 12 years and older (born on this day in 2009 or earlier) provincially (online and call centre booking available). This is a long tweet, so second might get bumped. It is so long, we might not even get hashtags!? Maybe the short version.',
         'second': '2nd Doses Eligibility: Residents 65+ or anyone who received their first dose before March 22, 2021',
         'website': 'https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility',
         'expect': f'Currently Booking: 1st Dose: Residents 12 years and older (born on this day in 2009 or earlier) provincially  This is a long tweet, so second might get bumped. It is so long, we might not even get hashtags!? Maybe the short version.\n\n{tweet_time} https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility'
         },
        # possible_tweets - no matches
        {'first': 'Currently Booking: 1st Dose: Residents 12 years and older (born on this day in 2009 or earlier) provincially (online and call centre booking available). This is a long tweet, so second might get bumped. It is so long, we might not even get hashtags!? Maybe the short version. Nope... it is just too long!?',
         'second': '2nd Doses Eligibility: Residents 65+ or anyone who received their first dose before March 22, 2021',
         'website': 'https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking#check-your-eligibility',
         'expect': None
         },
    ]

    for tweet in tweets:
        result = main.compose_tweet(tweet['first'], tweet['second'], the_time, tweet['website'])
        assert result == tweet['expect'], f'compose_tweet() failed, {result} is not {tweet["expect"]}'


def test_should_tweet():
    inputs = [
        {
            'id': 'both different data, same day',
            'first_info': 'first booking info goes here',
            'second_info': 'second booking info goes here',
            'previous': {'first': '1 different', 'second': '2 different', 'time': '2021-04-28T14:33:50Z'},
            'current_time': '2021-04-28T14:33:50Z',
            'expect': True,
         },
        {
            'id': 'both different data, different day',
            'first_info': 'first booking info goes here',
            'second_info': 'second booking info goes here',
            'previous': {'first': '1 different', 'second': '2 different', 'time': '2021-04-28T14:33:50Z'},
            'current_time': '2021-05-05T01:00:03Z',
            'expect': True,
        },
        {
            'id': 'first different data, different day',
            'first_info': 'first booking info goes here',
            'second_info': 'second booking info goes here',
            'previous': {'first': '1 different', 'second': 'second booking info goes here', 'time': '2021-04-28T14:33:50Z'},
            'current_time': '2021-05-05T01:00:03Z',
            'expect': True,
        },
        {
            'id': 'second different data, different day',
            'first_info': 'first booking info goes here',
            'second_info': 'second booking info goes here',
            'previous': {'first': '1 different', 'second': 'second booking info goes here', 'time': '2021-04-28T14:33:50Z'},
            'current_time': '2021-05-05T01:00:03Z',
            'expect': True,
        },
        {
            'id': 'both same data, new day, after 8 am',
            'first_info': 'Booking information is here 123',
            'second_info': 'Booking information is here 456',
            'previous': {'first': 'Booking information is here 123', 'second': 'Booking information is here 456', 'time': '2021-04-28T14:33:50Z'},
            'current_time': '2021-05-30T14:33:50Z',
            'expect': True,
        },
        {
            'id': 'both same data, new day, exactly 8 am',
            'first_info': 'Booking information is here 123',
            'second_info': 'Booking information is here 456',
            'previous': {'first': 'Booking information is here 123', 'second': 'Booking information is here 456', 'time': '2021-04-28T14:33:50Z'},
            'current_time': '2021-05-30T08:00:00Z',
            'expect': False,
        },
        {
            'id': 'both same data, new day, before 8 am',
            'first_info': 'Booking information is here 123',
            'second_info': 'Booking information is here 456',
            'previous': {'first': 'Booking information is here 123', 'second': 'Booking information is here 456', 'time': '2021-04-28T14:33:50Z'},
            'current_time': '2021-05-30T07:33:50Z',
            'expect': False,
        },
        {
            'id': 'both same data, same day, after 8 am',
            'first_info': 'Booking information is here 123',
            'second_info': 'Booking information is here 456',
            'previous': {'first': 'Booking information is here 123', 'second': 'Booking information is here 456', 'time': '2021-05-30T07:22:03Z'},
            'current_time': '2021-05-30T07:33:50Z',
            'expect': False,
        },
    ]

    for i in inputs:
        result = main.should_tweet(i['first_info'], i['second_info'], i['previous'], datetime.datetime.strptime(i['current_time'], '%Y-%m-%dT%H:%M:%SZ'))
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
        {'expect': True, 'tweet': 'Effective, 8 a.m., Saturday, May 8, 2021, eligibility in the provincial age-based immunization program moves to 32 years of age and older. \n\nEffective, 8 a.m., Monday, May 10, 2021, eligibility in the provincial age-based immunization program moves to 29 years of age and older.'},
        {'expect': True, 'tweet': 'Residents ages 32+ are now eligible to book their #COVID19SK shot by visiting http://StickItToCOVID.ca or calling 1-833-SASK-VAX (1-833-727-5829)\n\nResidents ages 18-34 in the Northern Admin District are now eligible to book their shot by calling 1-833-SASK-VAX (1-833-727-5829)'},
        {'expect': True, 'tweet': 'COVID-19 Immunization Update effective May 11\n\nEligibility criteria remains unchanged at age 29 and older. It remains 18 and older in the Northern Saskatchewan Administration District.\n\nFor more information: https://saskhealthauthority.ca/news/releases/Pages/2021/May/COVID-19-Immunization-Update-effective-May-11.aspx'},
        {'expect': True, 'tweet': 'ICYMI: Effective at 8 a.m. May 14, eligibility for Covid-19 vaccinations moves to ages 23 and older and 18 and older in the Northern Saskatchewan Administration District. Read the rest of the news release for complete details: https://saskhealthauthority.ca/news/releases/Pages/2021/May/COVID-19-Immunization-Update-effective-May-14.aspx'},
        {'expect': True, 'tweet': 'As of May 17, 20+ are eligible provincially & 18+ in the Northern SK Admin District.\n\nNEW: Those eligible for 2nd doses (85+ or immunized with 1st dose prior to Feb 15) can also begin booking at pharmacies or go to a SHA drive-thru/walk-in clinic: https://saskhealthauthority.ca/news/releases/Pages/2021/May/COVID-19-Immunization-Update-effective-May-17-Second-Doses-Now-Available-to-85-Years-and-Older.aspx'},
        {'expect': False, 'tweet': 'Important reminderRed exclamation mark symbol\n\nDid you book a COVID-19 immunization appointment but went to a drive-thru/walk-in clinic instead? MAKE SURE you are cancelling your scheduled appointment so someone else can go. For SHA clinics cancel online (https://saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking) or call 1-833-727-5829'},
        {'expect': False, 'tweet': '#COVID19SK Update For May 16: 590,952 Vaccines Administered, 167 New Cases, 156 Recoveries, One New Death.\n\nCurrent 7-Day Average: 191 (15.6 new cases per 100,000)\n\nFull Details: https://saskatchewan.ca/government/news-and-media/2021/may/16/covid19-update-for-may-16-590952-vaccines-administered-167-new-cases-156-recoveries-one-new-death\n\nCOVID-19 Dashboard: https://dashboard.saskatchewan.ca/health-wellness'},
        {'expect': False, 'tweet': "Saskatchewan actor Tatiana Maslany encourages everyone to get their #COVID19SK vaccine.\n\nVisit http://saskatchewan.ca/COVID19-vaccine to learn more about Saskatchewan's Vaccine Delivery Plan. \n\n#GetVaccinatedSK"},
        {'expect': False, 'tweet': "Former Humboldt Broncos player @KalebDahlgren encourages everyone to get their #COVID19SK vaccine.\n\nVisit http://saskatchewan.ca/COVID19-vaccine to learn more about Saskatchewan's Vaccine Delivery Plan. \n\n#GetVaccinatedSK"},
        {'expect': False, 'tweet': 'The Regina Drive-Thru clinic has used its’ supply of vaccine and has closed for the day. Those in line will be vaccinated. The clinic will open again Wednesday, May 19. For a list of drop-in clinics & wait times, please visit https://saskhealthauthority.ca/news/service-alerts-emergency-events/Pages/COVID-19-Vaccine-Drive-Thru-Wait-Times.aspx'},
        {'expect': False, 'tweet': 'Walk-in COVID-19 immunizations are available today in Rosthern at the\n\nCommunity Multipurpose Centre from 12:00 p.m. – 2:30 p.m. Must meet current age eligibility. Health card and ID required.”'},
        {'expect': False, 'tweet': 'Margaret Hicks received her 2nd dose of the #COVID19sk vaccination this morning at the Glencairn Neighbourhood Centre in #Regina & got her "I Stuck it to COVID" sticker. Yay Margaret! Party popper For current eligibility, visit http://saskatchewan.ca/covid19-vaccine. #StickItToCOVID'},
        {'expect': True, 'tweet': '#COVID19SK vaccine eligibility:\n\n1st dose: residents 16+\n\n2nd doses: residents 85+ or anyone who received their first dose before February 15, 2021\n\nBook online: http://StickItToCOVID.ca\n\nOr by phone: 1-833-SASK-VAX (1-833-727-5829)'},
        {'expect': False, 'tweet': '#SaskAg, Your mental and physical health are important too. To stay safe, ensure you take frequent breaks, eat healthy and know your limits. For more information, please visit http://saskatchewan.ca/farmsafety. #Farmsafety'},
        {'expect': True, 'tweet': 'COVID-19 Immunization Update for June 3:\n\n- Second doses remain at 65 & older OR first dose received on/before March 22\n- First doses remain at 12 & older \n- Where to get vaccinated \n- Drive-thru and walk-in clinic schedule through June 5\n\nRead: https://saskhealthauthority.ca/news/releases/Pages/2021/June/COVID-19-Immunization-Update-June-3.aspx'},
        {'expect': True, 'tweet': 'COVID-19 Immunization Update for June 2:\n\n- Second Doses Age Rolls Down to 65+ OR March 22; \n-Saskatchewan to Follow NACI Recommendations on Second Doses; \n- Update on AstraZeneca Second Doses; \n- Over 5,000 Appointments Available to be Booked\n\nRead More: https://saskhealthauthority.ca/news/releases/Pages/2021/June/COVID-19-Immunization-Update-Second-Dose-Eligibility-and-Additional-Booked-Appointments-Added.aspx'},
        {'expect': False, 'tweet': "Q: I got AstraZeneca (AZ) as my 1st COVID-19 vaccine dose. What are 2nd dose options?\nA: SHA will offer 2nd dose AZ clinics to eligible residents after June 6. You can get AZ as 2nd dose or Pfizer or Moderna. Recommended 12 wks btw AZ doses but must be >28 days if choosing other."},
        {'expect': False, 'tweet': 'Thank you to the community of Melfort for your gift of this Rock Snake which recently appeared in front of Melfort Hospital.\n\nThe message reads “This Rock Snake has been placed here at MUH to show gratitude to healthcare workers. Please add your painted rocks &  watch it grow!”'},
        {'expect': False, 'tweet': 'Headed to a SHA walk-in (#Lanigan or #Regina) or drive-thru (Regina or #Saskatoon) vaccination clinics today? Pls prepare for the heat! Wear light clothing & a hat. Bring plenty of water & light, refreshing snacks. Umbrella work for portable shade. Be safe.'},
        {'expect': False, 'tweet': '#Regina and area...\nThe drive-thru vaccination site at Evraz Place is now closed to new vehicles in line (as of 3:30 pm June 2). Everyone already in line will receive their vaccine today. \nThe site will reopen tomorrow at 8:30am. Thank you for your patience.'},
        {'expect': False, 'tweet': 'If you are trying to get pregnant, are pregnant, or are a new mom, you likely have lots of questions including questions about the COVID-19 vaccine. Here are the facts… Speak to your healthcare provider if you have questions.'},
        {'expect': False, 'tweet': 'A special youth (12-17) walk-in COVID-19 vaccination clinic will be held at Prairieland Park in #Saskatoon June 2, 4 & 5 from noon to 8pm offering Pfizer. Enter via Ruth Street. Bring your Saskatchewan Health Card and wear a mask.'},
        {'expect': True, 'tweet': 'Saskatchewan residents 60+ or anyone who received their first dose before March 29, 2021 are now eligible to book their second dose of the #COVID19SK vaccination. \n\nBook online: http://StickItToCOVID.ca\n\nOr by phone: 1-833-SASK-VAX (1-833-727-5829)'},
        {'expect': True, 'tweet': '#COVID19SK for June 6: 800,772 Vaccines Administered, 73 New Cases, 119 Recoveries, No New Deaths, 101 in Hospital.\n\n7-Day Average:  103 (8.4 per 100,000)\n\nVaccine eligibility\n\n1st Dose: 12+\n\n2nd Dose: 65+\n\nDashboard: https://dashboard.saskatchewan.ca/health-wellness\n\nFull Release: https://saskatchewan.ca/government/news-and-media/2021/june/06/covid19-update-for-june-6-800772-vaccines-administered-73-new-cases-119-recoveries-no-new-deaths'},
    ]

    for i in inputs:
        result = main.should_retweet(i['tweet'])
        assert result == i['expect'], f'should_retweet() failed, should have been {i["expect"]}, tweet: {i["tweet"]} '


if __name__ == '__main__':
    print('Running Tests')
    test_get_html()
    test_get_string_between()
    test_compose_tweet()
    test_should_tweet()
    test_should_retweet()
    print('All Tests Passed')
