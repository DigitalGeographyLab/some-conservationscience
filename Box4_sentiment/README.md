# BOX 4: ASSESSING PUBLIC SENTIMENT FOR CONSERVATION – CASE PANGOLIN

Supplementary information for Box 4 in *Toivonen, T., Heikinheimo, V., Fink, C., Hausmann, A., Hiippala, T., Järv, O., Tenkanen, H., Di Minin, E. (2019). Social media data for conservation science: a methodological overview. Biological Conservation.*

## Software requirements

### Webis sentiment detection

We use the framework presented in *Hagen et al. (2015)*<sup>[[1]](#1)</sup>, for which the authors combined the previous years’ SemEval’s best Twitter sentiment detection approaches (*Mohammad et al., 2013*<sup>[[2]](#2)</sup>, *Günther and Furrer, 2013*<sup>[[3]](#3)</sup>, *Proisl et al., 2013*<sup>[[4]](#4)</sup>, and *Miura et al., 2014*<sup>[[5]](#5)</sup>). In *Zimbra et al. (2018)*<sup>[[6]](#6)</sup>’s evaluation of “The State-of-the-Art in Twitter Sentiment Analysis” this approach received the highest score in classification accuracy (average across five categories of content, table 4, p5:15).

The framework is available from the github [repo](https://github.com/webis-de/ECIR-2015-and-SEMEVAL-2015) of the Webis research project. It requires a recent Java development kit, and needs to be compiled using e.g. `javac`. To ease its use,  we devised a Python wrapper<sup>[[7]](#7)</sup> for this framework, which is available from the [Python Package Index](https://pypi.org/project/webis/) (PyPi) via `pip`, or from its [GitLab repository](https://gitlab.com/christoph.fink/python-webis/). In the example script, we use this Python wrapper.

To install all dependencies of the sample script: 
- Install a Java development kit (JDK), e.g. [OpenJDK8](https://openjdk.java.net/install/)
- Install the Python dependencies:
    - Navigate to this directory
    - (optional) Create a virtual enviroment:
    ```shell
    virtualenv .virtualenv
    source .virtualenv/bin/activate
    ```
    - Install the packages listed in `requirements.txt`
    ```shell
    pip install -r requirements.txt
    ```

*Note: depending on your installation you might have to replace `pip` with `pip3` and `virtualenv` with `virtualenv3`*

## Run the sample script

```shell
python3 ./identifySentiment.py
```

## References

###### [1]
Hagen, M., Potthast, M., Büchner, M., and Stein, B. (2015): *Webis: An Ensemble for Twitter Sentiment Detection.* In: Proceedings of SemEval 2015.

###### [2]
Mohammad, S., Kiritchenko, S., and Zhu, X. (2013): *NRC-Canada: Building the State-of-the-Art in Sentiment Analysis of Tweets.* In: Second Joint Conference on Lexical and Computational Semantics (*SEM) (Volume 2: Proceedings of the Seventh International Workshop on Semantic Evaluation). 

###### [3]
Günther, T., and Furrer, L. (2013): *GU-MLT-LT: Sentiment analysis of short messages using linguis- tic features and stochastic gradient descent.* In: Second Joint Conference on Lexical and Computational Semantics (*SEM) (Volume 2: Proceedings of the Seventh International Workshop on Semantic Evaluation). 

###### [4]
Proisl, T., Greiner, P., Evert, S., and Kabashi, B. (2013): *Klue: Simple and robust methods for polarity classification.* In: Second Joint Conference on Lexical and Computational Semantics (*SEM) (Volume 2: Proceedings of the Seventh International Workshop on Semantic Evaluation).

###### [5]
Miura, Y., Sakaki, S., Hattori, K., and Ohkuma, T. (2014): *Teamx: A sentiment analyzer with enhanced  lexicon mapping and weighting scheme for unbalanced data.* In: Proceedings of the 8th International Workshop on Semantic Evaluation (SemEval 2014).

###### [6]
Zimbra, D., Abbasi, A., Zeng, D., and Chen, H. (2018) The State-of-the-Art in Twitter Sentiment Analysis: A Review and Benchmark Evaluation. ACM Transactions on Management Information Systems 9(2): 1–29.

###### [7]
Fink, C. (2019): python-webis: Python wrapper for the webis Twitter sentiment evaluation ensemble. Zenodo. doi:10.5281/zenodo.2547461
