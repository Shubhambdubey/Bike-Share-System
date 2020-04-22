import time
import math
import pandas as pd
import numpy as np

DEBUG = 0

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# -------------------------
def clr_screen():
    """Clears terminal screen."""

    # clear terminal screen (tested on MacOS)
    print('\033[H\033[J')

# -------------------------
def sec_to_time(sec):
    """
    Converts seconds to a human readable string representing duration.

    Args:
        (number) - number of seconds, if not int, then rounded using round() function

    Returns:
        (str) time - how long number of seconds is in day:hour:minute:seconds format
    """

    sec = round(sec)

    day = sec // (24 * 3600)
    sec = sec % (24 * 3600)
    hour = sec // 3600
    sec %= 3600
    minute = sec // 60
    sec %= 60
    second = sec
    #print("d:h:m:s-> %d:%d:%d:%d" % (day, hour, minute, second))

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
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    #clr_screen()

    print('\n'*2 + '='*40)
    print('Hello! Let\'s explore some US bikeshare data!')
    print('='*40 + '\n')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Choose city:\n')
    print('1 - Chicago')
    print('2 - New York City')
    print('3 - Washington\n')
    while True:
        try:
            city_number = int(input('Choose [1-3] and press <enter> : '))
            if city_number == 1 or city_number == 2 or city_number == 3:
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
            month_number = int(input('Choose [0-6] and press <enter> : '))
            if month_number == 0:
                month = 'all'
                break
            elif month_number >= 1 and month_number <= 6:
                month = MONTHS[month_number-1]
                break
        except:
            pass

    print('\n' + '-'*40 + '\n')

    # get user input for day of week (all, monday, tuesday, ... sunday)
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
            day_number = int(input('Choose [0-7] and press <enter> : '))
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
            debug_number = int(input('Choose [0-1] and press <enter> : '))
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
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
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

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['month'] = df['Start Time'].dt.month #Jan=1 Dec=12
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
    """Displays statistics on the most frequent times of travel."""

    print('\n' + '-'*40)
    print('Calculating The Most Frequent Times of Travel...')
    print('-'*40)

    if DEBUG:
        start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Frequent Month is {}'.format(MONTHS[popular_month-1].title()))

    # display the most common day of week
    df['dayofweek_number'] = df['Start Time'].dt.dayofweek
    popular_dayofweek = df['dayofweek_number'].mode()[0]
    print('Most Frequent Day of Week is {}'.format(DAYS[popular_dayofweek].title()))

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Frequent Start Hour is {}:00'.format(popular_hour))

    if DEBUG:
        print('-'*10)
        print("This took %s seconds." % (time.time() - start_time))

# -------------------------
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\n' + '-'*40)
    print('Calculating The Most Popular Stations and Trip...')
    print('-'*40)

    if DEBUG:
        start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    popular_start_station_num_of_uses = df[df['Start Station'] == popular_start_station].count()[0]
    print("Most popular start station {} was used {} times".format(popular_start_station, popular_start_station_num_of_uses))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    popular_end_station_num_of_uses = df[df['End Station'] == popular_end_station].count()[0]
    print("Most popular end station {} was used {} times".format(popular_end_station, popular_end_station_num_of_uses))

    # display most frequent combination of start station and end station trip
    # combine start and end stations for comparison
    df['Trip'] = 'FROM ' + df['Start Station'] + ' TO '+ df['End Station']
    most_frequent_trip = df['Trip'].mode()[0]
    most_frequent_trip_number = df[df['Trip'] == most_frequent_trip].count()[0]
    print("Most popular trip chosen by {} users is {}".format(most_frequent_trip_number, most_frequent_trip))

    if DEBUG:
        print('-'*10)
        print("This took %s seconds." % (time.time() - start_time))

# -------------------------
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\n' + '-'*40)
    print('Calculating Trip Duration...')
    print('-'*40)

    if DEBUG:
        start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() #seconds
    #print("Total travel time for all trips: {}".format(str(datetime.timedelta(seconds=total_travel_time))))
    print("Total travel time for all trips is" + sec_to_time(total_travel_time))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print("Mean travel time for all trips is" + sec_to_time(mean_travel_time))

    # display shortest travel time
    shortest_travel_time = df['Trip Duration'].min()
    print("Shortest individual travel time is" + sec_to_time(shortest_travel_time))

    # display longest travel time
    longest_travel_time = df['Trip Duration'].max()
    print("Longest individual travel time is" + sec_to_time(longest_travel_time))

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
        print('There is/are {} occurence(s) of {} user type'.format(user_types[user_type], user_type))

    # display counts of gender
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts().to_dict()
        for gender_type in gender_types:
            print('There is/are {} {} user(s)'.format(gender_types[gender_type], gender_type))

    # display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        year_earliest = df['Birth Year'].min().astype(np.int64)
        year_most_recent = df['Birth Year'].max().astype(np.int64)
        year_most_common = df['Birth Year'].mode()[0].astype(np.int64)
        print("The oldest user was born in {}".format(year_earliest))
        print("The youngest user was born in {}".format(year_most_recent))
        print("The most common birth year of a user is {}".format(year_most_common))

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
        restart = input('Would you like to restart? Enter [yes] to continue or anything to quit and press <enter>: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
