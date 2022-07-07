library(pkgload)
library(devtools)
library(lodown)
library(dplyr)
library(readr)

# Unzip gz title.ratings file from directory, read tsv file
df_ratings <- df_basics <- R.utils::gunzip('title.ratings.tsv.gz')
df_ratings <- read_tsv('title.ratings.tsv', na = "\\N", quote = '')

# Unzip gz title.basics file from directory, read tsv file
df_basics <- R.utils::gunzip('title.basics.tsv.gz')
df_basics <- read_tsv("title.basics.tsv", na = "\\N", quote = '')

# Merge data files by tconst
df_imdb <- merge(df_basics, df_ratings, by=c("tconst"))

# Filter unnecessary columns and rows
df_imdb <- df_imdb[df_imdb$startYear >= 1960, c("tconst", "titleType", "primaryTitle", "startYear", "endYear", "genres", "averageRating","numVotes")]

# Write to CSV
write.csv(df_imdb,"IMDB_Data.csv", row.names = TRUE)