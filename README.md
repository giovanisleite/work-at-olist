# Documentation

## Description

This API enables you to send call detail information of existing subscribers and consult a monthly bill of a subscriber.

For this, it was assumed that this system already has telecommunication companies' information such as customers' name and phone number saved as Subscribers.


## API endpoints

#### ```POST /api/call/```

To this endpoint can be send start or end records, containing the information specified:

- <span id="call_start_format">Call Start Record</span>

```
{
  "id":  // Record unique identificator;
  "type":  // Indicate if it's a call "start" or "end" record;
  "timestamp":  // The timestamp of when the event occured;
  "call_id":  // Unique for each call record pair;
  "source":  // The subscriber phone number that originated the call;
  "destination":  // The phone number receiving the call.
}
```

- <span id="call_end_format">Call End Record</span>

```
{
   "id":  // Record unique identificator;
   "type":  // Indicate if it's a call "start" or "end" record;
   "timestamp":  // The timestamp of when the event occured;
   "call_id":  // Unique for each call record pair.
}
```

In response, for both types of information sent, you will receive a message of success or an error.


#### `GET /api/bill/<phone number>` or `GET /api/bill/<phone number>?period=<month/year>`

In this endpoint you will get the <span id="bill_format">*bill information*</span>, like this:

```
{
  "name": //The name of the subscriber
  "period": //The month/year of the bill
  "calls": {
              "destination": //Telephone that received the call
              "call_start_date": //Date that the call started
              "call_start_time": //Time that the call started
              "duration": // //Duration of the call (e.g. 2h30m15s)
              "price": // The cost of this call
  }
}
```

## Installing and Testing

### Install

Be sure that you have python >= 3.5 installed. And follow the instructions bellow:

```console
$ git clone https://github.com/giovanisleite/work-at-olist
$ cd work-at-olist
```

### Configure the .env variables (sample.env it is a good start, so you can rename it to .env)

```
$ mv sample.env .env
```

And fill the .env file with your settings preferences (If you want to, but it is not needed)

- `SEKRET` (_str_, _required_) [Django's secret key](https://docs.djangoproject.com/en/2.0/ref/settings/#secret-key)
- `DATABASE_URL` (_string_, _default: db.sqlite3_, _optional_) [Database URL](https://github.com/kennethreitz/dj-database-url#url-schema)
- `DEBUG` (_bool_, _default: False_, _optional_) enable or disable [Django debug mode](https://docs.djangoproject.com/en/2.0/ref/settings/#debug)
- `HOSTS` (_str_, _optional_ if DEBUG True) [Django's allowed hosts](https://docs.djangoproject.com/en/2.0/ref/settings/#allowed-hosts)

```console
$ pip install -r requirements-local.txt
$ python manage.py migrate
```
### Test

```console
$ python manage.py test
```

You can test the code in [heroku](http://giovani-work-at-olist.herokuapp.com/) or locally (replace the url for http:localhost:8000/) from your terminal, using _curl_. (For test purposes, the database (in Heroku) was populated with two Subscribers, the phones are 0042424242 and 4136363636)

#### If Locally, populate the database and run the application

```console
$ python manage.py shell
> from workatolist.phonecalls.models import Subscriber
> Subscriber.objects.create(name='Maria', phone='0042424242')
> Subscriber.objects.create(name='Joao', phone='4136363636')
> quit()
$ python manage.py runserver
```

(If locally, replace in the url from the examples - http://giovani-work-at-olist.herokuapp.com/ for http://localhost:8000/)

#### Send a call start information
```console
$ curl -H "Content-Type: application/json" -X POST -d '{"id":1, "type":"start", "timestamp":"1517407311", "call_id":"123", "source":"4136363636", "destination":"0042424242"}' http://giovani-work-at-olist.herokuapp.com/api/call/

```
You should see something like the <a href="#call_start_format">call start format</a> in response.

---------------------------------------------------------------------------

#### Send a call end information
```console
$ curl -H "Content-Type: application/json" -X POST -d '{"id":2, "type":"end", "timestamp":"1517407842", "call_id":"123"}' http://giovani-work-at-olist.herokuapp.com/api/call

```
You should see something like the <a href="#call_end_format">call end format</a> in response.

---------------------------------------------------------------------------

#### Get the bill, for the number 4136363636, for the last month or for a specified period (12/2017, in 2nd request)
```console
$ curl -H "Content-Type: application/json" -X GET http://giovani-work-at-olist.herokuapp.com/api/bill/4136363636

$ curl -H "Content-Type: application/json" -X GET http://giovani-work-at-olist.herokuapp.com/api/bill/4136363636?period=12/2017

```
You should see something like the <a href="#bill_format"> bill information format</a> in response of both requests.

## Work Environment

- Python: 3.6.2

- Operating system: Ubuntu 16.04.3

- Text editor: Sublime Text + plugins: Djaneiro, AutoPEP8, SublimeLinter
