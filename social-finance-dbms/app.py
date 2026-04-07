from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sameera@2007",
    database="social_finance",
    buffered=True
)


# ================= HOME =================
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():

    cursor = db.cursor(buffered=True)

    cursor.execute("SELECT COUNT(*) FROM users")

    total_users = cursor.fetchone()[0]

    return render_template(
        "dashboard.html",
        total_users=total_users
    )


# ================= USERS PAGE =================
@app.route("/users")
def users():

    cursor = db.cursor()

    cursor.execute("SELECT * FROM users")

    data = cursor.fetchall()

    return render_template("users.html", data=data)


# ================= ADD USER =================
@app.route("/add_user", methods=["POST"])
def add_user():

    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO users(name,email,phone) VALUES(%s,%s,%s)",
        (name, email, phone)
    )

    db.commit()

    return redirect("/users")


# ================= DELETE USER =================
@app.route("/delete/<int:user_id>")
def delete(user_id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM users WHERE user_id=%s",
        (user_id,)
    )

    db.commit()

    return redirect("/users")


# ================= ADD LOAN PAGE =================
@app.route("/addloan")
def addloan():

    cursor = db.cursor()

    cursor.execute("SELECT user_id,name FROM users")

    users = cursor.fetchall()

    return render_template("addloan.html", users=users)


@app.route("/insertloan", methods=["POST"])
def insertloan():

    user_id = int(request.form["user_id"])
    amount = float(request.form["amount"])
    interest = float(request.form["interest"])
    duration = int(request.form["duration"])

    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO loans(user_id,loan_amount,interest_rate,duration) VALUES(%s,%s,%s,%s)",
        (user_id, amount, interest, duration)
    )

    db.commit()

    return render_template("loan_success.html")


# ================= TRANSACTIONS PAGE =================
@app.route("/transactions")
def transactions():

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
    SELECT t.transaction_id,
           u.name,
           t.amount,
           t.transaction_date
    FROM transactions t
    JOIN users u
    ON t.user_id = u.user_id
    ORDER BY t.transaction_date DESC
    """)

    data = cursor.fetchall()

    cursor.execute("SELECT user_id,name FROM users")

    users = cursor.fetchall()

    return render_template(
        "transactions.html",
        data=data,
        users=users
    )


# ================= ADD TRANSACTION =================
@app.route("/add_transaction", methods=["POST"])
def add_transaction():

    try:

        user_id = int(request.form["user_id"])
        amount = float(request.form["amount"])

        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO transactions(user_id,amount) VALUES(%s,%s)",
            (user_id, amount)
        )

        db.commit()

    except Exception as e:
        return f"Error inserting transaction: {e}"

    return redirect("/transactions")


# ================= DELETE TRANSACTION =================
@app.route("/delete_transaction/<int:id>")
def delete_transaction(id):

    cursor = db.cursor()

    cursor.execute(
        "DELETE FROM transactions WHERE transaction_id=%s",
        (id,)
    )

    db.commit()

    return redirect("/transactions")


@app.route("/emi", methods=["GET", "POST"])
def emi():

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT user_id, name FROM users")
    users = cursor.fetchall()

    emi_result = None

    if request.method == "POST":

        user_id = request.form["user_id"]

        cursor.execute("""
        SELECT 
            loan_amount,
            interest_rate,
            duration
        FROM loans
        WHERE user_id=%s
        """, (user_id,))

        loan = cursor.fetchone()

        if loan:

            P = float(loan["loan_amount"])
            R = float(loan["interest_rate"]) / 12 / 100
            N = int(loan["duration"])

            emi = (P * R * (1 + R)**N) / ((1 + R)**N - 1)

            emi_result = round(emi, 2)

    return render_template(
        "emi.html",
        users=users,
        emi_result=emi_result
    )

# ================= RUN APP =================
if __name__ == "__main__":
    app.run(debug=True)