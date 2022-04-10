from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import pairwise_kernels
import re

def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def cosine_compare(word1, word2):
    candidate_list = [deEmojify(word1)]
    target = deEmojify(word2)

    vec = CountVectorizer(analyzer='char')
    vec.fit(candidate_list)

    return pairwise_kernels(vec.transform([target]),
                vec.transform(candidate_list),
                metric='cosine')[0]