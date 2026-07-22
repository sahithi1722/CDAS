from datetime import date
import json
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Avg
from .models import AuditLog
from .models import User,LoginHistory
from delays.models import Delay
from accounts.models import User
from masters.models import Shop, Equipment, SubEquipment, Agency
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
from .forms import UserForm
from django.db.models.functions import TruncMonth
# ======================================================
# LOGIN
# ======================================================

def login(request):

    if request.method == "POST":

        emp_no = request.POST.get("emp_no")
        password = request.POST.get("password")

        try:

            user = User.objects.get(
    emp_no=emp_no,
    password=password,
    status="Active"
)

            request.session["emp_no"] = user.emp_no
            request.session["emp_name"] = user.emp_name
            request.session["role"] = user.role

            # Save login history
            LoginHistory.objects.create(
                emp_no=user.emp_no,
                emp_name=user.emp_name
            )

            return redirect("dashboard")

        except User.DoesNotExist:
            return render(
        request,
        "accounts/login.html",
        {
            "error": "Invalid Employee Number or Password"
        }
    )

    return render(request, "accounts/login.html")


# ======================================================
# DASHBOARD
# ======================================================

def dashboard(request):

    if "emp_no" not in request.session:
        return redirect("login")

    delays = Delay.objects.select_related(
        "shop",
        "equipment",
        "subequipment",
        "agency"
    )

    # -----------------------------
    # Filters
    # -----------------------------
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    shop = request.GET.get("shop")
    agency = request.GET.get("agency")

    if from_date:
        delays = delays.filter(delay_from__date__gte=from_date)

    if to_date:
        delays = delays.filter(delay_from__date__lte=to_date)

    if shop:
        delays = delays.filter(shop_id=shop)

    if agency:
        delays = delays.filter(agency_id=agency)

    # -----------------------------
    # KPI Cards
    # -----------------------------
    total_delays = delays.count()

    today_delays = delays.filter(
        delay_from__date=date.today()
    ).count()

    total_users = User.objects.count()

    total_equipment = Equipment.objects.count()

    avg = delays.aggregate(
        average=Avg("delay_duration")
    )["average"]

    average_duration = str(avg) if avg else "0"

    # -----------------------------
    # Agency Chart
    # -----------------------------
    agency_data = (
        delays.values("agency__agency_name")
        .annotate(total=Count("id"))
        .order_by("agency__agency_name")
    )

    agency_labels = [
        item["agency__agency_name"]
        for item in agency_data
    ]

    agency_values = [
        item["total"]
        for item in agency_data
    ]

    # -----------------------------
    # Equipment Impact Analysis
    # -----------------------------
    equipment_data = (
        delays.values("equipment__eqpt_desc")
        .annotate(total=Count("id"))
        .order_by("-total")[:6]
    )

    equipment_labels = [
        item["equipment__eqpt_desc"]
        for item in equipment_data
    ]

    equipment_values = [
        item["total"]
        for item in equipment_data
    ]

    # -----------------------------
    # Shop-wise Chart
    # -----------------------------
    shop_data = (
        delays.values("shop__shop_desc")
        .annotate(total=Count("id"))
        .order_by("shop__shop_desc")
    )

    shop_labels = [
        item["shop__shop_desc"]
        for item in shop_data
    ]

    shop_values = [
        item["total"]
        for item in shop_data
    ]

    # -----------------------------
    # Top Delay Equipment
    # -----------------------------
    top_equipment = (
        delays.values("equipment__eqpt_desc")
        .annotate(total=Count("id"))
        .order_by("-total")[:5]
    )

    max_equipment = 1

    if top_equipment:
        max_equipment = top_equipment[0]["total"]

    # -----------------------------
    # Render
    # -----------------------------
    context = {

        "shops": Shop.objects.all(),

        "agencies": Agency.objects.all(),

        "total_delays": total_delays,

        "today_delays": today_delays,

        "total_users": total_users,

        "total_equipment": total_equipment,

        "average_duration": average_duration,

        "top_equipment": top_equipment,

        "max_equipment": max_equipment,

        "agency_labels": json.dumps(agency_labels),

        "agency_values": json.dumps(agency_values),

        "equipment_labels": json.dumps(equipment_labels),

        "equipment_values": json.dumps(equipment_values),

        "shop_labels": json.dumps(shop_labels),

        "shop_values": json.dumps(shop_values),
    }

    return render(
        request,
        "dashboard.html",
        context
    )

# ======================================================
# LOGOUT
# ======================================================

def logout(request):
    LoginHistory.objects.filter(
    emp_no=request.session["emp_no"],
    logout_time__isnull=True
).update(
    logout_time=timezone.now()
)

    request.session.flush()

    return redirect("login")
# ======================================================
# CHANGE PASSWORD
# ======================================================

