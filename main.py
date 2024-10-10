from flask import Flask, render_template, session, request, jsonify, redirect
import firebase_admin
from firebase_admin import credentials, auth

cred = credentials.Certificate("firebase-sdk.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)
app.secret_key = "cigarette"

@app.route("/")
def homePage():
    try:
        session["email"]
        # Go to dashboard directly if cookie is found
        return render_template("dashboard.html")
    except:
        return render_template("index.html")

@app.route("/login", methods =["POST", "GET"])
def loginPage():
    if request.method=="GET":
        return render_template("login.html")
    elif request.method=="POST":
        print(request.form)
        email = request.form["email"]
        password = request.form["password"]
        try:
            authApp = auth.get_user_by_email(email)
            if authApp["password"]!=password:
                return redirect("/login")
            session["email"] = request.form["email"]
            return redirect("/")
        except auth.UserNotFoundError:
            # Login again if email is not found in the firebase
            return redirect("/login")
        

@app.route("/signup", methods = ["POST", "GET"])
def signupPage():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        email = request.form["email"]
        uid = request.form["uid"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]
        if password!=confirmPassword:
            return redirect("/signup")
        try:
            authApp = auth.create_user(uid = uid, email = email, password = password)
            session["email"] = email
            # Go to dashboard
            return redirect("/")
        except auth.EmailAlreadyExistsError:
            # Go to login page if email already exits
            return redirect("/login")

app.run(debug=True)