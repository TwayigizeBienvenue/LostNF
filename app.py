from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)

# Secret key for session management
app.secret_key = "supersecretkey"

# Sample storage (replace with DB later)
items = []

# Dummy user credentials
VALID_EMAIL = "user@gmail.com"
VALID_PASSWORD = "bienvenu@123"


# --- Index / Dashboard ---
@app.route('/')
def index():
    if 'user' not in session:  # redirect to login if not logged in
        return redirect(url_for('login'))
    return render_template('index.html', items=items)


# --- Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if email == VALID_EMAIL and password == VALID_PASSWORD:
            session['user'] = email
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')


# --- Logout ---
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


# --- Report Item ---
@app.route('/report', methods=['GET', 'POST'])
def report():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Collect form data
        item = {
            "itemName": request.form.get("itemName"),
            "description": request.form.get("description"),
            "category": request.form.get("category"),
            "foundLocation": request.form.get("foundLocation"),
            "dateFound": request.form.get("dateFound"),
            "serialNumber": request.form.get("serialNumber"),
            "reportedBy": request.form.get("reportedBy"),
            "contactInfo": request.form.get("contactInfo"),
            "status": "Pending"  # default status
        }
        items.append(item)  # store in list for now
        flash("Item reported successfully!", "success")
        return redirect(url_for('view'))
    return render_template('report.html')


# --- View Items ---
@app.route('/view')
def view():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('view.html', items=items)


if __name__ == '__main__':
    app.run(debug=True)
