#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas
import webis


def main():
    tweets = pandas.read_csv("sample_data.csv")

    sentiment = webis.SentimentIdentifier().identifySentiment(
        tweets[["tweetId", "text"]]
    )

    tweets.set_index("tweetId", inplace=True)
    sentiment.set_index("tweetId", inplace=True)
    tweets = tweets.join(sentiment)

    tweets.to_csv("sample_data_with_sentiment.csv")


if __name__ == "__main__":
    main()
