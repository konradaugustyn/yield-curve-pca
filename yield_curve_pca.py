import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
import tabulate

DATA = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS3MO,DGS6MO,DGS1,DGS2,DGS3,DGS5,DGS7,DGS10,DGS20,DGS30"

def main():
    df = pd.read_csv(DATA, index_col=0, parse_dates=True)
    df = df.loc["2007-01-01":]
    df = df.dropna()
    df = df.diff()
    bp_df = df*100
    bp_df = bp_df.dropna()
    pca = PCA(n_components=10)
    pca.fit(bp_df)
    pca_c3 = pca.components_[:3]
    loadings = pd.DataFrame(pca_c3, columns=bp_df.columns, index=["PC1", "PC2", "PC3"])
    loadings.loc["PC2"] *= -1

    exp_var = pd.DataFrame({
    "share": (pca.explained_variance_ratio_[:3]*100)}, index=["PC1", "PC2", "PC3"])
    exp_var["cumulative"] = exp_var["share"].cumsum()
    exp_var.round(1).to_csv("explained_variance.csv")

    #plot
    loadings.T.plot()
    loadings.index = ["PC1 (level)", "PC2 (slope)", "PC3 (curvature)"]
    loadings.columns = ["3m", "6m", "1y", "2y", "3y", "5y", "7y", "10y", "20y", "30y"]
    plt.xticks(range(10), loadings.columns)
    plt.axhline(0, color="grey", linewidth=1)
    plt.title("Yield curve PCA loadings (daily changes, 2007-2026)")
    plt.xlabel("Maturity")
    plt.ylabel("Loading")
    plt.savefig("loading.png")

    print(len(bp_df))
    print(bp_df.index[0])
    print(bp_df.index[-1])

    print(exp_var.round(1).to_markdown())

if __name__ == "__main__":
    main()
