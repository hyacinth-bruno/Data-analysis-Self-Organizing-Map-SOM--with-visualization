import time
import pandas as pd
import numpy as np
from minisom import MiniSom
import matplotlib.pyplot as plt


from bikeshare import display_raw_data, station_stats, trip_duration_stats, user_stats


CITY_DATA = { "chicago": "chicago.csv",
              "new york city": "new_york_city.csv",
              "washington": "washington.csv" }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("ENTER CITY NAME: ").lower()
    while city not in ["chicago", "new york city", "washington"]:
        city = input("CHOOSE APPROPRIATE CITY: ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("ENTER MONTH: ").lower()
    while month not in ["all", "january", "february", "march", "april", "may", "june"]:
        month = input ("ENTER APPROPRIATE MONTH: ").lower()
        

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter day of the week: ").lower()
    while day not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        day = input("Enter appropriate day of the week: ").lower()

   

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
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        
        df = df[df['month'] == month]
        
        
    # df['day_of_week'] = df['Start Time'].dt.weekday
    df['day_of_week'] = df['Start Time'].dt.day_name()

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    #Returns the highest count of the most frequent month
    print("\n\nThe most common month is: ", df['month'].value_counts().idxmax())

    # TO DO: display the most common day of week
    #Returns the highest count of the most frequent week
    print("The most common day is: ", df['day_of_week'].value_counts().idxmax())

    # TO DO: display the most common start hour
    #Returns the highest count of the frequent common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common hour is: ", df['hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
	#Displays the highest count of the most commonly used start station
    print("\n\nThe most common start station is: ", df ['Start Station'].value_counts().idxmax())

    # TO DO: display most commonly used end station
	#Displays the highest count of the most commonly used end station
    print("The most common end station is: ", df['End Station'].value_counts().idxmax())

    # TO DO: display most frequent combination of start station and end station trip
    print("The most frequent combination of start station and end station trip: ")
    mostCommon_start_and_end_statition = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    print(mostCommon_start_and_end_statition)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
        
    total_duration = df['Trip Duration'].sum() / 3600.0
    print("total travel time in hours is: ", total_duration)

    # TO DO: display mean travel time
    mean_duration = df['Trip Duration'].mean() / 3600.0
    print("\n\nmean travel time in hours is: ", mean_duration)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)



def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())
        

    # TO DO: Display counts of gender
    if "Gender" in df:
        print(df['Gender'].value_counts())

        # TO DO: Display earliest, most recent, and most common year of birth
    if "Birth Year" in df:
        print("The earliest year of birth is:",int(df['Birth Year'].min()),
                "\nMost recent one is:",int(df['Birth Year'].max()),
                "\nMost common one is: ",int(df['Birth Year'].value_counts().idxmax()))

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def display_raw_data(df):
    """ Your docstring here """
    i = 0
    raw = input("<Do you want to see the raw data? Yes or No?>").lower() # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df.iloc[i:i+5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("<Do you want to see more? Yes or No>").lower() # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'YES' or 'NO'\n").lower()




def som_analysis(df):
    # Extract relevant features: start hour, travel duration, and day of the week
    features = df[['hour', 'Trip Duration']].copy()
    features['day_of_week'] = df['Start Time'].dt.weekday
    features = features.values

    # Normalize the features
    feature_range = features.max(axis=0) - features.min(axis=0)
    feature_range[feature_range == 0] = 1  # Avoid division by zero
    features = (features - features.min(axis=0)) / feature_range

    # Create and train the SOM
    som = MiniSom(6, 6, input_len=features.shape[1], random_seed=42)
    som.train_random(features, 5000)

    # # Create and train the SOM with 10 by 10 grid
    # som = MiniSom(10, 10, input_len=features.shape[1], random_seed=42)
    # som.train_random(features, 5000)

 # Visualization code
    plt.figure(figsize=(10, 10))
    plt.pcolor(som.distance_map().T, cmap='bone_r')  # plotting the distance map as background
    plt.colorbar()
    plt.axis([0, som.get_weights().shape[0], 0, som.get_weights().shape[1]])
    plt.title('Self-Organizing Map (U-Matrix)')
    plt.show()

    # You can now use the trained SOM for visualization or further analysis.
    # For example, print the winning nodes for the first 5 entries:
    for i in range(5):
        winner = som.winner(features[i])
        print(f"Winning node for entry {i}: {winner}")



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df['hour'] = df['Start Time'].dt.hour  # Add hour column for SOM analysis

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        # Add SOM analysis
        som_analysis(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
    main()