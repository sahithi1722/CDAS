from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Shop, Equipment, SubEquipment, Agency
from .forms import EquipmentForm
from django.core.paginator import Paginator

# ===========================
# Equipment
# ===========================
def equipment_list(request):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    search = request.GET.get("search")

    equipment = Equipment.objects.select_related(
        "shop"
    ).order_by("eqpt_code")

    if search:

        equipment = equipment.filter(
            eqpt_desc__icontains=search
        )

    paginator = Paginator(equipment, 10)

    page = request.GET.get("page")

    equipment = paginator.get_page(page)

    return render(
        request,
        "masters/equipment_list.html",
        {
            "equipment": equipment,
            "search": search,
        }
    )

def equipment_add(request):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    if request.method == "POST":

        shop = Shop.objects.get(id=request.POST["shop"])

        eqpt_code = request.POST["eqpt_code"]

        eqpt_desc = request.POST["eqpt_desc"]

        if Equipment.objects.filter(eqpt_code=eqpt_code).exists():

            return render(
                request,
                "masters/equipment_form.html",
                {
                    "shops": Shop.objects.all(),
                    "error": "Equipment Code already exists."
                }
            )

        Equipment.objects.create(

            shop=shop,

            eqpt_code=eqpt_code,

            eqpt_desc=eqpt_desc

        )

        messages.success(request, "Equipment Added Successfully.")

        return redirect("equipment_list")

    return render(
        request,
        "masters/equipment_form.html",
        {
            "shops": Shop.objects.all()
        }
    )

# ===========================
# Masters Home
# ===========================

# ===========================
# Masters Home
# ===========================

def master_home(request):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    return render(
        request,
        "masters/master_home.html"
    )


# ===========================
# Shop List
# ===========================

def shop_list(request):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    search = request.GET.get("search")

    shops = Shop.objects.all().order_by("shop_code")

    if search:

        shops = shops.filter(
            shop_desc__icontains=search
        )

    paginator = Paginator(shops, 10)

    page = request.GET.get("page")

    shops = paginator.get_page(page)

    return render(
        request,
        "masters/shop_list.html",
        {
            "shops": shops,
            "search": search,
        }
    )


# ===========================
# Add Shop
# ===========================

def shop_add(request):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    if request.method == "POST":

        shop_code = request.POST.get("shop_code")
        shop_desc = request.POST.get("shop_desc")

        if Shop.objects.filter(shop_code=shop_code).exists():

            return render(
                request,
                "masters/shop_form.html",
                {
                    "error": "Shop Code already exists."
                }
            )

        Shop.objects.create(

            shop_code=shop_code,

            shop_desc=shop_desc

        )

        messages.success(request, "Shop Added Successfully.")

        return redirect("shop_list")

    return render(
        request,
        "masters/shop_form.html"
    )

# ===========================
# Edit Shop
# ===========================

def shop_edit(request, id):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    shop = get_object_or_404(Shop, id=id)

    if request.method == "POST":

        shop_code = request.POST.get("shop_code")

        if Shop.objects.exclude(id=id).filter(shop_code=shop_code).exists():

            return render(
                request,
                "masters/shop_form.html",
                {
                    "shop": shop,
                    "error": "Shop Code already exists."
                }
            )

        shop.shop_code = shop_code
        shop.shop_desc = request.POST.get("shop_desc")

        shop.save()

        messages.success(request, "Shop Updated Successfully.")

        return redirect("shop_list")

    return render(
        request,
        "masters/shop_form.html",
        {
            "shop": shop
        }
    )

# ===========================
# Delete Shop
# ===========================

def shop_delete(request, id):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    shop = get_object_or_404(Shop, id=id)

    shop.delete()

    messages.success(request, "Shop Deleted Successfully.")

    return redirect("shop_list")
def equipment_edit(request, id):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    equipment = get_object_or_404(Equipment, id=id)

    if request.method == "POST":

        eqpt_code = request.POST["eqpt_code"]

        if Equipment.objects.exclude(id=id).filter(
            eqpt_code=eqpt_code
        ).exists():

            return render(
                request,
                "masters/equipment_form.html",
                {
                    "equipment": equipment,
                    "shops": Shop.objects.all(),
                    "error": "Equipment Code already exists."
                }
            )

        equipment.shop = Shop.objects.get(id=request.POST["shop"])

        equipment.eqpt_code = eqpt_code

        equipment.eqpt_desc = request.POST["eqpt_desc"]

        equipment.save()

        messages.success(request, "Equipment Updated Successfully.")

        return redirect("equipment_list")

    return render(
        request,
        "masters/equipment_form.html",
        {
            "equipment": equipment,
            "shops": Shop.objects.all(),
        }
    )
def equipment_delete(request, id):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    equipment = get_object_or_404(
        Equipment,
        id=id
    )

    equipment.delete()

    messages.success(request, "Equipment Deleted Successfully.")

    return redirect("equipment_list")
