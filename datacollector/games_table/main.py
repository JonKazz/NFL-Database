from .ingest import scrape_team_game_logs
from .transform import game_mapping
from .load import create_games_table, insert_df

def run():
    print("Scraping team game logs...")
    df = scrape_team_game_logs()
    print("Transforming columns...")
    df = game_mapping(df)
    print("Creating games table...")
    create_games_table()
    print("Inserting into database...")
    insert_df(df)
    print("Done.")