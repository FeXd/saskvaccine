# Sask Vaccine
🤖 A bot to track COVID-19 vaccine age limit requirement in Saskatchewan.  
⏰ Tweets when info changes and once per day around 8 am.  
💻 Maintained by [@FeXd](https://github.com/FeXd).  
🐣 https://twitter.com/saskvaccine  

## ⁉️ How and Why
**Sask Vaccine** is a simple Python3 script that uses [urllib](https://docs.python.org/3/library/urllib.html) to pulll information from the [Appointments for COVID-19 Vaccine Website](https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking) and [Tweepy](https://github.com/tweepy/tweepy) to tweet updates to [@saskvaccine](https://twitter.com/saskvaccine).

_The Saskatchewan Health Authority_ does a fairly good job updating everyone via their [website](https://www.saskhealthauthority.ca/) and [twitter](https://twitter.com/SaskHealth). But many people in Saskatchewan (myself included) are just looking for one thing... **when can we sign up to get vaccinated!?**  

This bot is dedicated to just that, so that people can check [@saskvaccine](https://twitter.com/saskvaccine) quickly and easily, rather than feeling the need to refresh the [Appointments for COVID-19 Vaccine Website](https://www.saskatchewan.ca/government/health-care-administration-and-provider-resources/treatment-procedures-and-guidelines/emerging-public-health-issues/2019-novel-coronavirus/covid-19-vaccine/vaccine-booking) over and over again.

## 💻 Dependencies & Installation
- Python 3.x
     - `pip install -r requirements.txt`
- Twitter Authentication Tokens via a [Twitter Developer Account](https://developer.twitter.com/)
     - Create a `.env` file with these tokens in the root of the directory
     - ([Tweepy](https://www.tweepy.org/) has good documentation on retrieving those [here](https://docs.tweepy.org/en/latest/auth_tutorial.html))

## 🐞 Bugs, Questions, & Comments
Please feel free to provide feedback through any of the below methods:
- open an [issue](https://github.com/FeXd/saskvaccine/issues)  
- tweet [@FeXd](https://twitter.com/fexd) or [@saskvaccine](https://twitter.com/saskvaccine)  
- email <arlin@fexd.com>  

## 📜 License
     Copyright (c) 2021 Arlin Schaffel

     Licensed under the MIT License, available here:
     https://github.com/FeXd/saskvaccine/blob/main/LICENSE.md
