from datetime import timedelta

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
)


from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:test@localhost/room_reservations"
app.config["JWT_SECRET_KEY"] = "secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    password = db.Column(db.String)
    email = db.Column(db.String)


class Reservation(db.Model):
    __tablename__ = "reservations"
    reservation_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user = db.relationship("User", backref="reservations")
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.room_id"))
    room = db.relationship("Room", backref="reservations")
    resv_descr = db.Column(db.String)
    occupancy = db.Column(db.Integer)


class Room(db.Model):
    __tablename__ = "rooms"
    room_id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    room_descr = db.Column(db.String)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    user = User(
        user_name=data["user_name"],
        password=generate_password_hash(data["password"]),
        email=data["email"],
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(user_name=data["user_name"]).first()
    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.user_id)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"message": "Invalid username or password"}), 401


@app.route("/reserve", methods=["POST"])
@jwt_required()
def reserve():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    room = Room.query.get(data["room_id"])

    if not room:
        return jsonify({"message": "Room does not exist"}), 404

    if data["occupancy"] > room.capacity:
        return (
            jsonify({"message": "Requested occupancy is greater than room capacity"}),
            400,
        )

    overlapping_reservations = Reservation.query.filter(
        Reservation.room_id == data["room_id"],
        Reservation.date == data["date"],
        Reservation.start_time <= data["end_time"],
        Reservation.end_time >= data["start_time"],
    ).all()
    if overlapping_reservations:
        return (
            jsonify({"message": "Requested time conflicts with existing reservation"}),
            400,
        )

    reservation = Reservation(
        start_time=data["start_time"],
        end_time=data["end_time"],
        date=data["date"],
        user=user,
        room=room,
        resv_descr=data["resv_descr"],
        occupancy=data["occupancy"],
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation created successfully"}), 201


if __name__ == "__main__":
    app.run(debug=True)
