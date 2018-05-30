# PrathamBooks
Code and documentation for the collaboration with PrathamBooks during Sprint' 2018 

### Problem Area: 
At the time of committing this readme file, Pratham Books' StoryWeaver platform has 8000+ books in 113 languages (70+ International languages and 30+ Indian Languages) distributed across 25+ categories with hundred of tags. As StoryWeaver scales up to host 20K stories over next year or so, discoverability of books (inside the StoryWeaver platform as well as across the web via search engines) could be a challenge. DataKind intends to solve this using various Natural Language Processing and Machine Learning tools out there.

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
