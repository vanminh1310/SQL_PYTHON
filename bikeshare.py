"""Udacity Python Project 2: Explore US Bikeshare Data."""
import time
import pandas as pd


CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
# get user input for city (chicago, new york city, washington).
    while True:
        city = input("Please enter the city you want to explore: ").lower()
        if city not in CITY_DATA:
            print("Please enter a valid city name!")
        else:
            print("You have chosen {}.".format(city.title()))
            break
# get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Please enter the month you want to explore: ").lower()
        if month not in months:
            print("Please enter a valid month!")
        else:
            print("You have chosen {}.".format(month.title()))
            break
# get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Please enter the day you want to explore: ").lower()
        if day not in days:
            print("Please enter a valid day!")
        else:
            print("You have chosen {}.".format(day.title()))
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Load data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['month'] = pd.to_datetime(df['Start Time']).dt.month
    df['day'] = pd.to_datetime(df['Start Time']).dt.day_name()

    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day'] == day.title()]

    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    month = ['January', 'February', 'March', 'April', 'May', 'June']
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    cm_month = month[df['month'].value_counts().idxmax()-1]
    print("The most common month is: ", cm_month)
    # display the most common day of week
    day_cm = df['day'].mode()[0]
    print("The most common day of week is: ", day_cm)
    # display the most common start hour
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    hour_common = df['hour'].mode()[0]
    print("The most common hour is: ", hour_common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    cm_start_station = df['Start Station'].value_counts().idxmax()
    print("The most commonly used start station is: ", cm_start_station)

    # display most commonly used end station
    cm_end_station = df['End Station'].value_counts().idxmax()
    print("The most commonly used end station is: ", cm_end_station)

    # display most frequent combination of start station and end station trip
    cm_start_end_station = df[['Start Station', 'End Station']].mode().iloc[0]
    print("The most frequent combination of start station and end station trip is: ",
          cm_start_end_station.iloc[0], " and ", cm_start_end_station.iloc[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Display statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    travel_time_seconds = df['Trip Duration'].sum()
    travel_time_days, remainder = divmod(
        travel_time_seconds, 86400)
    travel_time_hours, remainder = divmod(remainder, 3600)
    travel_time_minutes, travel_time_seconds = divmod(
        remainder, 60)

    print("The total travel time is: {} days, {} hours, {} minutes, and {} seconds".format(
        travel_time_days, travel_time_hours, travel_time_minutes, travel_time_seconds))

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time_minutes, mean_travel_time_seconds = divmod(
        mean_travel_time, 60)

    print("The mean travel time is: {} minutes and {} seconds".format(
        int(mean_travel_time_minutes), int(mean_travel_time_seconds)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Display statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("The counts of user types are: ", user_counts)

    if 'Gender' in df.columns:
        gender_cnt = df['Gender'].value_counts()
        print("The Gender count is", gender_cnt)
    else:
        print('Gender information is not available in this dataset.')

    if 'Birth Year' in df.columns:
        earliest_year = df['Birth Year'].min()
        print("The earliest year of birth is", int(earliest_year))
        most_recent_year = df['Birth Year'].max()
        print("The most recent year of birth is", int(most_recent_year))
        most_common_year = df['Birth Year'].mode()[0]
        print("The most common year of birth is", int(most_common_year))
    else:
        print('Birth Year information is not available in this dataset.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Display a specified number of rows of individual trip data from a DataFrame."""
    start_loc = 0
    while True:
        view_data = input(
            '\nWould you like to view 5 rows of data?  Enter yes or press Enter: ').lower()
        if view_data == 'yes' or view_data == '':
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
        else:
            break


def main():
    """Run the main program to analyze US bikeshare data."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
