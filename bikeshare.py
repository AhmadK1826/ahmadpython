

import pandas as pd
import numpy as np

# Refactor: improved clarity in comments and variable names
def load_data(city):
    """
    Load the CSV for the specified city and add time-derived columns.

    Args:
        city (str): City name; expected one of {'chicago', 'new york city', 'washington'} (case-insensitive).

    Returns:
        pandas.DataFrame: DataFrame with columns:
            - Start Time (datetime)
            - month (int: 1..12)
            - day_of_week (str: e.g., 'Monday')
            - hour (int: 0..23)
        along with the original dataset columns.
    """
    CITY_DATA = {
        'chicago': 'chicago.csv',
        'new york city': 'new_york_city.csv',
        'washington': 'washington.csv'
    }
    df = pd.read_csv(CITY_DATA[city.lower()])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    return df


def load_data_filtered(city, month=None, day=None):
    """
    Load data for a city and apply optional filters for month and day.

    Args:
        city (str): City name (as in load_data).
        month (str, optional): Month name (e.g., 'January'..'June'), case-insensitive.
                               If None or 'all', no month filter is applied.
        day (str, optional): Day name (e.g., 'Monday'..'Sunday'), case-insensitive.
                             If None or 'all', no day filter is applied.

    Returns:
        pandas.DataFrame: Filtered DataFrame.
    """
    df = load_data(city)

    if month and month.lower() != 'all':
        # Validate month against allowed set January..June
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        m = month.strip().lower()
        if m not in months:
            raise ValueError("Invalid month. Choose one of January–June or 'all'.")
        month_number = months.index(m) + 1
        df = df[df['month'] == month_number]

    if day and day.lower() != 'all':
        # Validate day against allowed set Monday..Sunday
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        d = day.strip().lower()
        if d not in days:
            raise ValueError("Invalid day. Choose a day Monday–Sunday or 'all'.")
        df = df[df['day_of_week'].str.lower() == d]

    return df


def most_common_hour(df):
    """
    Return the most frequent start hour.

    Args:
        df (pandas.DataFrame): DataFrame after any filtering.

    Returns:
        int: The most common hour (0..23).
    """
    return int(df['hour'].mode()[0])


def user_types_count(df):
    """
    Return counts of user types.

    Args:
        df (pandas.DataFrame): DataFrame after any filtering.

    Returns:
        pandas.Series: Value counts for 'User Type'.
    """
    return df['User Type'].value_counts()


def gender_count(df):
    """
    Return counts of gender if the 'Gender' column exists, else raise KeyError.

    Args:
        df (pandas.DataFrame): DataFrame after any filtering.

    Returns:
        pandas.Series: Value counts for 'Gender'.
    """
    return df['Gender'].value_counts()


def birth_year_stats(df):
    """
    Compute earliest, most recent, and most common birth years.

    Args:
        df (pandas.DataFrame): DataFrame after any filtering.

    Returns:
        tuple[int, int, int]: (earliest_year, most_recent_year, most_common_year)
    """
    earliest_year = int(df['Birth Year'].min())
    most_recent_year = int(df['Birth Year'].max())
    most_common_year = int(df['Birth Year'].mode()[0])
    return earliest_year, most_recent_year, most_common_year


def most_common_month(df):
    """
    Return the most frequent month number in the data.

    Args:
        df (pandas.DataFrame): DataFrame after any filtering.

    Returns:
        int: Month number (1..12).
    """
    return int(df['month'].mode()[0])


def most_common_day(df):
    """
    Return the most frequent day of week name in the data.

    Args:
        df (pandas.DataFrame): DataFrame after any filtering.

    Returns:
        str: Day name (e.g., 'Monday').
    """
    return df['day_of_week'].mode()[0]


def total_travel_time(df):
    """
    Return total trip duration in seconds.

    Args:
        df (pandas.DataFrame): DataFrame after any filtering.

    Returns:
        int: Sum of 'Trip Duration'.
    """
    return int(df['Trip Duration'].sum())


def average_travel_time(df):
    """
    Return average trip duration in seconds.

    Args:
        df (pandas.DataFrame): DataFrame after any filtering.

    Returns:
        float: Mean of 'Trip Duration'.
    """
    return float(df['Trip Duration'].mean())