def change_password(request):

    if "emp_no" not in request.session:
        return redirect("login")


    if request.method == "POST":

        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")


        user = User.objects.get(
            emp_no=request.session["emp_no"]
        )


        if user.password != old_password:

            return render(
                request,
                "accounts/change_password.html",
                {
                    "error":"Old password incorrect"
                }
            )


        if new_password != confirm_password:

            return render(
                request,
                "accounts/change_password.html",
                {
                    "error":"Password mismatch"
                }
            )


        user.password = new_password
        user.save()


        return render(
            request,
            "accounts/change_password.html",
            {
                "success":"Password changed successfully"
            }
        )


    return render(
        request,
        "accounts/change_password.html"
    )


# ======================================================
# USER LIST
# ======================================================

# ======================================================
# USER MANAGEMENT
# ======================================================

def user_list(request):

    if "emp_no" not in request.session:
        return redirect("login")


    users = User.objects.all()


    # Search

    search = request.GET.get("search")


    if search:

        users = users.filter(
            emp_no__icontains=search
        ) | users.filter(
            emp_name__icontains=search
        )



    # Statistics

    total_users = User.objects.count()


    active_users = User.objects.filter(
        status="Active"
    ).count()


    inactive_users = User.objects.filter(
        status="Inactive"
    ).count()



    paginator = Paginator(
        users,
        10
    )


    page_number = request.GET.get("page")


    page_obj = paginator.get_page(
        page_number
    )
    total_users = User.objects.count()
    active_users = User.objects.filter(
    status="Active"
).count()
    inactive_users = User.objects.filter(
    status="Inactive"
).count()
    admin_count = User.objects.filter(
    role__in=[
        "sys_admin",
        "dept_admin",
        "ppm_admin"
    ]
).count()
    for u in users:
        print("Employee:", u.emp_no, "Status:", u.status)



    return render(
        request,
        "accounts/user_list.html",
        {

            "page_obj": page_obj,

            "search": search,


            "total_users": total_users,

            "active_users": active_users,

            "inactive_users": inactive_users,
            "total_users": total_users,
"active_users": active_users,
"inactive_users": inactive_users,
"admin_count": admin_count,

        }
    )
# ======================================================
# ADD USER
# ======================================================
def user_add(request):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.method == "POST":

        User.objects.create(
            emp_no=request.POST.get("emp_no"),
            emp_name=request.POST.get("emp_name"),
            department=request.POST.get("department"),
            password=request.POST.get("password"),
            role=request.POST.get("role"),
            status=request.POST.get("status"),
        )

        messages.success(request, "User added successfully.")
        return redirect("user_list")

    return render(
        request,
        "accounts/user_form.html",
        {"user": None}
    )
# ======================================================
# EDIT USER
# ======================================================

def user_edit(request, id):

    if "emp_no" not in request.session:
        return redirect("login")

    user = get_object_or_404(User, id=id)

    if request.method == "POST":

        user.emp_no = request.POST.get("emp_no")
        user.emp_name = request.POST.get("emp_name")
        user.department = request.POST.get("department")

        password = request.POST.get("password")
        if password:
            user.password = password

        user.role = request.POST.get("role")
        user.status = request.POST.get("status")

        user.save()

        messages.success(request, "User updated successfully.")
        return redirect("user_list")

    return render(
        request,
        "accounts/user_form.html",
        {"user": user}
    )
# ======================================================
# DELETE USER
# ======================================================

def user_delete(request, id):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "sys_admin":
        return redirect("dashboard")

    user = get_object_or_404(User, id=id)

    user.delete()

    messages.success(
        request,
        "User Deleted Successfully."
    )

    return redirect("user_list")


# ======================================================
# PROFILE
# ======================================================

def profile(request):

    if "emp_no" not in request.session:
        return redirect("login")

    user = User.objects.get(
        emp_no=request.session["emp_no"]
    )

    return render(
        request,
        "accounts/profile.html",
        {
            "user": user
        }
    )


# ======================================================
# LOGIN HISTORY
# ======================================================

def login_history(request):

    if "emp_no" not in request.session:
        return redirect("login")

    history = LoginHistory.objects.all().order_by(
        "-login_time"
    )

    return render(
        request,
        "accounts/login_history.html",
        {
            "history": history,
        },
    )


# ======================================================
# AUDIT LOG
# ======================================================

def audit_log(request):

    if "emp_no" not in request.session:
        return redirect("login")

    logs = AuditLog.objects.all().order_by(
        "-created_at"
    )

    return render(
        request,
        "accounts/audit_log.html",
        {
            "logs": logs,
        },
    )
# Update Profile

def update_profile(request):

    if "emp_no" not in request.session:
        return redirect("login")


    user = User.objects.get(
        emp_no=request.session["emp_no"]
    )


    if request.method == "POST":

        user.emp_name = request.POST.get("emp_name")

        user.save()


        request.session["emp_name"] = user.emp_name


        messages.success(
            request,
            "Profile updated successfully"
        )


        return redirect("profile")


    return render(
        request,
        "accounts/update_profile.html",
        {
            "user": user
        }
    )