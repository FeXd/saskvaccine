# Sask Vaccine Bot
🤖 Bot to track COVID-19 vaccine age eligibility in #SK  
⏰ Tweets when info changes & every morning around 8 am  
📢 Retweets [@SKGov](https://twitter.com/SKGov) & [@SaskHealth](https://twitter.com/SaskHealth)  
💻 Maintained by [@FeXd](https://github.com/FeXd)  
🐣 https://twitter.com/saskvaccine  

## ⁉️ How & Why
**Sask Vaccine Bot** is a [Twitter bot](https://en.wikipedia.org/wiki/Twitter_bot) dedicated to **tracking COVID-19 vaccine age eligibility in Saskatchewan**.  
It is written in [Python 3](https://www.python.org/) and uses the following packages:
- [urllib](https://docs.python.org/3/library/urllib.html) to pull information from the [Appointments for COVID-19 Vaccine Website](https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking)
- [Tweepy](https://github.com/tweepy/tweepy) to read tweets from [@SKGov](https://twitter.com/SKGov) / [@SaskHealth](https://twitter.com/SaskHealth) and to tweet / retweet to [@saskvaccine](https://twitter.com/saskvaccine)
- [python-dotenv](https://github.com/theskumar/python-dotenv) to set environment variables from a `.env` file

_The Saskatchewan Health Authority_ does a fairly good job updating everyone via their [website](https://www.saskhealthauthority.ca/) and [twitter](https://twitter.com/SaskHealth). But many people in Saskatchewan (myself included) are just looking for one thing... **when can we sign up to get vaccinated!?**  

People can subscribe to notifications from [@saskvaccine](https://twitter.com/saskvaccine) for up to date COVID-19 vaccine age eligibility, rather than feeling the need to refresh the [Appointments for COVID-19 Vaccine Website](https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking) or their twitter feed over and over again.

## 💻 Dependencies & Installation
- [Python 3](https://www.python.org/) with [pip](https://pypi.org/project/pip/)
     - run `pip install -r requirements.txt`
- Twitter Authentication Tokens via a [Twitter Developer Account](https://developer.twitter.com/)
     - Create a `.env` file with these tokens in the root of the directory
     - ([Tweepy](https://www.tweepy.org/) has good documentation on retrieving those [here](https://docs.tweepy.org/en/latest/auth_tutorial.html))
     - (`tweepy_setup.py` has also been provided to help set up tokens)
- Run the test suite (don't worry it won't Tweet)
     - run `python main_test.py`
- Run Sask Vaccine main script
     - run `python main.py`

## 🐞 Bugs, Questions, & Comments
Please feel free to provide feedback through any of the below methods:
- open an [issue](https://github.com/FeXd/saskvaccine/issues)  
- tweet [@FeXd](https://twitter.com/fexd) or [@saskvaccine](https://twitter.com/saskvaccine)  
- email <arlin@fexd.com>  

## 💡 Official Government Websites
This tool has been created independently and is not associated with the _Government of Saskatchewan_ or the _Saskatchewan Health Authority_. Below are links to official websites for more information about COVID-19, vaccination, and more.
- [https://stickittocovid.ca](https://stickittocovid.ca)
- [https://saskatchewan.ca/covid-19](https://saskatchewan.ca/covid-19)
- [https://saskhealthauthority.ca/](https://saskhealthauthority.ca/)
- [https://twitter.com/SKGov](https://twitter.com/SKGov)
- [https://twitter.com/SaskHealth](https://twitter.com/SaskHealth)

## 📜 License
Copyright (c) 2021 Arlin Schaffel

Licensed under the MIT License, available here:
https://github.com/FeXd/saskvaccine/blob/main/LICENSE.md
