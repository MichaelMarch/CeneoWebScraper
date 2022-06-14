from app.utils import get_item
from app.parameters import selectors

class Opinion:
    def __init__(self, opinion_id = 0, author = "", recomendation="", stars="", content="", useful="", useless="", published="", purchased="", pros=[], cons=[]):
        self.opinion_id = opinion_id
        self.author = author
        self.recomendation = recomendation
        self.stars = stars
        self.content = content
        self.useful = useful
        self.useless = useless
        self.published = published
        self.purchased = purchased
        self.pros = pros
        self.cons = cons


    def extract_opinion(self, opinion):
        for key, value in selectors.items():
            setattr(self, key, get_item(opinion, *value))
        self.opinion_id = opinion["data-entry-id"]

        return self
    
    def __str__(self) -> str:
        return f"opinion_id: {self.opinion_id}<br>" + "<br>".join(f"{key}: {str(getattr(self, key))}" for key in selectors.keys())

    def __repr__(self) -> str:
        return f"Opinion(opinion_id={self.opinion_id}, " + ", ".join(f"{key}={str(getattr(self, key))}" for key in selectors.keys()) + ")"

    def to_dict(self) -> dict:
        return {"opinion_id": self.opinion_id} | {key: getattr(self, key) for key in selectors.keys()}

