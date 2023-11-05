from django.http import Http404
from django.contrib.auth import login, authenticate, logout
from .forms import TicketForm, RegistrationForm, LoginForm, CommentForm
from .models import Flight, Ticket, Seat, Comment
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.crypto import get_random_string
from django.db.models import Q


def flights_list(request):
    if request.method != "GET":
        return Http404(f"Method {request.method} not supported")

    flights = Flight.objects.all()
    return render(
        request,
        "flight_list.html",
        {"flights": flights},
    )


@login_required
def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)

    if request.method == "POST":
        if "rating" in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.flight = flight
                comment.writer = request.user
                comment.save()

        return redirect("flight_detail", flight_id)

    else:

        seats_set = Seat.objects.filter(flight__id=flight_id).order_by("name")
        seats = [
            {
                "name": f"{seat}",
                "is_taken": Ticket.objects.filter(seat__id=seat.id).exists(),
            } for seat in seats_set
        ]

        ticket_form = TicketForm(flight)
        has_ticket = Ticket.objects.filter(
            passenger__id=request.user.id, seat__flight__id=flight_id
        ).exists()

        comments = Comment.objects.filter(flight__id=flight_id)
        comment_form = CommentForm()

        return render(
            request,
            "flight_detail.html",
            {
                "flight": flight,
                "comments": comments,
                "tickets": Ticket.objects.filter(seat__flight__id=flight_id),
                "seats": seats,
                "form": ticket_form,
                "has_ticket": has_ticket,
                "user": request.user,
                "comment_form": comment_form
            },
        )


@login_required
def buy_ticket(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)

    if request.method == "POST":
        if 'seat' in request.POST.keys():
            seat = Seat.objects.filter(name=request.POST['seat'], flight__id=flight_id).first()
            form = TicketForm({"seat": seat})

            if not form.is_valid():
                return redirect("flight_detail", flight_id)

            ticket = form.save(commit=False)
            ticket.number = get_random_string(32)
            ticket.passenger = request.user
            ticket.seat.flight = flight
            ticket.save()

            return redirect("tickets_for_user")

    else:
        seats_set = Seat.objects.filter(flight__id=flight_id).order_by("name")
        seats = [
            {
                "name": f"{seat}",
                "is_taken": Ticket.objects.filter(seat__id=seat.id).exists(),
            } for seat in seats_set
        ]

        return render(
            request,
            "buy_ticket.html",
            {
                "flight": flight,
                "tickets": Ticket.objects.filter(seat__flight__id=flight_id),
                "seats": seats,
                "user": request.user,
            },
        )


@login_required(login_url='/login/')
def tickets_for_user(request):
    tickets = Ticket.objects.filter(passenger=request.user)
    return render(request, "ticket_for_user.html", {"tickets": tickets})


def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if not form.is_valid():
            return redirect("ticket_update", ticket_id)

        form.save()
        return redirect("flight_detail", ticket.seat.flight.id)
    else:
        form = TicketForm(instance=ticket)
        return render(
            request,
            "ticket_update.html",
            {"form": form, "ticket": ticket},
        )


@login_required(login_url='/login/')
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, passenger=request.user)
    if request.method == "POST":
        ticket.delete()
        return redirect("flight_detail", ticket.seat.flight.id)
    else:
        return render(
            request,
            "ticket_delete.html",
            {"ticket": ticket},
        )


def register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            return redirect("user_login")
    else:
        user_form = RegistrationForm()

    return render(request, "register.html", {"user_form": user_form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        username = form.data.get("username")
        password = form.data.get("password")
        user = authenticate(username=username, password=password)

        if user is None:
            return redirect("user_login")

        login(request, user)
        return redirect("flights_list")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("user_login")
