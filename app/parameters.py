selectors = {
    "author": ["span.user-post__author-name"],
    "recomendation": ["span.user-post__author-recomendation > em"],
    "stars": ["span.user-post__score-count"],
    "content": ["div.user-post__text"],
    "pros": ["div[class$=\"positives\"] ~ div.review-feature__item", None, True],
    "cons": ["div[class$=\"negatives\"] ~ div.review-feature__item", None, True],
    "useful": ["button.vote-yes > span"],
    "useless": ["button.vote-no > span"],
    "published": ["span.user-post__published > time:nth-child(1)", "datetime"],
    "purchased": ["span.user-post__published > time:nth-child(2)", "datetime"],
}