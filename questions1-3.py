import pandas as pd
from math import pi


class EQWorks:
    def __init__(self):
        self.poi = pd.read_csv("data/POIList.csv")
        self.data = pd.read_csv("data/DataSample.csv")

    def findPOI(self, latitude, longitude):
        distance = 2 ** 31 - 1  # purposely set high so first hypotenuse is always lower
        poiID = None
        for index, row in self.poi.iterrows():
            hypotenuse = ((row[" Latitude"] - latitude) ** 2 + (row["Longitude"] - longitude) ** 2) ** 0.5
            if hypotenuse < distance:
                distance = hypotenuse
                poiID = row["POIID"]
        return poiID, distance

    def analyzeData(self, data):
        for index, row in self.poi.iterrows():
            df = data.loc[data["POIID"] == row["POIID"]]
            xRadius = (df["Longitude"].max() - df["Longitude"].min()) / 2
            yRadius = (df["Latitude"].max() - df["Latitude"].min()) / 2
            radius = max(xRadius, yRadius)
            density = df["Distance"].count() / (pi * radius * radius)

            self.poi.at[index, "Average Distance"] = df["Distance"].mean()
            self.poi.at[index, "Standard Deviation"] = df["Distance"].std()
            self.poi.at[index, "Radius"] = radius
            self.poi.at[index, "Density"] = density

    def main(self):
        # removes duplicates which are considered suspicious request records (question 1)
        self.data.drop_duplicates(subset=[" TimeSt", "Latitude", "Longitude"], keep=False, inplace=True)

        # finds minimum distance & POI (question 2)
        for index, row in self.data.iterrows():
            self.data.at[index, "POIID"], self.data.at[index, "Distance"] = self.findPOI(row["Latitude"], row["Longitude"])

        # finds avg, standard deviation, radius, & density (question 3.1, 3.2)
        self.analyzeData(self.data)

        # answers in CSV format
        self.data.to_csv("answers/DataSample.csv", index=False)
        self.poi.to_csv("answers/POIList.csv", index=False)


run = EQWorks()
run.main()
