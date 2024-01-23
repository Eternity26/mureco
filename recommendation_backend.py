import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import streamlit as st
from sklearn.cluster import KMeans
# from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from scipy.spatial.distance import cdist

scaler = StandardScaler()


# cache data so save memory
@st.cache_data
def read_data():
    # read data, get 114000 rows
    data = pd.read_csv('datasets/dataset.csv')
    # remove duplicates, get 107126 rows
    data = data.drop_duplicates(subset=['artists', 'track_name', 'album_name'], keep='first', inplace=False)
    # add info to the data frame to facilitate displaying in the frontend
    track_info_list_2d = data[['artists', 'track_name', 'album_name']].values.tolist()
    track_info_list = [str(i[0]) + ' - ' + str(i[1]) + ' | from "' + str(i[2]) + '"' for i in track_info_list_2d]
    df_info = pd.DataFrame(track_info_list, columns=['track_info'])
    data_with_info = pd.concat([data, df_info], axis=1)
    return data, track_info_list, data_with_info


data, track_info_list, data_with_info = read_data()


def get_standard_features(df, features):
    feature_data = pd.DataFrame(data=df, columns=features)
    standard_feature_data = pd.DataFrame(scaler.fit_transform(feature_data))
    return standard_feature_data


def get_features(df, features):
    feature_data = pd.DataFrame(data=df, columns=features)
    feature_data = pd.DataFrame(scaler.transform(feature_data))
    return feature_data


def get_data_with_info():
    return data_with_info


def get_track_info_list():
    return track_info_list


def get_id_by_info(input_info):
    return data_with_info.loc[data_with_info['track_info'] == input_info, ['track_id']]


def get_info_by_id(input_id):
    return data_with_info.loc[data_with_info['track_id'] == input_id, ['track_info']]


def get_recommendation_ids(id_input, num_recommendation):
    """
    :param id_input: id of input track
    :param num_recommendation: number of recommendations made
    :return: dataframe of recommended track ids
    """

    # from input id dataframe to string
    id_str = str(id_input.astype(str)).split()[2]

    # Spotify features, loudness is removed because of high correlation with energy
    features = ['danceability', 'energy',
                'speechiness', 'acousticness',
                'instrumentalness', 'liveness', 'valence']

    # only keep feature data and make them standard scaled
    features_all = get_standard_features(data, features)

    # Find the elbow point, which is 11
    # def sse(df, k):
    #     k_means = KMeans(n_clusters=k, init='k-means++', max_iter=100)
    #     k_means.fit(df)
    #     return k_means.inertia_
    #
    # sses = {}
    #
    # for k in range(1, 50):
    #     sses[k] = sse(features_all, k)
    #
    # plt.plot(list(sses.keys()), list(sses.values()))
    # plt.title('Elbow')
    # plt.show()

    # create the model and fit
    model = KMeans(
        n_clusters=11, init='random',
        n_init=10, max_iter=300,
        tol=1e-04, random_state=0,
    )

    model.fit(features_all)

    # silhouette_score is 0.223, acceptable
    # score = silhouette_score(features_all, model.labels_, metric='euclidean')
    # print('%.3f' % score)

    # from input id to feature dataframe
    df_input = data.loc[data['track_id'] == id_str]
    features_input = get_features(df_input, features)

    # get cluster number
    pred = model.predict(features_input)
    num_cluster = pred[0]

    # get all track features in the cluster
    label = pd.DataFrame(model.labels_, columns=['label'])
    data_all_labelled = pd.concat([data, label], axis=1)
    data_cluster = data_all_labelled[data_all_labelled['label'] == num_cluster]
    features_cluster = get_features(data_cluster, features)

    # compute mean vector
    features_mean = np.mean(features_input, axis=0)

    # calculate euclid distance
    dists = cdist(np.reshape(features_mean, (1, -1)), features_cluster)

    id_recommendation = pd.DataFrame(columns=['track_id', 'distance'])

    # sort by distance
    dist_sorted = pd.Series(dists.flatten(), name='distance')
    track_similar = pd.concat([data['track_id'].reset_index(drop=True), dist_sorted.reset_index(drop=True)],
                              axis=1)

    # remove track that is the same as input
    track_similar = track_similar[~(track_similar['track_id'] == id_str)]
    track_similar = track_similar.sort_values(by='distance', ascending=True).reset_index(drop=True)

    id_recommendation = pd.concat([id_recommendation, track_similar], axis=0, ignore_index=True)

    return id_recommendation.loc[0:num_recommendation - 1, ['track_id']]
