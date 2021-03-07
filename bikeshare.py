import time
import pandas as pd
import numpy as np

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
    print('\nHello! Let\'s explore some US bikeshare data!')
    print("")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while city not in {"chicago", "new york city", "washington"}:
        city = input("Please enter the city name: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = ""
    while month not in {"all", "january", "february", "march", "april", "may", "june"}:
        month = input("Please enter the month name or write all to select all the months: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = ""
    while day not in {"all", "saturday", "sunday", "monday", "tuesday", "wednesday", "thursday", "friday"}:
        day = input("Please enter the day name or write all to select all the days: ").lower()


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    # print(df.head())
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if len(df.groupby(["month"]).size()) > 1:
        mc_month = df.groupby(["month"]).size().idxmax() - 1
        print("The most common month of travel is: ", months[mc_month])
    else:
        current_month = df["month"].unique()[0] - 1
        print("There is no the most common month since you have selcted one month which is: ", months[current_month])

    # display the most common day of week
    if len(df.groupby(["day_of_week"]).size()) > 1:
        mc_day = df.groupby(["day_of_week"]).size().idxmax().lower()
        print("The most common day of travel is: ", mc_day)
    else:
        current_day = df["day_of_week"].unique()[0].lower()
        print("There is the no most common day since you have selected one day which is: ", current_day)

    # display the most common start hour
    mc_hour = df.groupby(["hour"]).size().idxmax()
    print("The most common hour of travel is: ", mc_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_s_station = df.groupby(["Start Station"]).size().idxmax()
    print("The most common start station is: ", mc_s_station)

    # display most commonly used end station
    mc_e_station = df.groupby(["End Station"]).size().idxmax()
    print("The most common end station is: ", mc_e_station)

    # display most frequent combination of start station and end station trip
    mc_combined_station = df.groupby(["Start Station", "End Station"]).size().idxmax()
    print("The most frequent combination of start and end station trip is {} and {}".format(mc_combined_station[0], mc_combined_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    tot_time = df["Trip Duration"].sum()
    print("Total travel time:", tot_time, "in seconds.")

    # Prints total time in format hh:mm:ss
    print("Total travel time in the form hh:mm:ss is:", str( int( (tot_time / 3600) ) ) + ":" +
          str( int(  ( (tot_time % 3600) / 60 )  ) ) + ":" +
          str( int( ( (tot_time % 3600) % 60 ) ) ) )

    # display mean travel time
    mean_time = df["Trip Duration"].mean()
    print("\nMean travel time:", mean_time, "in seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users. Notice that the data for Washington doesn't have
    the column for Gender and Birth Year. Therefore the function executes a conditional statement to check
    which data is under consideration."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    for i in range(0, len(user_types)):
        print("The counts of {} is {}.".format(user_types.index[i], user_types[i]))

    print("")
    # Display counts of gender
    # user_gender = df['Gender'].value_counts()
    if city in ['chicago','new york city']:
        user_gender = df.groupby(['Gender']).size()
        for i in range(0, len(user_gender)):
            print("The counts of {} is {}.".format(user_gender.index[i], user_gender[i]))

        print("")

        # Display earliest, most recent, and most common year of birth
        print("The earliest year of birth is: ", df['Birth Year'].min())
        print("The most recent year of birth is: ", df['Birth Year'].max())
        print("The most common year of birth is: ", df['Birth Year'].mode()[0])
    else:
        print("The data in the washington file does not include columns for Gender and Birth Year.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        row = 0
        while True:
            viewData = input("\nWould you like to see the raw data? Type 'Yes' or 'No'.\n")
            if viewData == "Yes":
                print(df.iloc[row:row+5, :])
                row += 5
            else:
                break

        restart = input('\nWould you like to restart? Enter Yes or No.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
