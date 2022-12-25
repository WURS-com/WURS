
# WURS 

Wolny Uczelniany Rezerwator Sal





[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)



## Authors

- [Anna Sierka](https://www.github.com/octokatherine)
- [Dominik Dobrowolski](https://www.github.com/octokatherine)


## License

[GPLv3](https://choosealicense.com/licenses/gpl-3.0/#)


## Tech Stack

**Database:** PostGRE SQL

**Backend:** Flask API 


## Deployment

To deploy this project run

```bash
  docker-compose up -d

```
or

```bash
  docker compose up -d
```


# API Reference

### Create user account
```http
  POST /register
```
#### Payload:
| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `user_name` | `string` | **Required**. Your username |
| `password` | `string` | **Required**. Your user password |
| `email` | `string` | **Required**. Your e-mail |


### Login with user account

```http
  POST /login
```
#### Payload:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `user_name`      | `string` | **Required**. Your username |
| `password`      | `string` | **Required**. Your password |

#### It returns your access_token. It will be valid for 30 minutes


### Show all possible rooms

```http
  GET /rooms
```
#### Authentication
| Parameter | Value     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `API-Key`      | `Bearer $YOUR_API_KEY` | **Required**. Your api key recieved after logging |

### Show all reservations

```http
  GET /reservations
```
#### Authentication
| Parameter | Value     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `API-Key`      | `Bearer $YOUR_API_KEY` | **Required**. Your api key recieved after logging |


### Create reservation

```http
  POST /reserve
```
#### Authentication
| Parameter | Value     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `API-Key`      | `Bearer $YOUR_API_KEY` | **Required**. Your api key recieved after logging |


#### Payload:
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `room_id`      | `integer` | **Required**. Room that you want to reserve |
| `start_time`      | `%H:%M` | **Required**. Begining of reservation Hour:Minute |
| `end_time`      | `%H:%M` | **Required**. Ending of reservation Hour:Minute |
| `date`      | `%Y-%m-%d` | **Required**. Date of reservation |
| `resv_descr`      | `string` | **Optional**. Description of reservation |
| `occupancy`      | `integer` | **Required**. How many people will attend |
| `repeat`      | `bool` | **Required**. Do you want your reservation to repeat |
| `repeat_interval`      | `integer` | **Required**. Do you want you reservation to repeat every week, 2 weeks, or more |






## Usage/Examples

#### Creating account
```bash
curl -X POST \
  http://localhost:5000/register \
  -H 'Content-Type: application/json' \
  -d '{
	"user_name": "testuser",
	"password": "testpassword",
	"email": "test@example.com"
}'
```
#### Logging in
```bash
curl -X POST \
  http://localhost:5000/login \
  -H 'Content-Type: application/json' \
  -d '{
	"user_name": "testuser",
	"password": "testpassword"
}'
```
#### Creating reservation
```bash
curl -X POST \
  http://localhost:5000/reserve \
  -H 'Authorization: Bearer ACCESS_TOKEN_HERE' \
  -H 'Content-Type: application/json' \
  -d '{
	"room_id": 1,
	"start_time": "09:00",
	"end_time": "10:00",
	"date": "2022-01-01",
	"resv_descr": "Test reservation",
	"occupancy": 4,
	"repeat": false,
	"repeat_interval": null
}'
```
#### Getting all rooms
```bash
curl -X GET \
  http://localhost:5000/rooms \
  -H 'Authorization: Bearer <ACCESS_TOKEN>'
```
#### Getting all reservations
```bash
curl -X GET \
  http://localhost:5000/reservations \
  -H 'Authorization: Bearer <ACCESS_TOKEN>'
```


