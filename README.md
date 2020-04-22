This Project Is The Part Of Programming for Data Science with Python Offerd By Udacity
Date:20/04/2020

BikeShare 
Python Script to Explore US Bikeshare Data 
This Python 3 script is written to explore data related to bike share systems for
Chicago, New York City, and Washington. It imports data from csv files and computes
descriptive statistics from the data. It is run from the terminal (or from Jupyter
notebooks). 
How to run the script 
This script is written in Python 3 and uses pandas, datetime, time, and csv packages.
You will need all of these packages and Python 3 to be able to launch the script.
Launch the bikeshare.py file from your terminal and you will see a prompt that will
guide your experience reviewing the bikeshare data and reading relevant data
analysis. You can also open the Data_Review_Chicago.ipynb file to view much of the
data analysis that is provided in the .py file, all relative to Chicago data. 
1) download the bikehsare folder onto your computer
2) open terminal
3) navigate to the location of your bikeshare folder
4) type the following into terminal / python bikeshare.py /
5) bikeshare.py:
 
import time 
import math 
import pandas as pd 
import numpy as np 
 
DEBUG = 0 
 
CITY_DATA = { 'chicago': 'chicago.csv', 
              'new york city': 'new_york_city.csv', 
              'washington': 'washington.csv' } 
 
MONTHS = ['january', 'february', 'march', 'april', 'may', 'june'] 
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
'Friday', 'Saturday', 'Sunday'] 
 
# ------------------------- 
def clr_screen(): 
    """Clears terminal screen.""" 
 
    # clear terminal screen (tested on MacOS) 
    print('\033[H\033[J') 
 
# ------------------------- 
def sec_to_time(sec): 
    """ 
    Converts seconds to a human readable string representing
duration. 
 
    Args: 
        (number) - number of seconds, if not int, then rounded
using round() function 
 
    Returns: 
        (str) time - how long number of seconds is in
day:hour:minute:seconds format 
    """ 
 
    sec = round(sec) 
 
    day = sec // (24 * 3600) 
    sec = sec % (24 * 3600) 
    hour = sec // 3600 
    sec %= 3600 
    minute = sec // 60 
    sec %= 60 
    second = sec 
    #print("d:h:m:s-> %d:%d:%d:%d" % (day, hour, minute,
second)) 
 
    str = "" 
    if day > 0: str += " {} day(s)".format(day) 
    if hour > 0: str += " {} hour(s)".format(hour) 
    if minute > 0: str += " {} minute(s)".format(minute) 
    if second > 0: str += " {} second(s)".format(second) 
 
    return str 
 
# ------------------------- 
def get_filters(): 
    """ 
    Asks user to specify a city, month, and day to analyze. 
 
    Returns: 
        (str) city - name of the city to analyze 
        (str) month - name of the month to filter by, or "all" to
apply no month filter 
        (str) day - name of the day of week to filter by, or "all" to
apply no day filter 
    """ 
 
    #clr_screen() 
 
    print('\n'*2 + '='*40) 
    print('Hello! Let\'s explore some US bikeshare data!') 
    print('='*40 + '\n') 
 
    # get user input for city (chicago, new york city,
