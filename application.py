from flask import Flask,jsonify,request
app=Flask(__name__)
from flask_sqlalchemy import SQLAlchemy



app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
db=SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@app.route('/')
def index():
    return 'hello!'

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()

    output=[]
    for drink in drinks:
        drink_data={'name': drink.name, 'description':drink.description}
        output.append(drink_data)
    return jsonify(output)

@app.route('/drinks/<int:id>')
def get_drinks_id(id):
    drinks = Drink.query.get_or_404(id)
    return jsonify({"name":drinks.name,"description":drinks.description})

@app.route('/drinks',methods=['POST'])
def add_drinks():
    drinks = Drink(name=request.json['name'],description=request.json['description'])
    db.session.add(drinks)
    db.session.commit()
    return {'id':drinks.id}

@app.route('/drinks/<int:id>',methods=['DELETE'])
def delete_drink(id):
    drinks = Drink.query.filter_by(id=id).first()
    db.session.delete(drinks)
    db.session.commit()
    return {"message":"data deleted"}