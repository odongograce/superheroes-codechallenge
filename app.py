from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/heroes")
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([{"id": h.id, "name": h.name, "super_name": h.super_name} for h in heroes]), 200


@app.route("/heroes/<int:id>")
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    return jsonify(hero.to_dict()), 200


@app.route("/powers")
def get_powers():
    powers = Power.query.all()
    return jsonify([p.to_dict() for p in powers]), 200


@app.route("/powers/<int:id>")
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    return jsonify(power.to_dict()), 200


@app.route("/powers/<int:id>", methods=["PATCH"])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    try:
        data = request.json
        if "description" in data:
            power.description = data["description"]
        db.session.commit()
        return jsonify(power.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400


@app.route("/hero_powers", methods=["POST"])
def create_hero_power():
    try:
        data = request.json
        hero_power = HeroPower(
            hero_id=data["hero_id"],
            power_id=data["power_id"],
            strength=data["strength"]
        )
        db.session.add(hero_power)
        db.session.commit()
        return jsonify(hero_power.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400


if __name__ == "__main__":
    app.run(debug=True)
