import os
import argparse
from bs4 import BeautifulSoup, Comment
import pandas as pd
import numpy as np
import warnings


"""This script is used to clean the stories data received from Pratham Books (stories_pages.csv). 
The output of the script will be two csv files. Once csv file consisting of only stories in English 
(stories_content_english.csv) and another file consisting of stories of all languages 
(stories_content_all_language). 

Usage:

    $ python clean_stories_data.py -i <Input_Directory>/datakind.csv -o <Output_Directory>

    For example:

    python clean_stories_data.py -i /vssexclude/ds/PrathamBooks/data/raw/datakind.csv -o /vssexclude/ds/PrathamBooks/python/notebooks/

"""

def remove_html_tags(html_text):
    '''
    Utility function to extract meaningful information from html tags
    using beautiful soup
    '''
    soup = BeautifulSoup(html_text, 'html.parser')
    
    for style_tag in soup.findAll('style'):
        style_tag.replace_with('')
    return(soup.get_text(separator=" ", strip=True))

def check_if_path_exists(path):
    '''
    Utility function to check if a file or directory path exists
    '''
    os_path = os.path.abspath(path)
    if not os.path.exists(os_path):
        print("ERROR : Path provided as an argument does not exist :", path)
        exit()
    else:
        return os_path

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="path of the raw stories file ", required=True)
parser.add_argument("-o", "--output", help="path to cleaned csv file", required=True)
args = parser.parse_args()

# Suppress pandas warnings 
# TODO Address the warnings instead of ignoring those
warnings.filterwarnings('ignore')

# Read the input file name and output directory name
file_in = args.input
file_out = args.output

# Validate if the input path exists
ip_path = check_if_path_exists(file_in)
# All good. Print the location of the input file
print("Location of the raw pages data:", ip_path)

# Validate if the output path exists
op_path = check_if_path_exists(file_out)
# All good. Print the location of the output file
print("Directory where output will be generated:", op_path)


print("Reading raw data....")
# Load the data
df_raw = pd.read_csv(file_in, sep=',')
print("Total number of pages:", df_raw.shape[0])
print("Number of unique stories:", df_raw.story_id.nunique())

# Get the index of the pages (rows) for which we have not-null content
not_null_index = df_raw.index[df_raw['page_content'].notnull()]
print("Total number of pages with not null content:", len(not_null_index))

print("Extracting meaningful content from html pages. It may take some time....")
# For each page, extract meaningful information from within html tags
# This takes some time as it uses apply function which is not vectorized
df_raw['page_content'].iloc[not_null_index] = df_raw.iloc[not_null_index]['page_content'].apply(lambda x : remove_html_tags(x))
print("Extraction of meaningful content from html pages is completed.")

# Remove new lines, carriage returns and tabs from page_content
df_raw.page_content = df_raw.page_content.str.replace("\n", " ")
df_raw.page_content = df_raw.page_content.str.replace("\r", " ")
df_raw.page_content = df_raw.page_content.str.replace("\t", " ")

# Remove new lines, carriage returns and tabs from summary of stories
df_raw.stories_summary = df_raw.stories_summary.str.replace("\n", " ")
df_raw.stories_summary = df_raw.stories_summary.str.replace("\r", " ")
df_raw.stories_summary = df_raw.stories_summary.str.replace("\t", " ")

# Now that meaningful data has been extracted, filter further. Get the stories pages which have valid content.
df_stories_with_story_pages = df_raw[(df_raw.page_content.notnull())]

print("Total number of pages with meaningful content:", df_raw.shape[0])
print("Number of unique stories with meaningful content:", df_raw.story_id.nunique())

# 'position' column indicates order of appearance of pages inside a story
df_stories_with_story_pages.sort_values(['story_id', 'position'], inplace=True)

# For every story (based on story_id), merge the content spread across multiple pages.
merged_story_pages = df_stories_with_story_pages.groupby('story_id')['page_content'].apply(lambda x : x.str.cat(sep=" ")).reset_index()

# Now that we have a separate DataFrame with merged story content, we don't need multiple rows 
# representing pages. Drop those.
df_stories_with_story_pages_dupl_removed = df_stories_with_story_pages.drop_duplicates(subset=['story_id'])
df_stories_with_story_pages_dupl_removed.drop("page_content", 'columns', inplace=True)

# Merge the two DataFrames
df_stories_with_content = pd.merge(left=df_stories_with_story_pages_dupl_removed, right=merged_story_pages, how='left', on='story_id')

# Rename the column name. We no longer have page level content, But we have story level content
df_stories_with_content.rename(columns={'page_content': 'story_content'}, inplace=True)
df_stories_with_content.drop(['position', 'page_id'], 'columns', inplace=True)


print("Recheck : Number of unique stories with meaningful content:", df_raw.story_id.nunique())

# Dump the content of English stories only!
location_of_english_csv = os.path.join(op_path, "stories_content_english.csv")
print("Writing stories in English at " + location_of_english_csv)
df_stories_with_content[df_stories_with_content.language_name == "English"].to_csv(location_of_english_csv, sep=",", index=False)
print("Number of English stories with meaningful content:", 
	df_stories_with_content[df_stories_with_content.language_name == "English"]['story_id'].nunique())

# Dump content of all stories
location_of_all_language_csv = os.path.join(op_path, "stories_content_all_language.csv")
print("Writing stories in English at " + location_of_all_language_csv)
df_stories_with_content.to_csv(location_of_all_language_csv, sep=",", index=False)
print("Number of stories in different languages with meaningful content:", 
	df_stories_with_content['story_id'].nunique())