def most_common_stations(df):
    """
    Return the most common start station, end station, and trip string.

    Args:
        df (pandas.DataFrame): DataFrame after any filtering.

    Returns:
        tuple[str, str, str]: (start_station, end_station, "Start to End").
    """
    common_start_station = df['Start Station'].mode()[0]
    common_end_station = df['End Station'].mode()[0]
    df['Trip'] = df['Start Station'] + " to " + df['End Station']
    common_trip = df['Trip'].mode()[0]
    return common_start_station, common_end_station, common_trip


def display_raw_data(df):
    """
    Interactively print 5-line chunks of raw data until the user says 'no'.

    Args:
        df (pandas.DataFrame): DataFrame after any filtering.
    """
    start = 0
    while True:
        show_data = input("Do you want to see 5 lines of raw data? Enter yes or no: ").strip().lower()
        if show_data != 'yes':
            break
        print(df.iloc[start:start + 5])
        start += 5


def main():
    """
    Interactive loop:
    - Ask for city (validated with try/except),
    - Ask for month/day filters (validated with try/except),
    - Compute and print required statistics,
    - Offer raw data display,
    - Ask to restart.
    """
    while True:
        # City input with validation
        while True:
            try:
                city = input("Enter city name (Chicago, New York City, Washington): ").strip().lower()
                if city not in ['chicago', 'new york city', 'washington']:
                    raise ValueError("City not supported.")
                break
            except ValueError:
                print("Invalid city name. Please enter either Chicago, New York City, or Washington.\n")

        # Month input with validation
        while True:
            try:
                month = input("Enter month name (e.g. January) or 'all' for no filter: ").strip().lower()
                months = ['january', 'february', 'march', 'april', 'may', 'june']
                if month != 'all' and month not in months:
                    raise ValueError("Month must be between January and June or 'all'.")
                break
            except ValueError:
                print("Invalid month. Please choose one of January–June or 'all'.\n")

        # Day input with validation
        while True:
            try:
                day = input("Enter day of week (e.g. Monday) or 'all' for no filter: ").strip().lower()
                days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                if day != 'all' and day not in days:
                    raise ValueError("Day must be Monday–Sunday or 'all'.")
                break
            except ValueError:
                print("Invalid day. Please choose a day name Monday–Sunday or 'all'.\n")

        # Load and filter
        if month != 'all' and day != 'all':
            try:
                df = load_data_filtered(city, month, day)
            except ValueError as e:
                print(f"Input error: {e}\n")
                continue
        elif month != 'all':
            try:
                df = load_data_filtered(city, month=month)
            except ValueError as e:
                print(f"Input error: {e}\n")
                continue
        elif day != 'all':
            try:
                df = load_data_filtered(city, day=day)
            except ValueError as e:
                print(f"Input error: {e}\n")
                continue
        else:
            df = load_data(city)

        print(f"\nCalculating statistics for {city.title()}.\n")
        print("Data successfully loaded and analysis in progress...")
        print(f"Most common month: {most_common_month(df)}")
        print(f"Most common day of week: {most_common_day(df)}")
        print(f"Most common start hour: {most_common_hour(df)}")

        start_station, end_station, trip = most_common_stations(df)
        print(f"Most common start station: {start_station}")
        print(f"Most common end station: {end_station}")
        print(f"Most common trip: {trip}")

        print(f"Total travel time: {total_travel_time(df)} seconds")
        print(f"Average travel time: {average_travel_time(df):.2f} seconds")

        user_types = user_types_count(df)
        print(f"Counts of user types:\n{user_types}")

        # Gender/Birth Year only for Chicago and NYC (not available in Washington)
        if city in ['chicago', 'new york city']:
            gender = gender_count(df)
            print(f"Counts of gender:\n{gender}")

            earliest, recent, common = birth_year_stats(df)
            print(f"Earliest year of birth: {earliest}")
            print(f"Most recent year of birth: {recent}")
            print(f"Most common year of birth: {common}")

        display_raw_data(df)

        restart = input("\nWould you like to restart? Enter yes or no: ").strip().lower()
        if restart != 'yes':
            break

# Entry point for running the bikeshare program directly
if __name__ == "__main__":
    main()
