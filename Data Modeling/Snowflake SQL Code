CREATE TABLE GenreDim(
genre_id integer unique,
genre_name varchar(50)
);

CREATE TABLE PlatformDim(
platform_id integer primary key,
platforms_name varchar(50));

CREATE TABLE GameDim(
game_id integer primary key,
game_name varchar,
release_date DATE);

Create Table LocalizationsDim(
localkey number identity(1,1) primary key,
localization varchar);

INSERT INTO GameDim(game_id, game_name, release_date)
SELECT DISTINCT "game_id", "game_name", "release_date"
FROM "VIDEOGAMETABLE";

INSERT into GenreDim(genre_id, genre_name)
select distinct "genre_id", "genre"
from "VIDEOGAMETABLE";

Insert into PlatformDim(platform_id, platforms_name)
select distinct "platform_id", "platforms"
from "VIDEOGAMETABLE";

Insert into LocalizationsDim(localization)
select distinct "game_localizations"
from "VIDEOGAMETABLE";


Create table FactsTable (
factskey number identity(1,1) primary key,
gameid integer,
genreid integer,
platformid integer,
local_key integer,
game_rating float,

foreign key (gameid) references GameDim(game_id),
foreign key (genreid) references GenreDim(genre_id),
foreign key (platformid) references PlatformDim(platform_id),
foreign key (local_key) references LocalizationsDim(localkey));

INSERT INTO FactsTable (gameid, genreid, platformid, local_key,game_rating)
SELECT
GameDim.game_id,
GenreDim.genre_id,
PlatformDim.platform_id,
l.localkey,
"total_rating"
FROM "VIDEOGAMETABLE"
join LocalizationsDim l on l.localization = VIDEOGAMETABLE."game_localizations"
join GameDim on GameDim.game_id = videogametable."game_id"
join GenreDim  on GenreDim.genre_id = videogametable."genre_id"
join PLATFORMDIM  on PLATFORMDIM.platform_id =  videogametable."platform_id";
