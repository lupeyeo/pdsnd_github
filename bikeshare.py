import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington)
    cities_list = ['Chicago', 'New York City', 'Washington']
    not_found = True

    while not_found:
        city = str(input("Enter city name here. Choose from Chicago, New York City, or Washington: ").title())
        if city in cities_list:
            print('ok')
            break
        else:
            print('City not found, please try again.')

        # Get user input for month (all, january, february, ... , june)
    month_list = ["All", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    not_found = True
    while not_found:
        month = str(input('Enter month name here or "all", if you do not wish to apply a filter: ').title())
        if month in month_list:
            print('ok')
            break
        else:
            print('Month not found. Try a month of the year.')

            # Get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ["All", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    not_found = True
    while not_found:
        day = str(input('Enter weekday here or "All", if you do not wish to apply a filter: ').title())
        if day in day_list:
            print('ok')
            break
        else:
            print('Weekday not found. Try a day of the week.')


    print('-'*40)
    return city, month, day




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
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'], format = "%Y-%m-%d %H:%M:%S")
    df['Start Time Month'] = pd.DatetimeIndex(df['Start Time']).month_name()
    df['Start Time Weekday'] = df['Start Time'].dt.day_name()
    df['Start Time Hour'] = df['Start Time'].dt.hour


    # Filter applied for month and day. If "all", no filter is applied.
    if month != 'All':
        df = df.loc[df['Start Time Month'] == month]
    if day != 'All':
        df = df.loc[df['Start Time Weekday'] == day]


    return df

def display_data(df):
    """Displays raw data in iterations of 5 rows. When prompted, user can view the next 5 rows."""
    # Ask for user input
    pd.set_option('display.max_columns',200)
    show_data = str(input('Do you wish to see the raw data? Enter "yes" or "no": ').title())
    index_top_rows = 0
    index_bottom_rows = 5

    # Loop to ensure "yes" or "no" is entered. If "yes", display top 5 rows and increase indices by 5. If "no", break and move on.
    while show_data != 'No':
        if show_data != 'Yes' and show_data != 'No':
            show_data = str(input('The value you entered was neither "yes" or "no". Please try again: ').title())
        elif show_data == 'Yes':
            print(df[index_top_rows:index_bottom_rows])
            show_data = str(input('Do you wish to see the next 5 rows? Enter "yes" or "no": ').title())
            index_top_rows += 5
            index_bottom_rows += 5

    print("Okay, let's move on.")

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    most_common_month = df['Start Time Month'].mode()[0]
    print("The most common month is: {}".format(most_common_month))

    # Display the most common day of week
    most_common_day = df['Start Time Weekday'].mode()[0]
    print("The most common weekday is: {}".format(most_common_day))

    # Display the most common start hour
    most_common_hour = df['Start Time Hour'].mode()[0]
    print("The most common hour is: {}".format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    most_common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is: {}.".format(most_common_start_station))

    # Display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print("The most common end station is: {}.".format(most_common_end_station))

    # Display most frequent combination of start station and end station trip
    most_popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print("The most common station combination is: {}.".format(most_popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is: {:.2f} seconds, which is {:.2f} minutes or {:.2f} hours.".format(total_travel_time, total_travel_time/60, total_travel_time/3600))

    # Display mean travel time
    mean_travel_time = float(df['Trip Duration'].mean())
    print("The mean travel time is: {:.2f} seconds, which is {:.2f} minutes or {:.2f} hours.".format(mean_travel_time, mean_travel_time/60, mean_travel_time/3600))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_user_types = df.groupby(['User Type'])['User Type'].count()
    print("The user types are distributed as follows: \n{}\n".format(count_user_types))

    # Display counts of gender
    try:
        count_genders = df.groupby(['Gender'])['Gender'].count()
        print("The genders are distributed as follows: \n{}\n".format(count_genders))
    except KeyError:
        print("This file does not contain data on gender.")

    # Display earliest, most recent, and most common year of birth. Try and except clauses ensure that the data source contains the necessary data.
    try:
        earliest_yob = int(df['Birth Year'].min())
        most_recent_yob = int(df['Birth Year'].max())
        most_common_yob = int(df['Birth Year'].mode()[0])

        print("The earliest year of birth is: {}".format(earliest_yob))
        print("The most recent year of birth is: {}".format(most_recent_yob))
        print("The most common year of birth is: {}".format(most_common_yob))
    except KeyError:
        print("This file does not contain data on the birth year.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
