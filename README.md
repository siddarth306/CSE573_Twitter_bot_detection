# Twitter Bot Detection: via Retweet Correlation

Project uses unsupervised learning via clustering techniques to detect Twitter bot accounts. 

#### Four Approachs: 
+ K-means++
  * Build Retweet matrix -> NMF -> K-means++ -> Detect high correlation clusters
+ Spectral Clustering
  * Build Retweet matrix -> NMF -> Pairwise Correlation -> Spectral Clustering -> Detect high correlation clusters
+ Clustering via Pairwise Correlation (using NMF)
  * Build Retweet matrix -> NMF -> Pairwise Correlation -> build graphs with only highly correlated users -> run BFS to cluster
+ Clustering via Pairwise Correlation (using Node-to-vec)
  * Build Retweet matrix -> Node-to-vec -> Pairwise Correlation -> build graphs with only highly correlated users -> run BFS to cluster


## Data and Evaluations
[Clustering Results on Sample Dataset](https://docs.google.com/spreadsheets/d/1Kt-IFO9PLN4qSeCPtY7AEXBRyl75Q_ckk4tzV2rBQ-M/edit?usp=sharing)

