import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def baseline_prediction(data, userid, movieid):
    """Function to calculate the baseline for user and movie"""

    global_mean = data.stack().dropna().mean()

    user_mean = data.loc[userid, :].mean()

    item_mean = data.loc[:, movieid].mean()

    user_bias = global_mean - user_mean

    item_bias = global_mean - item_mean

    baseline = global_mean + user_bias + item_bias

    return baseline


def find_neighbour(data, userid, neighbours_count=5):
    user_mean = data.mean(axis=0)
    user_removed_mean_rating = (data - user_mean).fillna(0)

    n_users = len(user_removed_mean_rating.index)
    similarity_score = np.zeros(n_users)

    user_target = user_removed_mean_rating.loc[userid].values.reshape(1, -1)

    for i, neighbour in enumerate(user_removed_mean_rating.index):
        user_neighbour = user_removed_mean_rating.loc[neighbour].values.reshape(1, -1)

        sim_i = cosine_similarity(user_target, user_neighbour)

        similarity_score[i] = sim_i[0, 0]

    sorted_idx = np.argsort(similarity_score)[::-1]

    similarity_score = np.sort(similarity_score)[::-1]

    closest_neighbour = user_removed_mean_rating.index[sorted_idx[1:neighbours_count + 1]].tolist()

    neighbour_similarities = list(similarity_score[1:neighbours_count + 1])

    return {
        'closest_neighbour': closest_neighbour,
        'closest_neighbour_similarity': neighbour_similarities,
    }


def predict_item_rating(userid, movieid, data, neighbour_data, neighbour_count, min_rating=1, max_rating=5):
    """Function to predict movie rating on userid and movieid"""
    baseline = baseline_prediction(data, userid, movieid)

    similarity_rating_total = 0
    similarity_sum = 0

    for i in range(neighbour_count):
        neighbour_rating = data.loc[neighbour_data['closest_neighbour'][i], movieid]

        if np.isnan(neighbour_rating):
            continue

        neighbour_baseline = baseline_prediction(data, neighbour_data['closest_neighbour'][i], movieid)

        adjusted_rating = neighbour_rating - neighbour_baseline

        similarity_rating = neighbour_data['closest_neighbour_similarity'][i] * adjusted_rating

        similarity_rating_total += similarity_rating

        similarity_sum += neighbour_data['closest_neighbour_similarity'][i]

    # Prevent invalid division
    if similarity_sum != 0:
        user_item_prediction_rating = baseline + (similarity_rating_total / similarity_sum)
    else:
        user_item_prediction_rating = baseline

    # Clip prediction to within allowed range
    user_item_prediction_rating = max(min(user_item_prediction_rating, max_rating), min_rating)

    return user_item_prediction_rating


def recommend_items(data, userid, neighbours_count, items_count, recommend_seen=False):
    """Function to recommend items based on a given userid"""

    neighbour_data = find_neighbour(data=data, userid=userid, neighbours_count=neighbours_count)

    prediction_df = pd.DataFrame()

    predicted_raitings = []

    mask = np.isnan(data.loc[userid])

    items_to_predict = data.columns[mask]

    if recommend_seen:
        items_to_predict = data.columns

    for movie in items_to_predict:
        predictions = predict_item_rating(userid=userid, movieid=movie, data=data, neighbour_data=neighbour_data,
                                          neighbour_count=5)

        predicted_raitings.append(predictions)

    prediction_df['movieId'] = data.columns[mask]

    prediction_df['predictions'] = predicted_raitings

    prediction_df = prediction_df.sort_values('predictions', ascending=False).head(items_count)

    return prediction_df


# read data
data = pd.read_csv("Amazon.csv")

# dataframe index
data = data.set_index('user_id')

# view data
# print(data.describe())

user_recommendation = recommend_items(data=data, userid="A3R5OBKS7OM2IR", neighbours_count=5, items_count=5,
                                      recommend_seen=False)

print(user_recommendation)
