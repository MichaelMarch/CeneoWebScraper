import requests
import json
from bs4 import BeautifulSoup
from app.utils import get_item
from app.models.opinion import Opinion
import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt


class Product:
    def __init__(self, product_id, product_name="", opinions=[], opinions_count=0, pros_count=0, cons_count=0, average_score=0):
        self.product_id = product_id
        self.product_name = product_name
        self.opinions = opinions
        self.opinions_count = opinions_count
        self.pros_count = pros_count
        self.cons_count = cons_count
        self.average_score = average_score


    def extract_opinions(self):
        url = f"https://www.ceneo.pl/{self.product_id}#tab-reviews"
        while url:
            response = requests.get(url)

            if not response.status_code == 200:
                print(f"Status code = {response.status_code}")
                break

            page = BeautifulSoup(response.text, "html.parser")
            opinions = page.select("div.js_product-review")

            for opinion in opinions:
                single_opinion = Opinion().extract_opinion(opinion)

                self.opinions.append(single_opinion)

            try:
                url = "https://ceneo.pl" + \
                    get_item(page, "a.pagination__next", "href")
            except TypeError:
                url = None

        return self

    def extract_name(self):
        url = f"https://www.ceneo.pl/{self.product_id}"
        response = requests.get(url)

        if not response.status_code == 200:
            print(f"Status code = {response.status_code}")
            return self

        page = BeautifulSoup(response.text, "html.parser")
        self.product_name = get_item(page, "h1.product-top__product-info__name")

    def calculate_stats(self):
        opinions = self.opinion_to_df()
        opinions["stars"] = opinions["stars"].map(
            lambda x: float(x.split('/')[0].replace(",", ".")))

        self.opinions_count = len(opinions),
        self.pros_count = opinions["pros"].map(bool).sum(),
        self.cons_count = opinions["cons"].map(bool).sum(),
        self.average_score = opinions["stars"].mean().round(2)

        return self

    def opinion_to_df(self):
        return pd.read_json(json.dumps([opinion.to_dict() for opinion in self.opinions]))

    def draw_charts(self):
        opinions = self.opinion_to_df()
        if not os.path.exists("app/static/plots"):
            os.makedirs("app/static/plots")

        recomendation = opinions["recommendation"].value_counts(
            dropna=False).sort_index().reindex(["Nie polecam", "Polecam", None], fill_value=0)

        # recomendation.plot.pie(
        #     label="",
        #     autopct=lambda p: "{:.1f}%".format(round(p)) if p > 0 else "",
        #     colors=["crimson", "forestgreen", "grey"],
        #     labels=["Nie polecam", "Polecam", "Nie mam zdania"]
        # )

        # plt.title("Rekomendacje")
        # plt.savefig(f"app/static/plots/{self.product_id}_recomendations.png")
        # plt.close()

        # stars = opinions["stars"].value_counts().sort_index().reindex(
        #     list(np.arange(0, 5.5, 0.5)))
        # plot = stars.plot.bar(
        #     color="pink"
        # )
        # plt.title("Oceny produktu")
        # plt.xlabel("Liczba gwiazdek")
        # plt.ylabel("liczba opinii")
        # plt.grid(True, axis="y")
        # plt.xticks(rotation=0)
        # plt.savefig(f"app/static/plots/{self.product_id}_stars.png")
        # plt.close()

        return self

    def __str__(self) -> str:
        return f"""Product id: {self.product_id}
Product name: {self.product_name}
Opinions: {self.opinions}
Opinions count: {self.opinions_count}
Pros count: {self.pros_count}
Cons count: {self.cons_count}
Average score: {self.average_score}"""

    def __repr__(self) -> str:
        return f'Product(product_id,product_name,opinions,opinions_count,pros_count,cons_count,average_score)'

    def to_dict(self) -> dict:
        return {
             "product_id": self.product_id,
             "product_name": self.product_name,
             "opinions": self.opinions,
             "opinions_count": self.opinions_count,
             "pros_count": self.pros_count,
             "cons_count": self.cons_count,
             "average_score": self.average_score
        }

    def export_opinions(self) -> dict:
        if not os.path.exists("app/opinions/"):
            os.makedirs("app/opinions/")

        with open(f"app/opinions/{self.product_id}.json", "w", encoding="UTF-8") as jf:
            json.dump([opinion.to_dict() for opinion in self.opinions],
                      jf, indent=4, ensure_ascii=False)

    def export_product(self):
        pass
