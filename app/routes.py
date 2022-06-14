from app import app
from flask import render_template, redirect, url_for, request
import json
import os
from app.models.product import Product


@app.route('/')
def index(name="Hello World!"):
    return render_template("index.html.jinja", text=name)


@app.route("/extract/", methods=["GET", "POST"])
def extract():
    if not request.method == "POST":
        return render_template("extract.html.jinja")

    product_id = request.form.get("product_id")
    product = Product(product_id)
    product.extract_name()

    if product.product_name:
        product.extract_opinions().calculate_stats().draw_charts()
        product.export_opinions()
        product.export_product()
    else:
        error = "Ups... coś poszło nie tak"
        return render_template("extract.html.jinja", error=error)

    all_opinions = []

    dir = "app/opinions/"
    if not os.path.exists(dir):
        os.makedirs(dir)

    with open(f"{dir}{product_id}.json", "w", encoding="utf-8") as file:
        json.dump(all_opinions, file, indent=4, ensure_ascii=False)

    return redirect(url_for('product', product_id=product_id))


@app.route("/products")
def products():
    products = [file[:file.rfind('.')] for file in os.listdir("app/opinions/")]
    return render_template("products.html.jinja", products=products)


@app.route("/author")
def author():
    return render_template("author.html.jinja")


@app.route("/product/<product_id>")
def product(product_id):
    return render_template("product.html.jinja", product_id=product_id)
