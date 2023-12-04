# Templates

**Задача**: Реализовать html страницы для отображения данных

Base.html включает в себя "шапку" сайта, а так же загружает библиотеку bootstrap для ускорения написания html страниц и придания лучшего вида

``` html title="base.html"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>Airport</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
          integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">

  <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <a class="nav-link active" aria-current="page" href="{% url 'flights_list' %}">Schedule</a>
            {% if user.is_authenticated %}
            <a class="nav-link active" aria-current="page" href="{% url 'tickets_for_user' %}"> Your Tickets</a>
            {% endif %}

          <div class="d-flex gap-2">
            {% if user.is_authenticated %}
              <a href="{% url 'user_logout' %}">
                <button class="btn btn-outline-danger" type="submit">Logout</button>
              </a>
            {% else %}
              <a href="{% url 'user_login' %}">
                <button class="btn btn-outline-primary" type="submit">Login</button>
              </a>
              <a href="{% url 'user_register' %}">
                <button class="btn btn-outline-primary" type="submit">Register</button>
              </a>
            {% endif %}
          </div>
        </div>
    </nav>

<div class="container py-3">
  {% block content %} {% endblock %}

</div>
</body>
</html>
```
![Screenshot](../img/Lab2/base.png)

``` html title="buy_ticket.html"
{% extends 'base.html' %} {% block content %}
<h2>Seats</h2>
<table class="table table-striped table-hover mb-5">
    {% for seat in seats %}
    <td class="text-center">
        {% if seat.is_taken %} <s style="color:grey;">{{seat.name}}</s>
        {% else %} {{seat.name}}
        {% endif %}
    </td>
    {% endfor %}
</table>

<div class="row">
    <div class="col-md-3">
        <form method="post">
            {% csrf_token %}
            <div class="mb-3">
                <label for="ticketSeatInput" class="form-label">Seat: </label>
                <input name='seat' class="form-control" id="ticketSeatInput">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    </div>
</div>
{%endblock%}
```

![Screenshot](../img/Lab2/buy_ticket.png)

``` html title="flight_detail.html"
{% extends 'base.html' %} {% block content %}

<h1>Flight {{flight.name}}</h1>

<br>

<h2 class="mb-3">Information about flight</h2>
<div>Type: {{ flight.type }}</div>
<div>Flight number: {{ flight.flight_number }}</div>
<div>Airline: {{ flight.air_line }}</div>
<div>Destination: {{ flight.destination }}</div>
<div>Time: {{ flight.time }}</div>
<div>Gate: {{ flight.gate }}</div>

<br>
<br>

<h2>Passengers already registered</h2>
<div class="mb-4">
    {% if tickets|length > 0 %}
    <table class="table table-striped table-hover">
        <thead>
        <tr>
            <th scope="col">Username</th>
            <th scope="col">Seat</th>
        </tr>
        </thead>

        <tbody>
        {% for ticket in tickets %}
        <tr>
            <td class="align-middle">{{ticket.passenger.username}}</td>
            <td class="align-middle">{{ticket.seat}}</td>
        </tr>
        {% endfor %}
        </tbody>
    </table>
        {%else%}
        All seats are free now.
    {% endif %}
        <br>
        <br>
</div>

{% if user.is_authenticated %}
<h3> You can buy a ticket <a href="{% url 'buy_ticket' flight.id%}"> here</a><h3>
    <div>
        {% if has_ticket%}
        <td>You already have a<a href="{% url 'tickets_for_user'%}" > ticket</a> on these flight</td>
        {% endif %}
        {%else%}
        If you want to buy a ticket, you should be <a href="{% url 'register' %}"> registered</a>
        {%endif%}
        <br>
        <br>
    </div>


<h2 class="my-3">Comments</h2>

{% if comments|length  > 0 %}
<ul class="list-group">
    {% for comment in comments %}
    <li class="list-group-item">
        <strong>{{ comment.writer.username }}</strong>
        <br>
        Rating: {{ comment.rating }}
        <br>
        {{ comment.message }}
    </li>
    {% endfor %}
</ul>
{% else %}
No comments were left
<br>
<br>
{% endif%}

{% if user.is_authenticated %}

<h5 class="my-3">Add comment</h5>
<form method="post" class="mb-5">
    {% csrf_token %}
    {{ comment_form.as_p }}
    <button type="submit" class="btn btn-primary">Add</button>
</form>
{% endif%}


{% endblock %}

```

