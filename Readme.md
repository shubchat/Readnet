# A recommender app for free short stories

![](usage_demo.gif)

The aim of development of this application is to develop a portal where anyone could go in and read for free.The reason they are free is that they are in public domain and have been maintained and aggregated by outstanding volunteer effort at [project guttenberg](https://www.gutenberg.org/).

Before you start using this repo I would highly recommend reading the accomapanied [tutorial blog](https://medium.com/analytics-vidhya/tutorial-on-development-of-an-ai-engine-for-recommending-great-short-stories-2e136b3afa27) that I wrote .It has a detailed explanation of context and explanation.

## Dependencies

- Postgres

## End to end development

There are six stage of development that need to be followed:

- Content creation
- Development of recommendation algorithm
- Development of backend database for storing text based recommendations
- Development of backend API to serve short stories and recomendations
- Development of a front end user interace for a great user experience
- Deployment of the webapp on Heroku

## Step-1:Content creation

### Data extract

All the short stories on readnet are free from copyright as that is the only way we could make it available for no charge to the readers. One of the largest repository for free out of copyright books and stories is [project guttenberg](https://www.gutenberg.org/) .<b>All the content that you would find on the site has been extracted from the guttenberg portal(Please consider a small [donation](https://www.gutenberg.org/wiki/Gutenberg:Project_Gutenberg_Needs_Your_Donation) to this outstanding initiative)<b>.

Running the script for [Data Extraction](Content_creation/Data_extract.py) will create a folder called books in the root directory and number of books you have asked to be downloaded would be placed as a text file in the [books](books) folder

Example:`python Content_creation/Data_extract.py 25` will download twenty five short stories in the books folder

### Data preparation

We would now need to extract metadata from all the text files which contain short stories.The information that we would be after are

- Book number
- Title
- Author
- Language

Post extracting this we would be pushing all the metadata into a table which would rest in a postgres database.
All of this can be achieved by using the [Data preparation script](Content_creation/Data_preparation.py).Below is an example for the same:

`python Content_creation/Data_preparation.py "user_name" "password" "books"`
Where,

- user_name-role under which you want to login to postgres
- password-Password if exists
- books-Name of the database to be created in postgres
  The above code will create a table <b>metadata<b> into a database called books on your locak postgres server.
