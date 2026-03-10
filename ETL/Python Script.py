import pandas as pd
import requests as request
import matplotlib.pyplot as mat
import snowflake.connector
import psycopg2
from snowflake.connector.pandas_tools import write_pandas
import requests as req
import time
import datetime

conn = snowflake.connector.connect(
    user="ommitted for confidentiality",
    password="ommitted for confidentiality",
    account="ommitted for confidentiality",
    warehouse="VIDEOGAMEWAREHOUSE",
    database="VIDEOGAMEDATABASE",
    schema="PUBLIC"
)

cur = conn.cursor()

#Create an empty list that we will add video games onto later.
Gamelist = []

#Establish header that will be used to gather API information.
header = {
    "Client-ID":"ommitted for confidentiality",
    "Authorization":"ommitted for confidentiality"
}
#Get the count of total games in the database with the specified fields.
gamecountbody = 'query games/count "Number of Games" {fields name, platforms.platform_family.name, total_rating, genres, genres.name, first_release_date, game_localizations.region, game_localizations.region.name;where platforms.platform_family.name != null;};'
gamecountlink = "https://api.igdb.com/v4/multiquery"
gamecountreq = req.post(url=gamecountlink,data=gamecountbody,headers=header)
gamecountJSON = gamecountreq.json()[0]['count']

#Extract data from api, with offset increasing to grab all available data and bypass request limit.
offset = 0
gameslink = 'https://api.igdb.com/v4/games'
while len(Gamelist) < gamecountJSON:
    gamesloop = f'fields name, platforms.platform_family.name, platforms.name, total_rating, genres, genres.name, first_release_date, game_localizations.region, game_localizations.region.name;limit 500; offset {offset}; where platforms.platform_family.name != null;'
    gamesrequest = req.post(url=gameslink,data=gamesloop,headers=header)
    Gamelist.extend(gamesrequest.json())
    offset += 500
    print(len(Gamelist))
    time.sleep(0.5)
else:
    print("done!")

#Convert list to dataframe for cleaning, export raw data for github repo
VideoGamesDf = pd.DataFrame(Gamelist)
VideoGamesDf.to_csv("rawvideogamedata.csv")


#remove null rows, get individual genres for each game
VideoGamesDf = VideoGamesDf.dropna().explode(column='genres')
VideoGamesDf['genresupdated'] = VideoGamesDf['genres'].apply(lambda x:x['name'])
VideoGamesDf['genreidupdated'] = VideoGamesDf['genres'].apply(lambda x:x['id'])

#Make seperate columns for platformids and platformname. Grab the updated platformid and updated platformname from their original column. 
VideoGamesDf = VideoGamesDf.explode(column='platforms')
VideoGamesDf['platformid'] = VideoGamesDf['platforms'].apply(lambda x:x.get('platform_family')['id'] if x.get('platform_family') else x.get('id'))
VideoGamesDf['UpdatedPlatforms'] = VideoGamesDf['platforms'].apply(lambda x:x.get('platform_family')['name'] if x.get('platform_family') else x.get('name'))

#Get Individual localizations for each game
VideoGamesDf = VideoGamesDf.explode(column='game_localizations')
VideoGamesDf['game_localizations'] = VideoGamesDf['game_localizations'].apply(lambda x:x.get('region')['name'])

#Convert the release date from a UNIX timestamp to MM-DD-YYYY format. Rename first_release_date to release_date.
VideoGamesDf['first_release_date'] = VideoGamesDf['first_release_date'].apply(lambda x: datetime.datetime.fromtimestamp(float(x))).dt.strftime("%Y-%m-%d")
VideoGamesDf = VideoGamesDf.rename(columns={'first_release_date':'release_date'})

#Now that we have all the cleaned platforms and columns, we can drop the original columns along with duplicates.
VideoGamesDf = VideoGamesDf.drop(columns=['genres', 'platforms']).drop_duplicates()
VideoGamesDf = VideoGamesDf.rename(columns={'genresupdated':'genre','genreidupdated':'genre_id','id':'game_id','name':'game_name','UpdatedPlatforms':'platforms','platformid':'platform_id'})

#Round game ratings to nearest tenth.
VideoGamesDf['total_rating'] = round(VideoGamesDf['total_rating'],1)
VideoGamesDf

success, nchunks, nrows, output = write_pandas(
    conn,
    VideoGamesDf,
    table_name='VIDEOGAMETABLE',
    auto_create_table=True,
    overwrite=False # Optional: set to True to replace existing table data
)

cur.close()