washington). HINT: Use a while loop to handle invalid inputs 
    print('Choose city:\n') 
    print('1 - Chicago') 
    print('2 - New York City') 
    print('3 - Washington\n') 
    while True: 
        try: 
            city_number = int(input('Choose [1-3] and press
<enter> : ')) 
            if city_number == 1 or city_number == 2 or city_number
== 3: 
                if city_number == 1: city = 'Chicago' 
                if city_number == 2: city = 'New York City' 
                if city_number == 3: city = 'Washington' 
                break 
        except: 
            pass 
 
    print('\n' + '-'*40 + '\n') 
 
    # get user input for month (all, january, february, ... , june) 
    print('Choose month:\n') 
    print('0 - All (January-June)') 
    print('1 - January') 
    print('2 - February') 
    print('3 - March') 
    print('4 - April') 
    print('5 - May') 
    print('6 - June\n') 
    while True: 
        try: 
            month_number = int(input('Choose [0-6] and press
<enter> : ')) 
            if month_number == 0: 
                month = 'all' 
                break 
            elif month_number >= 1 and month_number <= 6: 
                month = MONTHS[month_number-1] 
                break 
        except: 
            pass 
 
    print('\n' + '-'*40 + '\n') 
 
    # get user input for day of week (all, monday, tuesday, ...
sunday) 
    print('Choose day of week:\n') 
    print('0 - All (Monday-Sunday)') 
    print('1 - Monday') 
    print('2 - Tuesday') 
    print('3 - Wednesday') 
    print('4 - Thursday') 
    print('5 - Friday') 
    print('6 - Saturday') 
    print('7 - Sunday\n') 
    while True: 
        try: 
            day_number = int(input('Choose [0-7] and press
<enter> : ')) 
            if day_number == 0: 
                day = 'all' 
                break 
            elif day_number >= 1 and day_number <= 7: 
                day = DAYS[day_number-1] 
                break 
        except: 
            pass 
 
    print('\n' + '-'*40 + '\n') 
 
    # ask for debug mode 
    global DEBUG 
    print('Debug mode:\n') 
    print('0 - Off') 
    print('1 - On\n') 
    while True: 
        try: 
            debug_number = int(input('Choose [0-1] and press
<enter> : ')) 
            if debug_number == 0: 
                debug_label = 'off' 
                DEBUG = 0 
                break 
            elif debug_number == 1: 
                debug_label = 'on' 
                DEBUG = 1 
                break 
        except: 
            pass 
 
    print('\n' + '-'*40 + '\n') 
 
    print('Your choice:\n') 
    print('City: {}'.format(city.title())) 
    print('Month(s): {}'.format(month.title())) 
    print('Day(s) of week: {}'.format(day.title())) 
    print('Debug mode: {}'.format(debug_label.title())) 
 
    print('') 
    cont = input('Press <enter> to start generating statistics...') 
    #clr_screen() 
 
    return city, month, day 
 
# ------------------------- 
def load_data(city, month, day): 
    """ 
    Loads data for the specified city and filters by month and
day if applicable. 
 
    Args: 
        (str) city - name of the city to analyze 
        (str) month - name of the month to filter by, or "all" to
apply no month filter 
        (str) day - name of the day of week to filter by, or "all" to
apply no day filter 
    Returns: 
        df - Pandas DataFrame containing city data filtered by
month and day 
    """ 
 
    # standardize input values 
    city = city.lower() 
    month = month.lower() 
    day = day.lower() 
 
    # load data file into a dataframe 
    try: 
        df = pd.read_csv(CITY_DATA[city]) 
    except Exception as e: 
        print("Exception occurred: {}".format(e)) 
 
    # convert the Start Time column to datetime 
    df['Start Time'] = pd.to_datetime(df['Start Time']) 
 
    # extract month and day of week from Start Time to create
new columns 
    df['month'] = df['month'] = df['Start Time'].dt.month #Jan=1
Dec=12 
    df['day_of_week'] = df['Start Time'].dt.weekday_name 
 
    # filter by month if applicable 
    if month != 'all': 
        month = MONTHS.index(month) + 1 
        # filter by month to create the new dataframe 
        df = df[df['month'] == month] 
 
    # filter by day of week if applicable 
    if day != 'all': 
        # filter by day of week to create the new dataframe 
        df = df[df['day_of_week'] == day.title()] 
 
    return df 
 
# ------------------------- 
def time_stats(df): 
    """Displays statistics on the most frequent times of
travel.""" 
 
    print('\n' + '-'*40) 
    print('Calculating The Most Frequent Times of Travel...') 
    print('-'*40) 
 
    if DEBUG: 
        start_time = time.time() 
 
    # display the most common month 
    popular_month = df['month'].mode()[0] 
    print('Most Frequent Month is
{}'.format(MONTHS[popular_month-1].title())) 
 
    # display the most common day of week 
    df['dayofweek_number'] = df['Start Time'].dt.dayofweek 
    popular_dayofweek = df['dayofweek_number'].mode()[0] 
    print('Most Frequent Day of Week is
{}'.format(DAYS[popular_dayofweek].title())) 
 
    # display the most common start hour 
    df['hour'] = df['Start Time'].dt.hour 
    popular_hour = df['hour'].mode()[0] 
    print('Most Frequent Start Hour is
{}:00'.format(popular_hour)) 
 
    if DEBUG: 
        print('-'*10) 
        print("This took %s seconds." % (time.time() - start_time)) 
 
# ------------------------- 
def station_stats(df): 
    """Displays statistics on the most popular stations and
trip.""" 
 
    print('\n' + '-'*40) 
    print('Calculating The Most Popular Stations and Trip...') 
    print('-'*40) 
 
    if DEBUG: 
        start_time = time.time() 
 
    # display most commonly used start station 
    popular_start_station = df['Start Station'].mode()[0] 
    popular_start_station_num_of_uses = df[df['Start Station']
== popular_start_station].count()[0] 
    print("Most popular start station {} was used {}
times".format(popular_start_station,
popular_start_station_num_of_uses)) 
 
    # display most commonly used end station 
    popular_end_station = df['End Station'].mode()[0] 
    popular_end_station_num_of_uses = df[df['End Station'] ==
popular_end_station].count()[0] 
    print("Most popular end station {} was used {}
times".format(popular_end_station,
popular_end_station_num_of_uses)) 
 
    # display most frequent combination of start station and
end station trip 
    # combine start and end stations for comparison 
    df['Trip'] = 'FROM ' + df['Start Station'] + ' TO '+ df['End
Station'] 
    most_frequent_trip = df['Trip'].mode()[0] 
    most_frequent_trip_number = df[df['Trip'] ==
most_frequent_trip].count()[0] 
    print("Most popular trip chosen by {} users is
{}".format(most_frequent_trip_number, most_frequent_trip)) 
 
    if DEBUG: 
        print('-'*10) 
        print("This took %s seconds." % (time.time() - start_time)) 
 
# ------------------------- 
def trip_duration_stats(df): 
    """Displays statistics on the total and average trip
duration.""" 
 
    print('\n' + '-'*40) 
    print('Calculating Trip Duration...') 
    print('-'*40) 
 
    if DEBUG: 
        start_time = time.time() 
 
    # display total travel time 
    total_travel_time = df['Trip Duration'].sum() #seconds 
    #print("Total travel time for all trips:
{}".format(str(datetime.timedelta(seconds=total_travel_time)
))) 
    print("Total travel time for all trips is" +
sec_to_time(total_travel_time)) 
 
    # display mean travel time 
    mean_travel_time = df['Trip Duration'].mean() 
    print("Mean travel time for all trips is" +
sec_to_time(mean_travel_time)) 
 
    # display shortest travel time 
    shortest_travel_time = df['Trip Duration'].min() 
    print("Shortest individual travel time is" +
sec_to_time(shortest_travel_time)) 
 
    # display longest travel time 
    longest_travel_time = df['Trip Duration'].max() 
    print("Longest individual travel time is" +
sec_to_time(longest_travel_time)) 
 
    if DEBUG: 
        print('-'*10) 
        print("This took %s seconds." % (time.time() - start_time)) 
 
# ------------------------- 
def user_stats(df): 
    """Displays statistics on bikeshare users.""" 
 
    print('\n' + '-'*40) 
    print('Calculating User Stats...') 
    print('-'*40) 
 
    if DEBUG: 
        start_time = time.time() 
 
    # display counts of user types 
    user_types = df['User Type'].value_counts().to_dict() 
    for user_type in user_types: 
        print('There is/are {} occurence(s) of {} user
type'.format(user_types[user_type], user_type)) 
 
    # display counts of gender 
    if 'Gender' in df: 
        gender_types = df['Gender'].value_counts().to_dict() 
        for gender_type in gender_types: 
            print('There is/are {} {}
user(s)'.format(gender_types[gender_type], gender_type)) 
 
    # display earliest, most recent, and most common year of
birth 
    if 'Birth Year' in df: 
        year_earliest = df['Birth Year'].min().astype(np.int64) 
        year_most_recent = df['Birth
Year'].max().astype(np.int64) 
        year_most_common = df['Birth
Year'].mode()[0].astype(np.int64) 
        print("The oldest user was born in
{}".format(year_earliest)) 
        print("The youngest user was born in
{}".format(year_most_recent)) 
        print("The most common birth year of a user is
{}".format(year_most_common)) 
 
    if DEBUG: 
        print('-'*10) 
        print("This took %s seconds." % (time.time() - start_time)) 
 
# ------------------------- 
def main(): 
    while True: 
        city, month, day = get_filters() 
        df = load_data(city, month, day) 
 
        time_stats(df) 
        station_stats(df) 
        trip_duration_stats(df) 
        user_stats(df) 
 
        print('\n' + '-'*40) 
        restart = input('Would you like to restart? Enter [yes] to
continue or anything to quit and press <enter>: ') 
        if restart.lower() != 'yes': 
            break 
 
 
if __name__ == "__main__": 
 main() 
Datasets 
The datasets used for this script contain bike share data for the first six months of
2017. You can access the original data files here Chicago, New York City, Washington.
Some data wrangling, to reduce columns and reformat, has been performed to
condense these files to the core six columns used in this project. This makes the
analysis and the evaluation in this project more straightforward. 
The data is provided by Motivate, which is a bike share system provider for many
cities in the United States. The data files for all three cities contain the same six
columns: * Start Time * End Time * Trip Duration (in seconds) * Start Station * End
Station * User Type (Subscriber or Customer) 
The Chicago and New York City files also contain the following two columns: * Gender
* Birth Year 
Questions explored 
The script answers the following questions about the bike share data:
Popular times of travel * What is the most popular month for start time? * What is
the most popular day of week (Monday, Tuesday, etc.) for start time? * What is the
most popular hour of day for start time?
Popular stations and trip * What is the most popular start station and most popular
end station? * What is the most popular trip?
Trip duration * What is the total trip duration and average trip duration?
User information * What are the counts of each user type? * What are the counts of
gender? (only available for NYC and Chicago) * What are the earliest (i.e. oldest
person), most recent (i.e. youngest person), and most popular birth years? 
Additional Business Analysis Questions to Consider 
? How many bikes should each bikeshare have available?
? What is the optimal driving time between stations?
? Which users are more likely to pay for yearly subscription?
? Which users are more likely to buy short-term, such as 3-day or 24 hour passes?
? How does the use of bikes vary by cities?
? How does the season impact bikeshare use?
? Are certain user age groups more likely to use the bikeshare system than
others?
 
Resources 
? https://pandas.pydata.org/pandas-docs/stable/api.html#datetimelikeproperties
? https://pandas.pydata.org/pandasdocs/stable/generated/pandas.to_datetime.html
The datetime module contains many useful methods for handling date filtering and
extraction: strftime converts date objects into readable strings:
https://www.programiz.com/python-programming/datetime/strftime strptime
takes strings and converts them into date objects that Python can understand:
https://www.programiz.com/python-programming/datetime/strptime strf & strp
time: https://docs.python.org/3/library/datetime.html#strftime-and-strptimebehavior
This
stackoverflow
answer
explains
perfectly
how
to
extract
day,
month,

year
from
a
Date:
https://stackoverflow.com/questions/21954197/which-is-thefastest-way-to-extract-day-month-and-year-from-a-givendate/21954923#21954923\

Visit Udacity:https://www.udacity.com/
