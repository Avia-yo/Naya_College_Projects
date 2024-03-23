import pandas as pd
import os
import json


from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

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

#### Data Cleaning :  drop columns with null values,drop unnecessary columns, rename columns ###
imdb_df.columns

imdb_df.isnull().sum()

# drop columns
imdb_df.drop(columns=["Meta_score","Certificate","Gross"],inplace=True)
imdb_df.drop(columns=['Poster_Link','Overview','Star3','Star4'],inplace = True)

imdb_df.rename(columns={'Runtime': 'Runtime_Minutes'}, inplace=True)


#### Data calculation ###

# create functions

calculation_by_year= imdb_df.groupby(by="Released_Year").agg({'No_of_Votes': ['sum','min','max','mean','count']})
calculation_by_year_top_15= calculation_by_year.sort_values(by=('No_of_Votes', 'sum'), ascending=False).head(15)


def calculate_mean_IMDB_Rating_by_Genre(df):
    # Group the DataFrame by 'Genre' and calculate the average rating vote for each genre
    avg_IMDB_Rating_by_Genre = imdb_df.groupby('Genre')['IMDB_Rating'].mean().round(2)
    
    return avg_IMDB_Rating_by_Genre


df_mean_IMDB_Rating_per_Genre = calculate_mean_IMDB_Rating_by_Genre(imdb_df)

df_mean_IMDB_Rating_per_Genre = df_mean_IMDB_Rating_per_Genre.to_frame().reset_index()
df_top_10_IMDB_Rating_per_Genre = df_mean_IMDB_Rating_per_Genre.sort_values(by="IMDB_Rating", ascending=False).head(10)



df_top_10_movies= imdb_df.sort_values(by="IMDB_Rating", ascending=False).head(10)

print(df_top_10_IMDB_Rating_per_Genre)
print(df_top_10_movies)
print(calculation_by_year_top_15)




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
calculation_by_year_top_15[('No_of_Votes', 'sum')].plot(ax=ax2, kind='bar', figsize=(10, 6))

ax2.set_xlabel('Released_Year')
ax2.set_ylabel('Sum of No_of_Votes')
ax2.set_title('The Top 15 years with most number of Votes')
ax2.tick_params(axis='x', rotation=45)


######### Save the df to csv & json files ######### 

#csv
imdb_df.to_csv('imdb_df_clean.csv', index=False)

calculation_by_year.to_csv('imdb_calculation_by_year.csv', index=False)

#json
with open('top_10_movies.json', 'w') as json_file:

    for index, row in df_top_10_movies.iterrows():

        row_dict = row.to_dict()

        json.dump(row_dict, json_file)
        
        json_file.write('\n')


plt.show()

