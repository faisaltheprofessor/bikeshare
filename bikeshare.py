import time
import pandas as pd
from PyInquirer import prompt, Separator
from essentials import style, display_label
from prettytable import PrettyTable

import os

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

CITIES = ['Chicago', 'New York', 'Washington']
MONTHS =  ['All', 'January','February','March','April', 'May', 'June']
DAYS = ['All', 'Monday', 'Tuesday',  'Wednesday', 'Thursday',  'Friday', 'Saturday', "Sunday"]

def get_filters():
    global city
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    display_label('\n\n \t\t\tHello! Let\'s explore some US bikeshare data!\n\n')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    questions = [
        {
            'type': 'list', 
            'qmark': '❓',
            'name': 'city',
            'message': "Select a city?",
            'choices': CITIES
        },
        {
            'type': 'checkbox', 
            'name': 'month',
            'qmark': '❓',
            'message': 'Select a month?',
            'choices': [
                {'name': 'January', 'checked': True},
                {'name': 'February'},
                {'name': 'March'},
                {'name': 'April'},
                {'name': 'May'},
                {'name': 'June'}
            ],
             "mandatory": True,
             "validate": lambda result: len(result) >= 1,
            "invalid_message": "should be at least 1 selection",
            "instruction": "(select at least 1)",
        },
        {
            'type': 'checkbox', 
            'name': 'day',
            'qmark': '❓',
            'message': 'Select a day?',
            'choices': [ 
                {'name': 'Monday', 'checked': True},
                {'name': 'Tuesday'},
                {'name': 'Wednesday'},
                {'name': 'Thrusday'},
                {'name': 'Friday'},
                {'name': 'Saturday'},
                {'name': 'Sunday'}
            ],
            "mandatory": True,
             "validate": lambda result: len(result) >= 1,
            "invalid_message": "should be at least 1 selection",
            "instruction": "(select at least 1)",

        },
    ]




    

    # get user input for month (all, january, february, ... , june)

    # get user input for day of week (all, monday, tuesday, ... sunday)

    answers = prompt(questions, style=style)
    city = answers['city'].lower()
    months = answers['month']
    days = answers['day']
    print('-'*45)
    return city, months, days

def load_data(city, months, days):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) months - name of the months to filter by, or "all" to apply no month filter
        (str) days - names of the days of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # city, month, day = get_filters(city, month, day)
    df = pd.read_csv(CITY_DATA[city])

    # Conversions and adding required columns   
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour


# Dealing with months
    if('All' not in months):
        selected_months = []
        for i in months:
            selected_months.append(MONTHS.index(i))
        df = df.loc[df.month.isin(selected_months)]
    
# Dealing with Days
    if('All' not in days):
        df = df.loc[df.day.isin(days)]
    

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # display the most common month
    common_month = MONTHS[ df['month'].mode()[0] ] 

    # display the most common day of week
    common_day =  df['day'].mode()[0]

    # display the most common start hour
    common_start_hour =  df['hour'].mode()[0]
   

    t = PrettyTable(['Common Month', 'Common Day', 'Common Start Hour'])
    t.add_row([common_month, common_day, common_start_hour])
    print(t)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*45)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    most_commonly_used_start_station = df['Start Station'].mode()[0]

    # display most commonly used end station
    most_commonly_used_end_station = df['End Station'].mode()[0]


    # display most frequent combination of start station and end station trip
    df['Frequent Combos'] =  df['Start Station'] + ' -> ' + df['End Station']
    most_frequent_start_and_end_station = df['Frequent Combos'].mode()[0]

    t = PrettyTable(['Common Start Station', 'Common End Station', 'Frequent Combos'])
    t.add_row([most_commonly_used_start_station, most_commonly_used_end_station, most_frequent_start_and_end_station])
    print(t)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""  
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = str(round(df['Trip Duration'].sum() / (60 * 60), 2)) + ' hours'
    # display mean travel time
    mean_travel_time = str(round(df['Trip Duration'].mean() / 60, 2)) + 'minutes'

    t = PrettyTable(['Total Travel Time', 'Mean Travel Time'])
    t.add_row([total_travel_time, mean_travel_time])
    print(t)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()[:2]



    # Display counts of gender
    if city == 'chicago' or city == 'new york':
        gender_count = df['Gender'].value_counts()
        earliest_birth_year = int(df['Birth Year'].min())
        most_recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode()[0])
    else:
        gender_count = 'Not Available'
        earliest_birth_year = 'Not Available'
        most_recent_birth_year = 'Not Available'
        most_common_birth_year = 'Not Available'
    # Display earliest, most recent, and most common year of birth
 
  


    t = PrettyTable(['User Type', 'Gender Count', 'Earliest Birth Year', 'Youngest Birth Year', 'Frequent Birth Year'])
    t.add_row([user_types, gender_count, earliest_birth_year, most_recent_birth_year, most_common_birth_year])
    print(t)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw_data(df):
    """ Your docstring here """
    i = 0
    raw = input("Do you also want to see the raw data? 'yes' or 'no' \n") # TO DO: convert the user input to lower case using lower() function
    pd.set_option('display.max_columns',200)

    while True:            
        if raw == 'no':
            break
        elif raw == 'yes':
            print(df[i:i+5]) # TO DO: appropriately subset/slice your dataframe to display next five rows
            raw = input("Continue? 'yes' or 'no'\n") # TO DO: convert the user input to lower case using lower() function
            i += 5
        else:
            raw = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()

def main():
    while True:
        os.system('clear')
        city, months, days = get_filters()    
        df = load_data(city, months, days)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)
        
        restart = input("Restart the program? 'yes' or 'no' \n")    
        while True:            
            if restart == 'no':
                exit()
            elif restart == 'yes':
                main()
            else:
                restart = input("\nYour input is invalid. Please enter only 'yes' or 'no'\n").lower()


if __name__ == "__main__":
    main()
