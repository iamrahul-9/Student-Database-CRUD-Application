from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///student.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

with app.app_context():
    db = SQLAlchemy(app)

class StudentDB(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    dob = db.Column(db.Date,  nullable=False) 
    amount_due = db.Column(db.Float, default=0.0, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.srno} - {self.student_id} - {self.first_name} - {self.last_name} - {self.amount_due}"

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob_str = request.form['dob']
        amount_due_str = request.form['amount_due']
        amount_due = float(amount_due_str) if amount_due_str else 0.0

        # Convert dob string to a date object
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

        sdb = StudentDB(student_id=student_id, first_name=first_name, last_name=last_name, dob=dob, amount_due=amount_due)
        db.session.add(sdb)
        db.session.commit()
    allSDB = StudentDB.query.all()
    return render_template("index.html", allSDB=allSDB)

@app.route('/show')
def show():
    allSDB = StudentDB.query.all()
    print(allSDB)
    return render_template("index.html")

@app.route('/update/<int:srno>', methods=['GET', 'POST'])
def update(srno):
    if request.method=='POST':
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob_str = request.form['dob']
        amount_due_str = request.form['amount_due']
        amount_due = float(amount_due_str) if amount_due_str else 0.0

        # Convert dob string to a date object
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

        sdb = StudentDB.query.filter_by(srno=srno).first()
        sdb.student_id = student_id
        sdb.first_name = first_name
        sdb.last_name = last_name
        sdb.dob_str = dob_str
        sdb.amount_due = amount_due

        db.session.add(sdb)
        db.session.commit()
        return redirect("/")
    sdb = StudentDB.query.filter_by(srno=srno).first()
    return render_template('update.html', sdb=sdb)

@app.route('/delete/<int:srno>')
def delete(srno):
    sdb = StudentDB.query.filter_by(srno=srno).first()
    db.session.delete(sdb)
    db.session.commit()
    return redirect("/")

@app.route('/about')
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)