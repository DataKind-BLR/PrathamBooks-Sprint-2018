import pandas as pd

FILE_LOCATION = '../data/raw/spi_cleaned.csv'
df = pd.read_csv(FILE_LOCATION)

def get_illustration_text(story_id):
    return df.loc[df['story_id'] == int(story_id)]['illustration_text'].iloc[0]
