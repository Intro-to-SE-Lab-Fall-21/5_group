import re
import smtplib
import easyimap as e
from email.message import EmailMessage
from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

app = Flask(__name__)
app.secret_key = 'isgoodoneforme'


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/createAccount", methods=["POST", "GET"])
def createAccount():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        print(username)
        print(email)
        print(password)

        return redirect("login")

    else:
        return render_template("createAccount.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        if server.login(email, password):
            session['email'] = email
            session['password'] = password
            return redirect(url_for("user_index"))
        else:
            return render_template("login.html")

    else:
        return render_template("login.html")


@app.route("/user_index", methods=["POST", "GET"])
def user_index():
    query = ""
    if request.method == "POST":
        query = request.form.get("search")
        emails = displayEmails(query)
        return render_template("search_results.html", emails=emails)

    emails = displayEmails(query)
    return render_template("user_index.html", emails=emails)


@app.route("/user_send", methods=["POST", "GET"])
def sendEmail():
    if request.method == "POST":
        email = session["email"]
        password = session['password']
        recipient = request.form.get("recipient")
        subject = request.form.get("subject")
        message = request.form.get("message")
        filename = request.form.get("file")

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = email
        msg['To'] = recipient
        msg.set_content(message)

        if filename != "":
            with open(filename, 'rb') as f:
                file_data = f.read()
                file_name = f.name

            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
        server.send_message(msg)
        server.quit()

        return redirect("user_index")

    else:
        return render_template("user_send.html")


@app.route("/user_forward", methods=["POST", "GET"])
def forward():
    if request.method == "POST":
        email = session["email"]
        password = session['password']
        recipient = request.form.get("recipient")
        subject = request.form.get("subject")
        message = request.form.get("message")
        print(email)
        print(recipient)
        print(subject)
        print(message)

        msg = EmailMessage()
        msg.set_content(message)

        msg['Subject'] = subject
        msg['From'] = email
        msg['To'] = recipient

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
        server.send_message(msg)
        server.quit()

        return redirect("user_index")

    else:
        return render_template("user_forward.html")


@app.route("/search_results")
def search_results():
    return render_template("search_results.html")


def displayEmails(query):
    user = session["email"]
    password = session['password']

    server = e.connect("imap.gmail.com", user, password)
    server.listids()

    num = len(server.listids())
    print(num)

    if query != "":
        results = []
        for i in range(num):
            email = server.mail(server.listids()[i])
            body = email.body.lower().split()

            if query in body:
                results.append(email)

        server.quit()
        print(results)
        return results

    else:
        msgs = []
        for i in range(num):
            email = server.mail(server.listids()[i])
            msgs.append(email)
        server.quit()
        return msgs


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
