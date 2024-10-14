from flask import make_response, jsonify, request
from models import db, Hero, HeroPower, Power

def configure_routes(app):
    # home route
    @app.route('/')
    def home():
        return 'Welcome to Superheroes API!'

    # route for handling heroes
    @app.route("/heroes", methods=["GET", "POST"])
    def heroes():
        if request.method == "GET":
            heroes_lc = [hero.to_dict() for hero in Hero.query.all()]
            response = make_response(jsonify(heroes_lc), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        elif request.method == "POST":
            data = request.get_json()
            new_hero = Hero(name=data["name"], super_name=data["super_name"])
            db.session.add(new_hero)
            db.session.commit()
            new_hero_dict = new_hero.to_dict()
            response = make_response(jsonify(new_hero_dict), 201)
            response.headers["Content-Type"] = "application/json"
            return response

    # route for handling individual heroes
    @app.route("/heroes/<int:hero_id>", methods=["GET", "PATCH", "DELETE"])
    def hero(hero_id):
        hero = Hero.query.filter_by(id=hero_id).first()
        if not hero:
            response_body = {"error": "Hero not found"}
            response = make_response(jsonify(response_body), 400)
            response.headers["Content-Type"] = "application/json"
            return response
        if request.method == "GET":
            hero_dict = hero.to_dict()
            response = make_response(jsonify(hero_dict), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        elif request.method == "PATCH":
            data = request.get_json()
            for attr in data:
                setattr(hero, attr, data.get(attr))
            db.session.commit()
            hero_dict = hero.to_dict()
            response = make_response(jsonify(hero_dict), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        elif request.method == "DELETE":
            db.session.delete(hero)
            db.session.commit()
            response_body = {"success": True, "message": "Hero deleted"}
            response = make_response(jsonify(response_body), 200)
            response.headers["Content-Type"] = "application/json"
            return response

    # route for handling powers
    @app.route("/powers", methods=["GET"])
    def powers():
        if request.method == "GET":
            powers_lc = [power.to_dict() for power in Power.query.all()]
            response = make_response(jsonify(powers_lc), 200)
            response.headers["Content-Type"] = "application/json"
            return response

    # route for handling individual powers
    @app.route("/powers/<int:power_id>", methods=["GET", "PATCH", "DELETE"])
    def power(power_id):
        power = Power.query.filter_by(id=power_id).first()
        if not power:
            response_body = {"error": "Power not found"}
            response = make_response(jsonify(response_body), 400)
            response.headers["Content-Type"] = "application/json"
            return response
        if request.method == "GET":
            power_dict = power.to_dict()
            response = make_response(jsonify(power_dict), 200)
            response.headers["Content-Type"] = "application/json"
            return response
        elif request.method == "PATCH":
            try:
                data = request.get_json()
                for attr in data:
                    setattr(power, attr, data.get(attr))
                db.session.commit()
                power_dict = power.to_dict()
                response = make_response(jsonify(power_dict), 200)
                response.headers["Content-Type"] = "application/json"
                return response
            except ValueError as e:
                response_body = {"errors": [str(e)]}
                response = make_response(jsonify(response_body), 400)
                response.headers["Content-Type"] = "application/json"
                return response

    # route for creating heropowers
    @app.route("/hero_powers", methods=["POST"])
    def heropowers():
        if request.method == "POST":
            try:
                data = request.get_json()
                new_heropower = HeroPower(
                    strength=data["strength"],
                    hero_id=data["hero_id"],
                    power_id=data["power_id"]
                )
                db.session.add(new_heropower)
                db.session.commit()
                new_heropower_dict = new_heropower.to_dict()
                response = make_response(jsonify(new_heropower_dict), 201)
                response.headers["Content-Type"] = "application/json"
                return response
            except ValueError as e:
                response_body = {"errors": [str(e)]}
                response = make_response(jsonify(response_body), 400)
                response.headers["Content-Type"] = "application/json"
                return response
