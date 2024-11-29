from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height_unit = db.Column(db.String(10), nullable=False)
    weight_unit = db.Column(db.String(10), nullable=False)

    def calculate_bmi(self):
        # Convert to standard units if needed
        if self.height_unit == 'inches':
            height_m = self.height * 0.0254
        else:
            height_m = self.height

        if self.weight_unit == 'lbs':
            weight_kg = self.weight * 0.453592
        else:
            weight_kg = self.weight

        # Calculate BMI
        return round(weight_kg / (height_m ** 2), 2)

    def bmi_category(self):
        bmi = self.calculate_bmi()
        if bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= bmi < 25:
            return 'Normal weight'
        elif 25 <= bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collect form data
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        height_unit = request.form['height_unit']
        weight_unit = request.form['weight_unit']

        # Create new user entry
        new_user = User(
            height=height, 
            weight=weight, 
            height_unit=height_unit, 
            weight_unit=weight_unit
        )
        
        # Add to database
        db.session.add(new_user)
        db.session.commit()

        # Redirect to results page
        return render_template('results.html', 
            user=new_user, 
            bmi=new_user.calculate_bmi(), 
            bmi_category=new_user.bmi_category()
        )
    
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)