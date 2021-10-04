import numpy as np
import plotly.express as px

def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Medal', 'Event'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')
    print(x)

    return x


def medal_tally(df):
    medal_tally=df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Medal','Event'])
    medal_tally=medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',
                                                                                            ascending=False).reset_index()
    medal_tally['total']=medal_tally['Gold']+medal_tally['Silver']+medal_tally['Bronze']

    medal_tally['Gold']=medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')


    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
    nations_over_time.rename(columns={'index': 'Editions', 'Year': col}, inplace=True)

    return nations_over_time


def male_female(df):
    temp_df = df.drop_duplicates(['Year', 'Sport', 'Name'])
    temp_df = temp_df[['Year', 'Sex']].value_counts().reset_index().sort_values('Year')
    male_df = temp_df[temp_df['Sex'] == 'M']
    female_df = temp_df[temp_df['Sex'] == 'F']

    female_df.rename(columns={0: 'count'}, inplace=True)

    male_df.rename(columns={0: 'count'}, inplace=True)

    fig = px.line()

    fig.add_scatter(x=female_df['Year'], y=female_df['count'], name="Female")
    fig.add_scatter(x=male_df['Year'], y=male_df['count'], name="Male")
    return fig

# top 15 athletes of all time

def most_successful(df, sport):
    temp_df=df.dropna(subset=['Medal'])
    if sport!='Overall':
        temp_df=temp_df[temp_df['Sport']==sport]
    x=temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='index',right_on='Name', how='left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    x.rename(columns={'index':'Name','Name_x':'Medals'},inplace=True)
    return x

def yearwise_medaltally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Year', 'Event', 'Medal', 'region'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby(['Year']).count()['Medal'].reset_index()
    return final_df


def country_sport_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(['Year', 'Event', 'Medal', 'region'], inplace=True)
    new_df = temp_df[temp_df['region'] ==country ]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt


def top_athletes_of_country(df,country):
    temp_df = df[df['region'] == country]
    temp_df = temp_df.dropna(subset=['Medal'])
    temp_df = temp_df.groupby(['Name','Sport']).count()['Medal'].reset_index().sort_values('Medal', ascending=False).head(10)
    return temp_df


# athletes medals ---------------------------------------------------------

def atheletes_medal(df, Name):
    athletes_df = df.dropna(subset=['Medal'])
    x = athletes_df[athletes_df['Name'] == Name].groupby(['Year']).count()
    new_df = x['Medal'].reset_index()
    new_df.rename(columns={'Medal': 'Medals', 'Year': 'Edition'})

    return new_df


def ath_country(df, Name):
    x = df[df['Name'] == Name]
    team = x['Team'].unique()[0]
    sport = x['Sport'].unique()[0]
    year = x['Year'].unique()
    y=len(year)
    return team, sport, y
