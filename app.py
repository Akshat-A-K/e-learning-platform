from flask import Flask, request, render_template, redirect
import mysql.connector

dbr = mysql.connector.connect(
    host='localhost',
    user='root',
    password='2003',
    database='apk1'
)

cr = dbr.cursor()

app = Flask(__name__)

# Define a global variable to hold the email value
logged_in_email = None


@app.route("/", methods=["GET"])
def register():
    return render_template('register.html')


@app.route("/register", methods=["GET", "POST"])
def register_user():
    if request.method == "GET":
        return render_template('register.html')
    else:
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        phone = request.form.get("phone")
        birthdate = request.form.get("birthdate")
        pwd = request.form.get("password")
        print("Received form data:")
        print("First Name:", firstname)
        print("Last Name:", lastname)
        print("Email:", email)
        print("Phone:", phone)
        print("Birth Date:", birthdate)
        print("Password: ", pwd)
        try:
            cr.execute('''INSERT INTO registers (fname, lname, email, phone, bdate, password)
                       VALUES (%s, %s, %s, %s, %s, %s)''', (firstname, lastname, email, phone, birthdate, pwd))
            dbr.commit()
            print("Data inserted successfully")
            return render_template('login.html')
        except mysql.connector.Error as error:
            return "Database error: {}".format(error), 500


@app.route("/login", methods=["GET", "POST"])
def login():
    global logged_in_email  # Reference the global variable
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # Query the database to check if username and password match
        cr.execute("SELECT * FROM registers WHERE email = %s AND password = %s", (username, password))
        user = cr.fetchone()
        if user:
            logged_in_email = user[2]  # Assuming email is in the third column
            print("Logged in email:", logged_in_email)  # Check the value
            # Redirect to dashboard or profile page
            return redirect("/dashboard")
        else:
            error_message = "Invalid username or password"
            return render_template('login.html', error_message=error_message)
    else:
        return render_template('login.html')


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


@app.route("/cyber")
def cyber():
    return render_template('cyber.html')


@app.route("/python")
def python():
    return render_template('python.html')


@app.route("/profile", methods=["GET"])
def profile():
    global logged_in_email
    print("Profile email:", logged_in_email)  # Check the value
    if logged_in_email:
        cr.execute("SELECT * FROM registers WHERE email = %s", (logged_in_email,))
        user_data = cr.fetchone()
        print("User data:", user_data)
        return render_template('profile.html', user=user_data)
    else:
        return redirect("/login")


if __name__ == '__main__':
    app.run(threaded=True, debug=True, port=4000)
