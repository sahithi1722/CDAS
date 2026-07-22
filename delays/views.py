from datetime import datetime

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings

from .models import Delay, DelayHistory

from masters.models import (
    Shop,
    Equipment,
    SubEquipment,
    Agency
)
from accounts.models import User, AuditLog

# =====================================================
# Delay Entry
# =====================================================

def delay_entry(request):

    if "emp_no" not in request.session:
        return redirect("login")

    if request.method == "POST":

        shop_id = request.POST.get("shop")
        equipment_id = request.POST.get("equipment")
        sub_equipment_id = request.POST.get("sub_equipment")
        agency_id = request.POST.get("agency")

        delay_from = datetime.fromisoformat(
            request.POST.get("delay_from")
        )

        delay_upto = datetime.fromisoformat(
            request.POST.get("delay_upto")
        )

        delay_desc = request.POST.get("delay_desc")

        duration = delay_upto - delay_from

        delay = Delay.objects.create(
            shop_id=shop_id,
            equipment_id=equipment_id,
            subequipment_id=sub_equipment_id,
            agency_id=agency_id,
            delay_from=delay_from,
            delay_upto=delay_upto,
            delay_duration=duration,
            delay_desc=delay_desc,
            entered_by=request.session["emp_name"]
        )

        send_mail(
            subject="New Delay Entered",
            message=f"""
New Delay Entered

Shop:
{delay.shop}

Equipment:
{delay.equipment}

Description:
{delay.delay_desc}

Entered By:
{request.session["emp_name"]}
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[
                "sahithi1722@gmail.com"
            ],
            fail_silently=True,
        )

        DelayHistory.objects.create(
            delay=delay,
            action="Created",
            user=request.session["emp_name"],
            remarks="Delay Entry Created",
        )

        AuditLog.objects.create(
            user=request.session["emp_name"],
            action="ADD DELAY",
            description=f"Added delay {delay.id}",
        )

        messages.success(
            request,
            "Delay Added Successfully"
        )

        return redirect("delay_list")

    return render(
        request,
        "delays/delay_entry.html",
        {
            "shops": Shop.objects.all(),
            "agencies": Agency.objects.all(),
        },
    )


# =====================================================
# Delay List
# =====================================================

def delay_list(request):

    delays = Delay.objects.select_related(

        "shop",

        "equipment",

        "subequipment",

        "agency"

    ).order_by("-delay_from")



    # Filters

    shop = request.GET.get("shop")

    equipment = request.GET.get("equipment")

    agency = request.GET.get("agency")

    from_date = request.GET.get("from_date")

    to_date = request.GET.get("to_date")



    if shop:
        delays = delays.filter(shop_id=shop)


    if equipment:
        delays = delays.filter(equipment_id=equipment)


    if agency:
        delays = delays.filter(agency_id=agency)


    if from_date:
        delays = delays.filter(
            delay_from__date__gte=from_date
        )


    if to_date:
        delays = delays.filter(
            delay_upto__date__lte=to_date
        )



    paginator = Paginator(
        delays,
        10
    )


    page = request.GET.get("page")


    delays = paginator.get_page(page)



    # Duration Formatting

    for delay in delays:

        seconds = int(
            delay.delay_duration.total_seconds()
        )

        hours = seconds // 3600

        minutes = (
            seconds % 3600
        ) // 60


        delay.duration_display = (
            f"{hours}h {minutes}m"
        )



    return render(

        request,

        "delays/delay_list.html",

        {

            "delays": delays,

            "shops": Shop.objects.all(),

            "equipment": Equipment.objects.all(),

            "agencies": Agency.objects.all()

        }

    )



# =====================================================
# AJAX Equipment Dropdown
# =====================================================

def get_equipment(request):

    shop_id = request.GET.get("shop_id")


    equipment = Equipment.objects.filter(

        shop_id=shop_id

    ).values(

        "id",

        "eqpt_desc"

    )


    return JsonResponse(
        list(equipment),
        safe=False
    )



# =====================================================
# AJAX Sub Equipment Dropdown
# =====================================================

def get_sub_equipment(request):

    equipment_id = request.GET.get(
        "equipment_id"
    )


    sub_equipment = SubEquipment.objects.filter(

        equipment_id=equipment_id

    ).values(

        "id",

        "sub_eqpt_desc"

    )


    return JsonResponse(

        list(sub_equipment),

        safe=False

    )



# =====================================================
# Delete Delay
# =====================================================

def delete_delay(request,id):

    delay = get_object_or_404(
        Delay,
        id=id
    )


    AuditLog.objects.create(

        user=request.session["emp_name"],

        action="DELETE DELAY",

        description=f"Deleted Delay {delay.id}"

    )


    DelayHistory.objects.create(

        delay=delay,

        action="Deleted",

        user=request.session["emp_name"],

        remarks="Delay Deleted"

    )


    delay.delete()


    messages.success(
        request,
        "Delay Deleted Successfully"
    )


    return redirect("delay_list")



# =====================================================
# Edit Delay
# =====================================================

def edit_delay(request,id):

    delay = get_object_or_404(
        Delay,
        id=id
    )


    if request.method=="POST":


        delay.shop_id = request.POST.get("shop")

        delay.equipment_id = request.POST.get("equipment")

        delay.subequipment_id = request.POST.get("sub_equipment")

        delay.agency_id = request.POST.get("agency")


        d1 = datetime.fromisoformat(
            request.POST.get("delay_from")
        )

        d2 = datetime.fromisoformat(
            request.POST.get("delay_upto")
        )


        delay.delay_from=d1

        delay.delay_upto=d2

        delay.delay_duration=d2-d1

        delay.delay_desc=request.POST.get(
            "delay_desc"
        )


        delay.save()



        DelayHistory.objects.create(

            delay=delay,

            action="Edited",

            user=request.session["emp_name"],

            remarks="Delay Edited"

        )


        AuditLog.objects.create(

            user=request.session["emp_name"],

            action="EDIT DELAY",

            description=f"Edited Delay {delay.id}"

        )


        return redirect("delay_list")



    return render(

        request,

        "delays/edit_delay.html",

        {

            "delay":delay,

            "shops":Shop.objects.all(),

            "equipment":Equipment.objects.all(),

            "sub_equipment":SubEquipment.objects.all(),

            "agencies":Agency.objects.all()

        }

    )


# =====================================================
# Equipment History
# =====================================================

def equipment_history(request,id):

    equipment=get_object_or_404(
        Equipment,
        id=id
    )


    delays=Delay.objects.filter(

        equipment=equipment

    ).select_related(

        "shop",

        "subequipment",

        "agency"

    ).order_by("-delay_from")



    return render(

        request,

        "delays/equipment_history.html",

        {

            "equipment":equipment,

            "delays":delays

        }

    )



# =====================================================
# Delay History
# =====================================================

def delay_history(request,id):

    history=DelayHistory.objects.filter(

        delay_id=id

    ).order_by("-action_date")



    return render(

        request,

        "delays/delay_history.html",

        {

            "history":history

        }

    )