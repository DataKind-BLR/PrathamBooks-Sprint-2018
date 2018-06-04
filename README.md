# PrathamBooks
Code and documentation for the collaboration with PrathamBooks during Sprint' 2018 

### Problem Area: 
At the time of committing this readme file, Pratham Books' StoryWeaver platform has 8000+ books in 113 languages (70+ International languages and 30+ Indian Languages) distributed across 25+ categories with hundred of tags. As StoryWeaver scales up to host 20K stories over next year or so, discoverability of books (inside the StoryWeaver platform as well as across the web via search engines) could be a challenge. DataKind intends to solve this using various Natural Language Processing and Machine Learning tools out there.

### Data Description:

File Name: stories_pages.csv

	stories_pages.csv is the main table. It captures most of the attributes of the story including title, synopsis, content, language, reading level etc.

		story_id - Unique Numeric identifier for a story
		story_title - Title of the story
		story_english_title - Title of the English version of the story
		is_child_created_story - If the story created by a child 
		stories_status - If the story is published or not. A story may be in the draft status etc. In that case, it will not be published. 
		stories_summary - Synopsis of the story
		ancestry - Parent child relationship between different versions of the same story
		is_recommended_story - If the story is displayed as recommended on the StroyWeaver platform
		reads - Total Number of reads for the story
		language_name - Language of the story
		organization_name - If the story is from a Publisher, name of the Publisher/Organization.
		page_id - A Story consists of multiple pages. Numeric identifier of each page.
		page_content - Content of the page (if any).
		page_type - Type of the page
		story_derivation_type - If it's a original story or a derived (Translated or Releveled) one
		story_publishing_type - If it's from a Publisher or from a Community User
		reading_level_cat - Reading Level of the Story (1 - 4)

File Name : stories_categories.csv 

	stories_categories.csv table captures categories associated with each story

		story_id - Unique Numeric identifier for a story
		story_title - Title of the story
		story_english_title - Title of the English version of the story
		category_name - Name of the category associated with the story


File Name : stories_tags.csv

	stories_tags table captures tags associated with each story

		story_id - Unique Numeric identifier for a story
		story_title - Title of the story
		story_english_title - Title of the English version of the story
		story_tag_name - Name of the tag associated with the story

#### Proposed Project Structure
```
|
|- data
|    |- raw                     <- Original datadump supplied by Partner Organization
|    |- external                <- External data (if any)
|    |- processed               <- Final data after cleaning etc
|
|- r                            <- All code composed using R programming language live here
|  |- src                       <- Scripts for visualization, modeling etc
|  |- notebooks                 <- RMarkdown Notebooks
|  |- reports                   <- Generated analysis as HTML, PDF
|
|
|- python                       <- All code composed using python programming language live here
|        |- src                 <- Source code for visualization, modeling etc
|        |- notebooks           <- Jupyter Notebooks
|        |- reports.            <- Generated analysis as HTML, PDF
|        |- requirements.txt    <- The requirements file for reproducing the python analysis environment
|
|- readme.txt                   <- Readme file (YOU ARE HERE!)
```
