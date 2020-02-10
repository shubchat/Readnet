# A recommender app for free short stories

![](usage_demo.gif)

The aim of development of this application is to develop a portal where anyone could go in and read for free.The reason they are free is that they are in public domain and have been maintained and aggregated by outstanding volunteer effort at [project guttenberg](https://www.gutenberg.org/).

Before you start using this repo I would highly recommend reading the accomapanied [tutorial blog](https://medium.com/analytics-vidhya/tutorial-on-development-of-an-ai-engine-for-recommending-great-short-stories-2e136b3afa27) that I wrote .It has a detailed explanation of context and explanation.

## Dependencies

- Postgres on your local machine

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

All the short stories on readnet are free from copyright as that is the only way we could make it available for no charge to the readers. One of the largest repository for free out of copyright books and stories is [project guttenberg](https://www.gutenberg.org/) .**All the content that you would find on the site has been extracted from the guttenberg portal(Please consider a small [donation](https://www.gutenberg.org/wiki/Gutenberg:Project_Gutenberg_Needs_Your_Donation) to this outstanding initiative)**.

Running the script for [Data Extraction](Content_creation/Data_extract.py) will create a folder called books in the root directory and number of books you have asked to be downloaded would be placed as a text file in the [books](books) folder

Example:`python Content_creation/Data_extract.py 25` will download twenty five short stories in the books folder

### Data preparation

We would now need to extract metadata from all the text files which contain short stories.The information that we would be after are

- Book number
- Title
- Author
- Language

In addition to this we would need the source text of short stories to be also stored in a table corresponding to the book numbers.

Post extracting these we would be pushing all the metadata into a metadata table and all stories into a short_stories tables both of this would rest in a postgres database .
All of this can be achieved by using the [Data preparation script](Content_creation/Data_preparation.py).Below is an example for the same:

`python Content_creation/Data_preparation.py "user_name" "password" "books"`
Where,

- user_name-role under which you want to login to postgres
- password-Password if exists
- books-Name of the database to be created in postgres

  The above code will create a table **metadata** and **short_stories** into a database called books on your local postgres server.

## Step2: Development of recommendation algorithm

We have now done the data extraction part,now is when we develop the logic/algorithm which helps us identify which stories are similar to each other.We have kept things really simple .

- Use [TFIDF](http://www.tfidf.com/) to vectorize each of the short stories
- Get a similarity between all the transformed vectors using [cosine similarity](https://www.sciencedirect.com/topics/computer-science/cosine-similarity)
- For each short story find five most similar short stories and push this information into a database

All of the above steps can be completed by using the script[Recom_logic/Algo.py](Recom_logic/Algo.py)

`python Recom_logic/Algo.py "books"`

Where:
books-Is the name of postgres DB already created which has the short_stories table which is used to generate the recommendations

## Step3:Development of backend database for storing text based recommendations

We don't need to go through this step seperately,we incorporated this as part of the first two steps where we have pushed three tables into a postgres database called books.The three tables are:

- metadata:Contains the metadata for all the short stories
- short_stories:content of all Short stories
- recos:For each short story what are the top five recommendations

## Step 4 & 5 :Development of backend API to serve short stories and recomendations & Development of a front end user interace for a great user experience

We are now in the part where we are developing a web application to serve short stories.Any web application would have two parts:

- A backend REST API to serve the content
- A front end system accepting the content for display

Both the steps are not isolated from each other,how we design the API would depend upon how we want the user interface to be displayed as.A basic bare bone design using a bootstrap template you would find withing the [webapp](webapp) folder.Structurally it contains the backend content being served using flask,the details of which you would find in [application.py](webapp/application.py) .

The only change you need to do is set up `DATABASE_URL` as an environment variable .In our case as we would add `export DATABASE_URL=postgresql:///stories"` in the bash_profile.

The front end is deployed using bootstrap and html templates.

## Step 6 : Deployment of the webapp on Heroku

We have done all the necessary ground work ,the only step that remains is how do we deploy it so that it is visible to everyone.Thi can easily be done by using n- number of providers .In my case the app is deployed on heroku at https://project-guttenberg.herokuapp.com/

You would find multiple instructions online of how to deploy as flask app on heroku but it in essence zooms out to:

- Have a requirement file(which we already have) for creating the environment for the webapp
- Migrate the Postgres Database to Heroku server
- Deploy the app (free or get your own domain)
