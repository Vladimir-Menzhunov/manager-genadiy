import logging
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

def getAlpha(text):
    res1 = ""
    
    for i in text:
        if i.isalpha():
            res1 = "".join([res1, i])

    return res1

def cosine_compare(word1, word2):
    word1 = getAlpha(word1)
    word2 = getAlpha(word2)

    candidate_list = [deEmojify(word1)]
    logging.info(f"candidate_list: {candidate_list}")
    target = deEmojify(word2)
    logging.info(f"target: {target}")

    vec = CountVectorizer(analyzer='char')
    vec.fit(candidate_list)

    result = pairwise_kernels(vec.transform([target]),
                vec.transform(candidate_list),
                metric='cosine')[0]
    logging.info(f"cosine: {result}, projectTodoist: {word1}, projectGot: {word2}")
    return result