import time
import pandas as pd
import numpy as np
import math as m

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington).
    cities = set(["chicago", "new york city", "washington"])
    city = input("Which city would you like to analyze? (chicago, new york city, or washington)\n")
    while city not in cities:
        city = input("Please enter a valid city (chicago, new york city, or washington)\n")

    # Get user input for month (all, january, february, ... , june)
    months = set(["all", "january", "february", "march", "april", "may", "june"])
    month = input("During which month(s)? (all, january, february, ... , june)\n")
    while month not in months:
        month = input("Please enter a valid month (all, january, february, ... , june):\n")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    days = set(["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"])
    day = input("During which day(s)? (all, monday, tuesday, ... sunday)\n")
    while day not in days:
        day = input("Please enter a valid day of the week (all, monday, tuesday, ... sunday):\n")

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
    # Convert city to file name and load csv into DataFrame
    city = city.replace(" ", "_") + ".csv"
    df = pd.read_csv(city)
    
    # Filter by the provided month and day if the user selected something other than 'all'
    # Note: Start Time and End Time columns in the csv are assumed to be same day to simplify code due to short rental durations
    df['Start Time'] = pd.to_datetime(df['Start Time']) # converting the 'Start Time' column to a datetime object from a string
    if month != 'all':
        df = df[df['Start Time'].dt.month_name().str.lower() == month]
    if day != 'all':
        df = df[df['Start Time'].dt.day_name().str.lower() == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Find and display the most common month from the table
    most_common_month = df['Start Time'].dt.month_name().mode().iloc[0]
    print(f"The most common month is {most_common_month}")

    # Find and display the most common day of the week from the table
    most_common_dow = df['Start Time'].dt.day_name().mode().iloc[0]
    print(f"The most common day is {most_common_dow}")

    # Find and display the most common start hour from the table
    most_common_hour = df['Start Time'].dt.hour.mode().iloc[0]
    if most_common_hour > 12:
        print(f"The most common start hour is at {most_common_hour - 12} PM")
    else:
        print(f"The most common start hour is at {most_common_hour} AM")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Find and display the most commonly used start station
    most_common_start_station = df['Start Station'].mode().iloc[0]
    print(f"The most commonly used start station is {most_common_start_station}")

    # Find and display the most commonly used end station
    most_common_end_station = df['End Station'].mode().iloc[0]
    print(f"The most commonly used end station is {most_common_end_station}")


    # Find and display the most frequent combination of start station and end station trips
    most_common_station_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"The most common station combination is to start at {most_common_station_combo[0]} and end at {most_common_station_combo[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # Find and display total travel time
    total_travel_time = df['Trip Duration'].sum() # total duration in seconds
    years = total_travel_time // (365 * 24 * 3600) # Get number of years if any
    total_travel_time %= (365 * 24 * 3600) # update total seconds to remove that many years
    days = total_travel_time // (24 * 3600) # Get number of days if any
    total_travel_time %= (24 * 3600) # update total seconds to remove that many days
    hours = total_travel_time // 3600 # Get number of hours if any
    total_travel_time %= 3600 # update total seconds to remove that many hours
    minutes = total_travel_time // 60 # Get number of minutes if any
    seconds = total_travel_time % 60 # Set seconds to be equal to remaining seconds
    print(f"The total travel time is {years} years, {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds." )

    # Find and display the mean travel time
    mean_travel_time = df['Trip Duration'].mean();
    hours = mean_travel_time // 3600 # Get number of hours if any
    mean_travel_time = mean_travel_time % 3600 # update total seconds to remove the hours
    minutes = mean_travel_time // 60
    seconds = mean_travel_time % 60
    print(f"The mean travel time is {m.floor(hours)} hours, {m.floor(minutes)} minutes, and {m.floor(seconds)} seconds.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Caclulate and display counts of user types
    count_of_user_types = df['User Type'].value_counts().to_string()
    print(f"The total count of each user type: \n{count_of_user_types}\n")

    # Calculate and display counts of gender
    count_of_gender = df['Gender'].value_counts().to_string()
    print(f"The total count of each gender: \n{count_of_gender}\n")

    # Find and display earliest, most recent, and most common year of birth
    earliest_birth_year = df['Birth Year'].min()
    print(f"The earliest birth year on record is {m.floor(earliest_birth_year)}")
    
    most_recent_birth_year = df['Birth Year'].max()
    print(f"The most recent birth year on record is {m.floor(most_recent_birth_year)}")
    
    most_common_birth_year = df['Birth Year'].mode().iloc[0]
    print(f"The most common birth year on record is {m.floor(most_common_birth_year)}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        # Ask user which city they want to view stats for and then load the table into a data frame
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # Display stats about the selected city
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask user if they want to restart the query or not
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()