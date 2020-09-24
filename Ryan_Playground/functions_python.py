import pandas as pd

def combine_dfs_add_time(dataframe_date_list):
    """
    feed in a list of turnstyle dataframes dates
    returns the combined datafrae with columns for date time and day of week
    """
    dfs = []
    for date in dataframe_date_list:
        dfs.append(pd.read_csv('http://web.mta.info/developers/data/nyct/turnstile/turnstile_{}.txt'.format(date)))


    # concatenate the dataframes into one
    df = pd.concat(dfs, ignore_index=True)

    # rename the exits field
    df = df.rename(columns={'EXITS                                                               ': 'EXITS'})

    # create a new column that combines the day and time into one and makes it a datetime object
    df["DATE_TIME"] =  pd.to_datetime(df["DATE"] +" "+ df["TIME"])

    # add in a day of the week column
    df["DAY_INT"] = df["DATE_TIME"].dt.dayofweek

    # create a mapper to map the day of the week nubers to actual string values
    day_dict = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }

    # add that day of the week string column
    df["DAY_STR"] = df["DAY_INT"].map(day_dict)

    return df


def add_entry_and_exit_differences(df):
    """
    Takes in the dataframe with the date time column
    returns a data frame with a entry and exit diff column
    these new columns tell us how many people exuted/entered in that time period
    """

    # sort the dataframe by turnstyle date
    ordered_date_df = df.sort_values(by=['STATION', 'SCP','UNIT','C/A', 'DATE_TIME'])

    """
    group by station, scp, unit, and c/a to get the individual counters
    then take the difference in entries to get entry changes on each timestamp
    """
    ordered_date_df['ENTRIES_DIFF']=ordered_date_df.groupby(['STATION', 'SCP','UNIT','C/A'])['ENTRIES'].diff().fillna(0)

    """
    group by station, scp, unit, and c/a to get the individual counters
    then take the difference in exits to get exit changes on each timestamp
    """
    ordered_date_df['EXIT_DIFF']=ordered_date_df.groupby(['STATION', 'SCP', 'UNIT', 'C/A'])['EXITS'].diff().fillna(0)

    return ordered_date_df

def clean_entry_exit_values(df, max_val, min_val=0):
    """
    takes in a dataframe with the entry/exit diff columns and a max and min val for the entry diff
    returns a dataframe with the crazy values removed
    """

    # create mask to remove negative entries and exits or astronomically high differences
    pre_cleaning_rows = df.shape[0]
    cleaning_mask = (df["ENTRIES_DIFF"]>=min_val) & \
                    (df["EXIT_DIFF"]>=min_val) & \
                    (df["ENTRIES_DIFF"]<max_val) & \
                    (df["EXIT_DIFF"]<max_val)

    df = df[cleaning_mask]
    post_cleaning_rows = df.shape[0]
    print("You removed {} rows in the cleaning".format(pre_cleaning_rows-post_cleaning_rows))
    return df

def totals_combined_per_station(df):

    """
    takes in a dataframe with the entry/exit diff columns
    returns a dataframe with rows of avg entries, exits, and cobined for each station in desc order
    """

    # show the total entries and exits, it looks much better
    entries_exit_totals = df.groupby(["STATION"])[["ENTRIES_DIFF", "EXIT_DIFF"]].sum()

    # cobine the entries and exits and sort to get the most popuklar stations
    entries_exit_totals["COMBINED"] = entries_exit_totals["ENTRIES_DIFF"] + entries_exit_totals["EXIT_DIFF"]
    entries_exit_totals = entries_exit_totals.sort_values(by=["COMBINED"], ascending=False)

    return entries_exit_totals

def avg_combined_per_station(df):

    """
    takes in a dataframe with the entry/exit diff columns
    returns a dataframe with rows of total entries, exits, and cobined for each station in desc order
    """

    # show the total entries and exits, it looks much better
    entries_exit_totals = df.groupby(["STATION", "DATE"])[["ENTRIES_DIFF", "EXIT_DIFF"]].sum()
    entries_exit_avg = entries_exit_totals.groupby(["STATION"])[["ENTRIES_DIFF", "EXIT_DIFF"]].mean()

    # cobine the entries and exits and sort to get the most popuklar stations
    entries_exit_avg["COMBINED"] = entries_exit_avg["ENTRIES_DIFF"] + entries_exit_avg["EXIT_DIFF"]
    entries_exit_avg = entries_exit_avg.sort_values(by=["COMBINED"], ascending=False)

    return entries_exit_avg

def avg_per_day_of_week(df):
    """
    takes in a dataframe with the entry/exit diff columns
    returns a dataframe with rows of total entries, exits, and cobined for the avg traffic
    on each DAY OF WEEK for each station

    i.e. Station A on Monday
    """

    # return the avg usage per day of week per station on each day
    total_daily_per_station = df.groupby(['STATION', 'DATE','DAY_INT', 'DAY_STR',])["ENTRIES_DIFF", "EXIT_DIFF"].sum()

    # average out the traffic at each station grouped by day of the week
    avg_daily_per_station = total_daily_per_station.groupby(["STATION","DAY_INT", "DAY_STR"])["ENTRIES_DIFF", "EXIT_DIFF"].mean()

    # cobine the entries and exits and sort to get the most popuklar days at what stations
    avg_daily_per_station["COMBINED"] = avg_daily_per_station["ENTRIES_DIFF"] + avg_daily_per_station["EXIT_DIFF"]
    avg_daily_per_station.sort_values(by=["COMBINED"], ascending=False)

    return avg_daily_per_station

def avg_per_day_of_week_and_time(df):
    """
    takes in a dataframe with the entry/exit diff columns
    returns a dataframe with rows of total entries, exits, and cobined for the avg traffic
    on each DAY OF WEEK and TIME SLOT for each station

    i.e. Station A on Monday between 2-6 pm
    """

    # get the total traffic for each station at each hour of each day
    total_hourly_per_station = df.groupby(['STATION', 'DATE', 'DAY_INT', 'DAY_STR' ,'TIME'])["ENTRIES_DIFF", "EXIT_DIFF"].sum()

    # average out the traffic at each station grouped by day of the week and time slot
    avg_hourly_per_station = total_hourly_per_station.groupby(["STATION", 'DAY_INT', 'DAY_STR' ,"TIME"])["ENTRIES_DIFF", "EXIT_DIFF"].mean()

    # cobine the entries and exits and sort to get the most popular days and times at each stations
    avg_hourly_per_station["COMBINED"] = avg_hourly_per_station["ENTRIES_DIFF"] + avg_hourly_per_station["EXIT_DIFF"]
    avg_hourly_per_station.sort_values(by=["COMBINED"], ascending=False).head(50)

    return avg_hourly_per_station

def create_interested_colored_bar_graph(df, num_stations):

    """
    Takes in a dataframe that has combined data and total nscore data
    outputs a bar plot with the bars colored by score
    """

    color_mapper = {
        "7":'g',
        "6":'b',
        "5":'y',
        "4":'y',
        "3":'orange',
        "2":'r',
        "1":'r',
        "0":'r',
    }

    df["color"] = df["total score"].astype(str).map(color_mapper)

    return(df.head(num_stations).plot.bar(x='STATION', y='COMBINED', color=df["color"], figsize=(10,5)))
    plt.xticks(rotation=90);
