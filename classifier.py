import pandas as pd
import numpy as np
import database
import subprocess
import matplotlib
import idlelib
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import shuffle
from sklearn.feature_extraction.text import CountVectorizer


class Recommendation:

    def __init__(self, file, userid):
        self.file = file
        self.userid = userid
        self.data = self.load_data()
        self.df = pd.read_csv(file)

    def load_data(self):
        db = database.Database()
        data = db.get_choice_user(self.userid)
        return data

    def clean_df(self):
        return self.df.dropna(axis=1)

    def vectorize(self):
        df = shuffle(self.df)
        le = LabelEncoder()
        le.fit(df)
        return le

    def recommend_by_price(self):
        matter = True
        for row in self.data:
            print(row)
            if 'price' in row:
                matter = True if row[3] == 'yes' else False
        if matter:
            try:
                self.df.price = self.df.price.str.replace(',', '')
                self.df.price = self.df.price.str.strip()
                df = self.df[self.df.price.astype(float) > 0]
                out = self.df.loc[self.df.price.astype(float).idxmin()]
            except:
                out = self.df.loc[self.df.price.astype(float).idxmin()]
                # outv = df.dropna(subset=['price'])
            return pd.DataFrame(out.to_dict(), index=[0])[
                ['company', 'customerreviews', 'link', 'price', 'rating', 'reviews', 'title']]
        else:
            return self.df.sort_values(by='price', ascending=False).head(1)

    def recommend_by_brand(self):
        matter = True
        db = database.Database()
        data = db.get_brand(self.userid)
        data = data[-1][3]
        print(data)
        if data:
            if ',' in data:
                brandlist = data.split(',')
                for brand in brandlist:
                    df_filtered = self.df[self.df.company.str.lower() == brand.lower()]
                    if df_filtered.size > 0:
                        return df_filtered.sort_values(by='rating', ascending=False).head(1)
            else:
                print(self.df.company.str.lower() == data.lower())
                df_filtered = self.df[self.df.company.str.lower() == data.lower()]
                if df_filtered.size > 0:
                    filtered_sort_values = df_filtered.sort_values(by='rating', ascending=False)
                    return filtered_sort_values.head(1)
        return None

    def recommend_by_rating(self, matter=True):
        matter = False
        for row in self.data:
            print(row)
            if 'rating' in row:
                matter = True if int(row[3]) > 2 else False
        if matter:
            df = self.df[self.df.rating > 0]
            return df.loc[df.rating.idxmax()]
        else:
            return self.df.sort_values(by='rating').head(1)

    def recommend_by_review(self, matter=True):
        matter = False
        for row in self.data:
            print(row)
            if 'review' in row:
                matter = True if row[3] == 'yes' else False
        if matter:
            return self.df.sort_values(by='reviews').head(1)
        else:
            return self.df.sort_values(by='reviews', ascending=False).head(1)
