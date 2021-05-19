import pandas as pd
import json
import math
import torch

prefix = "D:\data\yelp_dataset\csv\\"

def user_feature_extract(file):
    df = pd.read_csv(prefix + file + ".csv")
    float_features = ["average_stars", "useful", "compliment_photos", "compliment_list", 'compliment_funny',
                    'compliment_plain', 'review_count', 'fans', 'compliment_note', 'funny', 'compliment_writer',
                    'compliment_cute', 'average_stars', 'compliment_more', 'compliment_hot', 'cool',
                    'compliment_profile', 'compliment_cool']
    array_length_features = ["elite", 'friends']
    features = {}
    for idx, profile in df.iterrows():
        feature = [float(profile[key]) for key in float_features]
        for key in array_length_features:
            f = profile[key]
            if isinstance(f, float) and math.isnan(f):
                feature.append(0.0)
            else:
                feature.append(float(len(profile[key].split(","))))
        features[profile["user_id"]] = feature
    with open(prefix + file + ".json", "w") as outfile:
        json.dump(features, outfile)
        outfile.close()


def item_feature_extract(file):
    df = pd.read_csv(prefix + file + ".csv")
    float_features = ["stars", "review_count", "is_open", "attributes.RestaurantsPriceRange2"]
    bool_features = ["RestaurantsDelivery", "Open24Hours", "DogsAllowed", "CoatCheck", "RestaurantsGoodForGroups",
                     "BYOB", "RestaurantsTableService", "RestaurantsCounterService", "Corkage", "GoodForKids",
                     "BusinessAcceptsBitcoin", "HappyHour", "WheelchairAccessible", "BusinessAcceptsCreditCards",
                     "ByAppointmentOnly", "DriveThru", "HasTV", "GoodForDancing", "Caters", "AcceptsInsurance",
                     "RestaurantsReservations", "RestaurantsTakeOut", "BikeParking", "OutdoorSeating"]
    enumerate_features = ["Smoking", "AgesAllowed", "Alcohol", "BYOBCorkage", "NoiseLevel", "WiFi", "RestaurantsAttire"]
#     pending_features = ["categories", "DietaryRestrictions", "HairSpecializesIn", "Ambience", "GoodForMeal", "Music", "BusinessParking", "BestNights"]
    features = {}
    dic = {'Smoking': {'no': 1, 'yes': 2, 'outdoor': 3}, 'AgesAllowed': {'21plus': 1, 'allages': 2, '19plus': 3, '18plus': 4}, 'Alcohol': {'full_bar': 1, 'beer_and_wine': 2}, 'BYOBCorkage': {'yes_corkage': 1, 'no': 2, 'yes_free': 3}, 'NoiseLevel': {'very_loud': 1, 'quiet': 2, 'average': 3, 'loud': 4}, 'WiFi': {'no': 1, 'free': 2, 'paid': 3}, 'RestaurantsAttire': {'formal': 1, 'casual': 2, 'dressy': 3}}
    for idx, profile in df.iterrows():
        feature1 = []
        for key in float_features:
            f = profile[key]
            if isinstance(f, float) or isinstance(f, int):
                feature1.append(f)
            elif isinstance(f, str):
                if f.lower() == "none":
                    feature1.append(0.0)
                else:
                    feature1.append(float(f))
            else:
                print(f)
        feature2 = []
        for key in bool_features:
            f = profile["attributes." + key]
            if isinstance(f, float) and math.isnan(f):
                feature2.append(0.0)
                continue
            if isinstance(f, bool):
                feature2.append(1.0 if f else 0.0)
                continue
            f = f.lower()
            if f == 'none' or f == 'false':
                feature2.append(0.0)
            elif f == 'true':
                feature2.append(1.0)
            else:
                print(f)
        feature3 = []
        for key in enumerate_features:
            f = profile["attributes." + key]
            if isinstance(f, float) and math.isnan(f):
                feature3.append(0.0)
                continue
            if isinstance(f, str):
                f = f.replace('u\'', "").replace('\'', "")
                if f.lower() == "none":
                    feature3.append(0.0)
                    continue
            feature3.append(1.0 * dic[key][f])
            # dic[key].add(f)
        features[profile["business_id"]] = feature1 + feature2 + feature3
    # for key in enumerate_features:
    #     dic[key] = {v: idx for idx, v in enumerate(dic[key], 1)}
    # print(dic)
    with open(prefix + file + ".json", "w") as outfile:
        json.dump(features, outfile)
        outfile.close()

def feature_to_tensor(file):
    with open(prefix + file + ".json", "r") as file:
        features_list = json.load(file)
        file.close()
        features = {user: torch.tensor(f, dtype=torch.float64, device=torch.device("cpu")) for user, f in features_list.items()}
    return features



# user_feature_extract("yelp_academic_dataset_user")
# item_feature_extract("yelp_academic_dataset_business")
# feature_to_tensor("yelp_academic_dataset_user")
feature_to_tensor("yelp_academic_dataset_business")