# ==========================
# Agency Master
# ==========================

from django.core.paginator import Paginator
from django.contrib import messages

def agency_list(request):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    search = request.GET.get("search")

    agencies = Agency.objects.all().order_by("agency_name")

    if search:
        agencies = agencies.filter(
            agency_name__icontains=search
        )

    paginator = Paginator(agencies, 10)

    page = request.GET.get("page")

    agencies = paginator.get_page(page)

    return render(
        request,
        "masters/agency_list.html",
        {
            "agencies": agencies,
            "search": search,
        }
    )
def agency_add(request):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    if request.method == "POST":

        agency_name = request.POST.get("agency_name")

        if Agency.objects.filter(
            agency_name=agency_name
        ).exists():

            return render(
                request,
                "masters/agency_form.html",
                {
                    "error": "Agency already exists."
                }
            )

        Agency.objects.create(
            agency_name=agency_name
        )

        messages.success(
            request,
            "Agency Added Successfully."
        )

        return redirect("agency_list")

    return render(
        request,
        "masters/agency_form.html"
    )
def agency_edit(request, id):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    agency = get_object_or_404(
        Agency,
        id=id
    )

    if request.method == "POST":

        agency_name = request.POST.get("agency_name")

        if Agency.objects.exclude(id=id).filter(
            agency_name=agency_name
        ).exists():

            return render(
                request,
                "masters/agency_form.html",
                {
                    "agency": agency,
                    "error": "Agency already exists."
                }
            )

        agency.agency_name = agency_name

        agency.save()

        messages.success(
            request,
            "Agency Updated Successfully."
        )

        return redirect("agency_list")

    return render(
        request,
        "masters/agency_form.html",
        {
            "agency": agency
        }
    )
def agency_delete(request, id):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    agency = get_object_or_404(
        Agency,
        id=id
    )

    agency.delete()

    messages.success(
        request,
        "Agency Deleted Successfully."
    )

    return redirect("agency_list")

def subequipment_list(request):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    search = request.GET.get("search")

    subequipment = SubEquipment.objects.select_related(
        "equipment",
        "equipment__shop"
    ).order_by("sub_eqpt_code")

    if search:
        subequipment = subequipment.filter(
            sub_eqpt_desc__icontains=search
        )

    paginator = Paginator(subequipment, 10)

    page = request.GET.get("page")

    subequipment = paginator.get_page(page)

    return render(
        request,
        "masters/subequipment_list.html",
        {
            "subequipment": subequipment,
            "search": search,
        }
    )
def subequipment_add(request):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    if request.method == "POST":

        equipment = Equipment.objects.get(
            id=request.POST["equipment"]
        )

        sub_eqpt_code = request.POST["sub_eqpt_code"]
        sub_eqpt_desc = request.POST["sub_eqpt_desc"]

        if SubEquipment.objects.filter(
            sub_eqpt_code=sub_eqpt_code
        ).exists():

            return render(
                request,
                "masters/subequipment_form.html",
                {
                    "equipment": Equipment.objects.all(),
                    "error": "Sub Equipment Code already exists."
                }
            )

        SubEquipment.objects.create(
            equipment=equipment,
            sub_eqpt_code=sub_eqpt_code,
            sub_eqpt_desc=sub_eqpt_desc
        )

        messages.success(
            request,
            "Sub Equipment Added Successfully."
        )

        return redirect("subequipment_list")

    return render(
        request,
        "masters/subequipment_form.html",
        {
            "equipment": Equipment.objects.all()
        }
    )
def subequipment_edit(request, id):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    subequipment = get_object_or_404(
        SubEquipment,
        id=id
    )

    if request.method == "POST":

        code = request.POST["sub_eqpt_code"]

        if SubEquipment.objects.exclude(id=id).filter(
            sub_eqpt_code=code
        ).exists():

            return render(
                request,
                "masters/subequipment_form.html",
                {
                    "subequipment": subequipment,
                    "equipment": Equipment.objects.all(),
                    "error": "Sub Equipment Code already exists."
                }
            )

        subequipment.equipment = Equipment.objects.get(
            id=request.POST["equipment"]
        )

        subequipment.sub_eqpt_code = code
        subequipment.sub_eqpt_desc = request.POST["sub_eqpt_desc"]

        subequipment.save()

        messages.success(
            request,
            "Sub Equipment Updated Successfully."
        )

        return redirect("subequipment_list")

    return render(
        request,
        "masters/subequipment_form.html",
        {
            "subequipment": subequipment,
            "equipment": Equipment.objects.all(),
        }
    )
def subequipment_delete(request, id):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.session.get("role") != "Admin":
        return redirect("dashboard")

    subequipment = get_object_or_404(
        SubEquipment,
        id=id
    )

    subequipment.delete()

    messages.success(
        request,
        "Sub Equipment Deleted Successfully."
    )

    return redirect("subequipment_list")