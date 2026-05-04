from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=DESKTOP-A3EB83I;"
    "DATABASE=INFINITYROSES;"
    "Trusted_Connection=yes;"
)

@app.route("/")
def home():
    category_id = request.args.get('category')

    cursor = conn.cursor()

    if category_id:
        cursor.execute("""
        SELECT name, price, image_url 
        FROM Products
        WHERE category_id = ?
        ORDER BY product_id
        """, category_id)
    else:
        cursor.execute("""
        SELECT name, price, image_url 
        FROM Products
        ORDER BY product_id
        """)

    products = []
    for row in cursor.fetchall():
        products.append({
            "name": row.name,
            "price": row.price,
            "image": row.image_url
        })

    return render_template("index.html", products=products)


if __name__ == "__main__":
    app.run(debug=True)