![Screenshot](../img/Lab2/flight_detail.png)
``` html title="flight_list.html"
{% extends 'base.html' %} {% block content %}

<h1 class="text-center">Schedule</h1>

<table class="table table-striped table-hover mb-5">
  <thead>
    <tr>
      <th scope="col">Type:</th>
      <th scope="col">Time:</th>
      <th scope="col">Flight Num:</th>
      <th scope="col">Direction:</th>
      <th scope="col">Airline:</th>
      <th scope="col">More info:</th>
    </tr>
  </thead>

  <tbody>
    {% for flight in flights %}
      <tr>
        <td>{{flight.type}}</td>
        <td>{{flight.time}}</td>
        <td>{{flight.flight_number}}</td>
        <td>{{flight.destination}}</td>
        <td>{{flight.air_line}}</td>
        <td><a href="{% url 'flight_detail' flight.id %}">Details</a></td>
      </tr>
    {% endfor %}
  </tbody>
</table>

{% endblock %}
```
![Screenshot](../img/Lab2/flight_list.png)

``` html title="login.html"
{% extends 'base.html' %} {% block content %}

<h2 class="mb-3">Sign in</h2>
<form method="post" class="mb-3">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="btn btn-primary">Sign in</button>
</form>
{% endblock %}
```
![Screenshot](../img/Lab2/login.png)

``` html title="register.html"
{% extends 'base.html' %} {% block content %}

<h2 class="mb-4">Registration</h2>
<form method="post" class="mb-3">
    {% csrf_token %}
    {{ user_form.as_p }}
    <button type="submit" class="btn btn-primary">Register</button>
</form>
<p>Already have a profile? <a href="{% url 'user_login' %}" class="text-primary">Login</a></p>

{% endblock %}

```

![Screenshot](../img/Lab2/register.png)

``` html title="ticket_delete.html"
{% extends 'base.html' %} {% block content %}

<a href="{% url 'flight_detail' ticket.seat.flight.id %}" class="btn btn-secondary mb-4">Back to flight</a>

<h2>Delete ticket</h2>
<h5 class="my-3">Information about ticket</h5>
<div>Seat: {{ ticket.seat }}</div>
<div>Ticket: {{ ticket.ticket_number }}</div>

<form method="POST" class="mt-3">
    {% csrf_token %}
    <p>Are you sure you want to delete ticket?</p>

    <button type="submit" class="btn btn-danger">Delete</button>
</form>

{% endblock %}
```

![Screenshot](../img/Lab2/delete_ticket.png)

``` html title="ticket_for_user.html"
{% extends 'base.html' %} {% block content %}

<h2 class="mb-4">Your tickets</h2>
<table class="table table-bordered">
    <thead class="thead-light">
    <tr>
        <th scope="col">Seat</th>
        <th scope="col">Ticket</th>
        <th scope="col">Flight</th>
        <th scope="col">FlightLink</th>
    </tr>
    </thead>
    <tbody>
    {% for ticket in tickets %}
    <tr>
        <td>{{ ticket.seat}}</td>
        <td>{{ ticket.number}}</td>
        <td>
            <div>Flight number: {{ ticket.seat.flight.flight_number }}</div>
            <div>Airline: {{ ticket.seat.flight.air_line }}</div>
            <div>Destination: {{ ticket.seat.flight.destination }}</div>
            <div>Time: {{ ticket.seat.flight.time }}</div>
            <div>Gate: {{ ticket.flight.gate }}</div>
        </td>
        <td><a href="{% url 'flight_detail' ticket.seat.flight.id %}" class="btn btn-primary">More</a></td>
        <td><a href="{% url 'ticket_update' ticket.id %}" class="btn btn-primary">Change</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>

{% endblock %}
```

![Screenshot](../img/Lab2/ticket_for_user.png)

``` html title="ticket_update.html"
{% extends 'base.html' %} {% block content %}

<a href="{% url 'flight_detail' ticket.seat.flight.id %}" class="btn btn-secondary mb-4">Back to flight</a>

<h2>Change seat</h2>
<h5 class="my-3">Information about ticket</h5>
<div>Old seat: {{ ticket.seat }}</div>
<div>Ticket: {{ ticket.ticket_number }}</div>

<form method="POST" class="mt-3">
    {% csrf_token %}
    {{ form.as_p }}

    <button type="submit" class="btn btn-primary">Save changes</button> <a href="{% url 'ticket_delete' ticket.id %}" class="btn btn-primary"> or Delete</a>
</form>



{% endblock %}
```

![Screenshot](../img/Lab2/ticket_update.png)