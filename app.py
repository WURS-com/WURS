from datetime import timedelta, datetime, time
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    verify_jwt_in_request,
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
    repeat = db.Column(db.Boolean)
    repeat_interval = db.Column(db.Integer)


class Room(db.Model):
    __tablename__ = "rooms"
    room_id = db.Column(db.Integer, primary_key=True)
    building_id = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    room_descr = db.Column(db.String)


with app.app_context():
    db.create_all()


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


@app.route("/rooms", methods=["GET"])
@jwt_required()
def get_all_rooms():
    user_id = get_jwt_identity()
    rooms = Room.query.all()
    results = []
    for room in rooms:
        obj = {
            "room_id": room.room_id,
            "building_id": room.building_id,
            "capacity": room.capacity,
            "room_descr": room.room_descr,
        }
        results.append(obj)
    return jsonify(results)


@app.route("/reservations", methods=["GET"])
@jwt_required()
def get_reservations():
    user_id = get_jwt_identity()
    reservations = Reservation.query.filter_by(user_id=user_id).all()
    results = []
    for reservation in reservations:
        obj = {
            "reservation_id": reservation.reservation_id,
            "start_time": reservation.start_time.strftime("%H:%M"),
            "end_time": reservation.end_time.strftime("%H:%M"),
            "date": reservation.date,
            "user_id": reservation.user_id,
            "room_id": reservation.room_id,
            "resv_descr": reservation.resv_descr,
            "occupancy": reservation.occupancy,
            "repeat": reservation.repeat,
            "repeat_interval": reservation.repeat_interval,
        }
        results.append(obj)
    return jsonify(results)


@app.route("/reserve", methods=["POST"])
@jwt_required()
def reserve():
    data = request.get_json()
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    room = Room.query.get(data["room_id"])
    if data["occupancy"] > room.capacity:
        return (
            jsonify({"message": "Requested occupancy is greater than room capacity"}),
            400,
        )

    if not room:
        return jsonify({"message": "Room does not exist"}), 404

    # Convert start_time and end_time to datetime.time objects
    start_time = datetime.datetime.strptime(data["start_time"], "%H:%M").time()
    end_time = datetime.datetime.strptime(data["end_time"], "%H:%M").time()

    # Check for overlapping reservations every week for the next 4 weeks
    for i in range(4):
        date = datetime.datetime.strptime(
            data["date"], "%Y-%m-%d"
        ) + datetime.timedelta(weeks=-i)

        reservations = Reservation.query.filter_by(
            room_id=data["room_id"], date=date
        ).all()
        for reservation in reservations:
            # Compare start_time and end_time to reservation.start_time and reservation.end_time, respectively
            if (
                start_time <= reservation.start_time
                and end_time >= reservation.end_time
            ):
                return jsonify({"message": "Room is not available at this time"}), 400
    reservation = Reservation(
        start_time=start_time,
        end_time=end_time,
        date=data["date"],
        user=user,
        room=room,
        resv_descr=data["resv_descr"],
        occupancy=data["occupancy"],
        repeat=data["repeat"],
        repeat_interval=data["repeat_interval"],
    )
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"message": "Reservation created successfully"}), 201


if __name__ == "__main__":
    app.run(debug=True)
