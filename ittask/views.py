from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm, TicketForm, UserCreateForm, UserUpdateForm
from .models import Ticket, CustomUser
from common.decorators import role_required
from django.shortcuts import render
from .models import Ticket
from django.utils import timezone




# ===================== AUTH =====================

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "ittask/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect based on role
            if user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "manager":
                return redirect("manager_dashboard")
            elif user.role == "staff":
                return redirect("staff_dashboard")
            else:  # viewer
                return redirect("viewer_dashboard")
    else:
        form = LoginForm()
    return render(request, "ittask/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")


# ===================== DASHBOARDS =====================

@login_required
def dashboard(request):
    role = request.user.role
    if role == "admin":
        return redirect("admin_dashboard")
    elif role == "manager":
        return redirect("manager_dashboard")
    elif role == "staff":
        return redirect("staff_dashboard")
    else:
        return redirect("viewer_dashboard")


@role_required(['admin'])
def admin_dashboard(request):
    return render(request, "ittask/admin_dashboard.html")


@role_required(['manager'])
def manager_dashboard(request):
    return render(request, "ittask/manager_dashboard.html")


@role_required(['staff'])
def staff_dashboard(request):
    return render(request, "ittask/staff_dashboard.html")


@role_required(['viewer'])
def viewer_dashboard(request):
    return render(request, "ittask/viewer_dashboard.html")


# ===================== TICKETS =====================

@login_required


def ticket_list(request):
    user = request.user

    if user.role in ["admin", "manager"]:
        tickets = Ticket.objects.all()  # All tickets for admin/manager
    else:  # staff
        tickets = Ticket.objects.filter(assigned_to=user)  # Only assigned tickets

    # Count tickets for summary
    total_tickets = tickets.count()
    open_tickets = tickets.filter(status="open").count()
    in_progress_tickets = tickets.filter(status="in_progress").count()
    closed_tickets = tickets.filter(status="closed").count()

    context = {
        "tickets": tickets,
        "total_tickets": total_tickets,
        "open_tickets": open_tickets,
        "in_progress_tickets": in_progress_tickets,
        "closed_tickets": closed_tickets,
    }
    return render(request, "ittask/ticket_list.html", context)




@role_required(['admin', 'manager'])

def ticket_create(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)  # Don't save yet

            # ✅ REQUIRED: set creator
            ticket.created_by = request.user

            # ✅ If a staff is assigned, record assignment time
            if ticket.assigned_to:
                ticket.assigned_at = timezone.now()

            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()

    return render(request, "ittask/ticket_form.html", {"form": form})

@role_required(['admin', 'manager', 'staff'])

def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Staff can only update tickets assigned to them
    if request.user.role == "staff" and ticket.assigned_to != request.user:
        return redirect("ticket_list")

    if request.method == "POST":
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save(commit=False)  # Don't save yet

            # Update assigned_at if assigned_to is set and was previously empty
            if form.cleaned_data['assigned_to'] and ticket.assigned_at is None:
                ticket.assigned_at = timezone.now()

            # Update closed_at if status changed to closed
            if ticket.status == 'closed' and ticket.closed_at is None:
                ticket.closed_at = timezone.now()

            ticket.save()  # Save changes
            return redirect("ticket_list")
    else:
        form = TicketForm(instance=ticket)

    return render(
        request,
        "ittask/ticket_form.html",
        {"form": form, "title": "Update Ticket"}
    )


@role_required(['admin', 'manager'])
def ticket_delete(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.delete()
    return redirect("ticket_list")


@role_required(['admin', 'manager', 'staff'])
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Staff can only see their assigned tickets
    if request.user.role == "staff" and ticket.assigned_to != request.user:
        return redirect("ticket_list")

    return render(request, "ittask/ticket_detail.html", {"ticket": ticket})



# ===================== USER MANAGEMENT =====================

@role_required(['admin'])
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, "ittask/user_list.html", {"users": users})


@role_required(['admin'])
def user_create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserCreateForm()
    return render(request, "ittask/user_form.html", {"form": form, "title": "Create User"})


@role_required(['admin'])
def user_update(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_list")
    else:
        form = UserUpdateForm(instance=user)
    return render(request, "ittask/user_form.html", {"form": form, "title": "Update User"})
