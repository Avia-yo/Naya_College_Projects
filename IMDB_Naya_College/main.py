import pandas as pd
import os
import json


from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter
from utils import utils
from kaggle.api.kaggle_api_extended import KaggleApi

# ######### Get Data - by api #########

api = KaggleApi()

api.authenticate()

owner = "harshitshankhdhar"
dataset_name = "imdb-dataset-of-top-1000-movies-and-tv-shows"
dataset_slug = f"{owner}/{dataset_name}"

download_path = 'C:\Temp\IMDB_Dataset'

api.dataset_download_files(dataset_slug, path=download_path, unzip=True)

files = os.listdir(download_path)

csv_file_path = os.path.join(download_path, files[0])
imdb_df = pd.read_csv(csv_file_path)

######### Get Data - by load csv file #########

# csv_file_path = r"D:\Users\Avia\Git\Naya_College_Projects\IMDB_Naya_College\imdb_top_1000.csv"

# imdb_df = pd.read_csv(csv_file_path)

######### Data Manipulation :  drop columns with null values,drop unnecessary columns, rename columns #########

#### Data Cleaning :  drop columns with null values & unnecessary columns, rename columns ###
imdb_df.columns

null_values = imdb_df.isnull().sum(axis=1)
rows_with_null = null_values[null_values > 0]
sum_of_rows_with_null = rows_with_null.sum()
print("Number of null rows:", sum_of_rows_with_null)

duplicates_value = imdb_df.duplicated().sum()
print("Number of duplicate rows:", duplicates_value)

# drop columns & rename column
imdb_df.drop(columns=['Meta_score','Certificate','Gross','Poster_Link','Overview','Star3','Star4'],inplace=True)

imdb_df.rename(columns={'Runtime': 'Runtime_Minutes'}, inplace=True)


#### Data calculations ###

utl = utils()

calculations_by_year = utl.get_calculation(imdb_df, "Released_Year", "No_of_Votes")
calculations_by_year = calculations_by_year.rename(columns={
    'count': 'no_of_rate_movies_this_year',
    'sum': 'sum_no_of_votes',
    'min': 'the_min_votes_for_movie',
    'max': 'the_max_votes_for_movie',
    'mean': 'the_mean_votes_for_movie'
})                                               

df_top_15_No_of_Votes_per_year = utl.get_sort_and_pick_top(calculations_by_year, ('No_of_Votes', 'sum_no_of_votes'), False, 15)

df_mean_IMDB_Rating_per_Genre = utl.get_mean(imdb_df, "Genre", "IMDB_Rating").to_frame().reset_index()

df_top_10_IMDB_Rating_per_Genre = utl.get_sort_and_pick_top(df_mean_IMDB_Rating_per_Genre, "IMDB_Rating", False, 10)

df_top_10_movies=  utl.get_sort_and_pick_top(imdb_df, "IMDB_Rating", False, 10)


print(df_top_15_No_of_Votes_per_year)
print(df_top_10_IMDB_Rating_per_Genre)
print(df_top_10_movies)

######### Visualization #########
# 1 - Creating a scatter plot 

x = df_top_10_IMDB_Rating_per_Genre['Genre']
y = df_top_10_IMDB_Rating_per_Genre['IMDB_Rating']

fig1, ax1 = plt.subplots()
ax1.scatter(x, y)

ax1.set_xlabel('Genre')
ax1.set_ylabel('Average IMDB Rating')
ax1.set_title('The top 10 IMDB Rating by Genre')
ax1.tick_params(axis='x', rotation=90, labelsize=8)
ax1.yaxis.set_major_formatter(FuncFormatter(lambda x, _: '{:.2f}'.format(x)))
fig1.set_size_inches((10, 6))


# 2 - Creating a bar plot
_, ax2 = plt.subplots()
df_top_15_No_of_Votes_per_year[('No_of_Votes', 'sum_no_of_votes')].plot(ax=ax2, kind='bar', figsize=(10, 6))

ax2.set_xlabel('Released_Year')
ax2.set_ylabel('Sum of No_of_Votes')
ax2.set_title('The Top 15 years with most number of Votes')
ax2.tick_params(axis='x', rotation=45)


######### Save the df to csv & json files ######### 

#csv
imdb_df.to_csv('imdb_df_clean.csv', index=False)

calculations_by_year.to_csv('imdb_calculation_by_year.csv', index=False)

#json
with open('top_10_movies.json', 'w') as json_file:

    for index, row in df_top_10_movies.iterrows():

        row_dict = row.to_dict()

        json.dump(row_dict, json_file)
        
        json_file.write('\n')


plt.show()

