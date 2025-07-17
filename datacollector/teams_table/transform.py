import pandas as pd
import re
from config import TEAM_NAME_MAP, TEAM_CITY_MAP

def transform_teams_table(df):
    df = column_mapping(df)
    df = parse_playoffs_column(df)
    df = parse_record_column(df)
    
    df['team_id'] = df['team'] + '_' + df['year']
    df['name'] = df['team'].map(TEAM_NAME_MAP)
    df['city'] = df['team'].map(TEAM_CITY_MAP)
    df['coach'] = df['coach'].str.replace(r'\s*\(\d+-\d+-\d+\)', '', regex=True)
    df['pointsFor'] = df['pointsFor'].str.split(' ').str[0]
    df['pointsAgainst'] = df['pointsAgainst'].str.split(' ').str[0]
    df = df.drop(columns=['record'])
    return df

    
def column_mapping(df):
    col_map = {
        'Coach': 'coach',
        'Points For': 'pointsFor',
        'Points Against': 'pointsAgainst',
        'Record': 'record',
        'Playoffs': 'playoffs',
        'Offensive Coordinator': 'offCoordinator',
        'Defensive Coordinator': 'defCoordinator',
        'Stadium': 'stadium',
        'Offensive Scheme': 'offScheme',
        'Defensive Alignment': 'defAlignment',
        'team': 'team',
        'year': 'year',
        'logo': 'logo'
    }
    df = df.rename(columns=col_map)
    df = df[list(col_map.values())]
    return df
    

def parse_playoffs_column(df):
    def classify_playoffs(playoff_text):
        if pd.isna(playoff_text):
            return 'Missed Playoffs'
        elif 'Won Super Bowl' in playoff_text:
            return 'Won Super Bowl'
        elif 'Lost Super Bowl' in playoff_text:
            return 'Lost Super Bowl'
        elif 'Lost Conference Championship' in playoff_text:
            return 'Lost Conference Championship'
        elif 'Lost Divisional' in playoff_text:
            return 'Lost Divisional'
        elif 'Lost Wild Card' in playoff_text:
            return 'Lost Wild Card'
        else:
            return 'Unknown'

    df['playoffs'] = df['playoffs'].apply(classify_playoffs)
    return df


def parse_record_column(df):
    def extract_all_parts(record):
        if pd.isna(record):
            return pd.Series([None, None, None, None, None])

        match = re.search(r'(\d+)-(\d+)-(\d+),\s*(\d+)(?:st|nd|rd|th)\s+in\s*([A-Z]+ [A-Za-z]+)', record)
        if match:
            wins = int(match.group(1))
            losses = int(match.group(2))
            ties = int(match.group(3))
            division_rank = int(match.group(4))
            division = match.group(5)
            return pd.Series([wins, losses, ties, division_rank, division])
        else:
            return pd.Series([None, None, None, None, None])

    df[['wins', 'losses', 'ties', 'divisionRank', 'division']] = df['record'].apply(extract_all_parts)
    return df