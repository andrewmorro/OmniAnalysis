
from analysis.marketdata.MarketDataService import MinDataService
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import pandas




def prepare_sample(path, df):
    sample = None
    try:
        sample = pandas.read_excel(path)
    except Exception:
        print('Sample cache not found.')

    mdService = MinDataService()
    if sample is None:
        result = []
        book = []
        for index, row in df.iterrows():
            data = mdService.get_1M(row['Code'], row['Date'])
            if data is not None and len(data) == 243:
                book.append((row['Code'], row['Date']))
                result.append(data)

        print("Start clustering...")
        if len(result) <= 0:
            print('No Samples.')
            exit(0)
        sample = pandas.DataFrame(result)

        sample.to_excel(path)
    else:
        print("Using cache for samples...")
    return sample


def show_clustered(sample, n):
    kmeans = KMeans(n_clusters=n)
    pred = kmeans.fit_predict(sample, y=[len(sample), 243])
    #print(kmeans.cluster_centers_)
    # plt.figure(figsize=(12, 12))
    for center in kmeans.cluster_centers_:
        plt.plot(center)
    plt.show()

    clusters = {}
    n = 0
    for item in pred:
        if item in clusters:
            clusters[item].append(sample[n])
        else:
            clusters[item] = [sample[n]]
        n += 1
    return clusters
