from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth
from delays.models import Delay
import openpyxl
from openpyxl.styles import Font
from openpyxl import Workbook
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)

import os
import json


from masters.models import (
    Shop,
    Equipment
)

from delays.models import Delay

from django.contrib.auth.models import User



# ==================================================
# REPORT HOME
# ==================================================





def report_home(request):

    # Total delays
    total_delays = Delay.objects.count()


    # Total delay hours
    total_duration = Delay.objects.aggregate(
        total=Sum('delay_duration')
    )['total']


    if total_duration:
        total_hours = round(
            total_duration.total_seconds() / 3600,
            2
        )
    else:
        total_hours = 0



    # Average duration in minutes
    avg_duration = Delay.objects.aggregate(
        avg=Avg('delay_duration')
    )['avg']


    if avg_duration:
        avg_duration = round(
            avg_duration.total_seconds() / 60,
            2
        )
    else:
        avg_duration = 0




    # Shops affected
    shops_count = (
        Delay.objects.values('shop')
        .distinct()
        .count()
    )





    # Shop wise chart

    shop_data = (
        Delay.objects
        .values('shop__shop_desc')
        .annotate(total=Count('id'))
        .order_by('-total')
    )


    shop_labels = [
        item['shop__shop_desc']
        for item in shop_data
    ]


    shop_values = [
        item['total']
        for item in shop_data
    ]







    # Agency wise chart

    agency_data = (
        Delay.objects
        .values('agency__agency_name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )


    agency_labels = [
        item['agency__agency_name']
        for item in agency_data
    ]


    agency_values = [
        item['total']
        for item in agency_data
    ]
    equipment_data = (
    Delay.objects
    .values('equipment__eqpt_desc')
    .annotate(total=Count('id'))
    .order_by('-total')[:10]
)
    equipment_labels = [
    item['equipment__eqpt_desc']
    for item in equipment_data
]
    equipment_values = [
    item['total']
    for item in equipment_data
]
    monthly_data = (
    Delay.objects
    .annotate(month=TruncMonth('delay_from'))
    .values('month')
    .annotate(total=Count('id'))
    .order_by('month')
)
    monthly_labels = [
    item['month'].strftime('%b %Y')
    for item in monthly_data
]
    monthly_values = [
    item['total']
    for item in monthly_data
]






    context = {


        "total_delays": total_delays,


        "total_hours": total_hours,


        "avg_duration": avg_duration,


        "shops_count": shops_count,


        "shop_labels": shop_labels,


        "shop_values": shop_values,


        "agency_labels": agency_labels,


        "agency_values": agency_values,
        "equipment_labels": equipment_labels,

"equipment_values": equipment_values,
"monthly_labels": monthly_labels,

"monthly_values": monthly_values,


    }



    return render(
        request,
        "reports/report_home.html",
        context
    )


# ==================================================
# EXCEL EXPORT
# ==================================================

def export_excel(request):

    wb = Workbook()

    ws = wb.active

    ws.title = "Delay Report"


    ws.append([
        "Shop",
        "Equipment",
        "Sub Equipment",
        "Agency",
        "Delay From",
        "Delay Upto",
        "Duration",
        "Description",
        "Entered By"
    ])


    delays = Delay.objects.select_related(
        "shop",
        "equipment",
        "sub_equipment",
        "agency"
    )


    for d in delays:

        ws.append([

            d.shop.shop_desc,

            d.equipment.eqpt_desc,

            d.sub_equipment.sub_eqpt_desc,

            d.agency.agency_name,

            d.delay_from.strftime(
                "%d-%m-%Y %H:%M"
            ),

            d.delay_upto.strftime(
                "%d-%m-%Y %H:%M"
            ),

            str(d.delay_duration),

            d.delay_desc,

            d.entered_by

        ])


    response = HttpResponse(
        content_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


    response["Content-Disposition"] = (
        'attachment; filename="Delay_Report.xlsx"'
    )


    wb.save(response)


    return response





# ==================================================
# PRINT REPORT
# ==================================================

def print_report(request):

    delays = Delay.objects.select_related(
        "shop",
        "equipment",
        "sub_equipment",
        "agency"
    ).order_by("-delay_from")


    return render(
        request,
        "reports/print_report.html",
        {
            "delays":delays
        }
    )





# ==================================================
# ACTIVITY LOG
# ==================================================

def activity_log(request):

    logs = Delay.objects.select_related(
        "shop",
        "equipment",
        "sub_equipment",
        "agency"
    ).order_by("-created_at")


    return render(
        request,
        "reports/activity_log.html",
        {
            "logs":logs
        }
    )





# ==================================================
# DATABASE BACKUP
# ==================================================

def backup_database(request):

    backup_file = os.path.join(
        settings.BASE_DIR,
        "cdas_backup.sql"
    )


    command = (
        'mysqldump -u root -pMysql@123 cdas_db > "{}"'
        .format(backup_file)
    )


    os.system(command)


    with open(
        backup_file,
        "rb"
    ) as f:


        response = HttpResponse(
            f.read(),
            content_type="application/sql"
        )


        response["Content-Disposition"] = (
            'attachment; filename="cdas_backup.sql"'
        )


        return response





# ==================================================
# PDF EXPORT
# ==================================================

def export_pdf(request):

    response = HttpResponse(
        content_type="application/pdf"
    )


    response["Content-Disposition"] = (
        'attachment; filename="Delay_Report.pdf"'
    )


    doc = SimpleDocTemplate(response)


    elements=[]


    styles=getSampleStyleSheet()


    elements.append(
        Paragraph(
            "Centralized Delay Analysis System",
            styles["Heading1"]
        )
    )


    data=[

        [
            "Date",
            "Shop",
            "Equipment",
            "Agency",
            "Duration"
        ]

    ]


    delays=Delay.objects.select_related(
        "shop",
        "equipment",
        "agency"
    )


    for d in delays:

        data.append([

            d.delay_from.strftime("%d-%m-%Y"),

            d.shop.shop_desc,

            d.equipment.eqpt_desc,

            d.agency.agency_name,

            str(d.delay_duration)

        ])


    table=Table(data)


    table.setStyle(
        TableStyle([

            (
            "GRID",
            (0,0),
            (-1,-1),
            1,
            colors.black
            )

        ])
    )


    elements.append(table)


    doc.build(elements)


    return response





# ==================================================
# COMMON REPORTS
# ==================================================

def shop_wise_report(request):

    report = (
        Delay.objects
        .values("shop__shop_desc")
        .annotate(total=Count("id"))
    )


    return render(
        request,
        "reports/shop_wise_report.html",
        {
            "report":report
        }
    )



def equipment_wise_report(request):

    report=(

        Delay.objects
        .values("equipment__eqpt_desc")
        .annotate(total=Count("id"))

    )


    return render(
        request,
        "reports/equipment_wise_report.html",
        {
            "report":report
        }
    )




def agency_wise_report(request):

    report=(

        Delay.objects
        .values("agency__agency_name")
        .annotate(total=Count("id"))

    )


    return render(
        request,
        "reports/agency_wise_report.html",
        {
            "report":report
        }
    )




def date_wise_report(request):

    delays=Delay.objects.all()


    from_date=request.GET.get("from_date")

    to_date=request.GET.get("to_date")


    if from_date:

        delays=delays.filter(
            delay_from__date__gte=from_date
        )


    if to_date:

        delays=delays.filter(
            delay_from__date__lte=to_date
        )


    return render(
        request,
        "reports/date_wise_report.html",
        {
            "delays":delays
        }
    )





def monthly_report(request):

    report=(

        Delay.objects
        .annotate(
            month=TruncMonth("delay_from")
        )
        .values("month")
        .annotate(
            total=Count("id")
        )

    )


    return render(
        request,
        "reports/monthly_report.html",
        {
            "report":report
        }
    )





# ==================================================
# MAIN ANALYTICS DASHBOARD
# ==================================================
# ==================================================
# MAIN ANALYTICS DASHBOARD
# ==================================================

from django.shortcuts import render
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth

from delays.models import Delay
from masters.models import Shop, Agency



def reports_dashboard(request):

    delays = Delay.objects.all()


    # -----------------------------
    # FILTERS
    # -----------------------------

    shop = request.GET.get("shop")
    agency = request.GET.get("agency")
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")


    if shop:
        delays = delays.filter(shop_id=shop)


    if agency:
        delays = delays.filter(agency_id=agency)


    if from_date:
        delays = delays.filter(
            delay_from__date__gte=from_date
        )


    if to_date:
        delays = delays.filter(
            delay_from__date__lte=to_date
        )



    # -----------------------------
    # SUMMARY CARDS
    # -----------------------------

    total_delays = delays.count()


    duration = delays.aggregate(
        total=Sum("delay_duration")
    )["total"]


    if duration:
        total_hours = round(
            duration.total_seconds() / 3600,
            2
        )
    else:
        total_hours = 0



    avg = delays.aggregate(
        average=Avg("delay_duration")
    )["average"]


    if avg:
        average_duration = str(avg)
    else:
        average_duration = "0"



    shops_covered = (
        delays.values("shop")
        .distinct()
        .count()
    )





    # -----------------------------
    # TOP EQUIPMENT
    # -----------------------------

    top_equipment = (

        delays.values(
            "equipment__eqpt_desc"
        )

        .annotate(
            count=Count("id"),
            duration=Sum(
                "delay_duration"
            )
        )

        .order_by("-count")[:10]

    )





    # -----------------------------
    # MONTHLY TREND
    # -----------------------------


    monthly_data = (

        delays.annotate(
            month=TruncMonth(
                "delay_from"
            )
        )

        .values("month")

        .annotate(
            total=Count("id")
        )

        .order_by("month")

    )


    months = []
    month_values = []


    for item in monthly_data:

        months.append(
            item["month"].strftime("%b")
        )

        month_values.append(
            item["total"]
        )





    # -----------------------------
    # AGENCY DISTRIBUTION
    # -----------------------------


    agency_data = (

        delays.values(
            "agency__agency_name"
        )

        .annotate(
            total=Count("id")
        )

        .order_by("-total")

    )


    agency_labels = []
    agency_values = []


    for item in agency_data:

        agency_labels.append(
            item["agency__agency_name"]
        )

        agency_values.append(
            item["total"]
        )





    # -----------------------------
    # TOP DELAY CAUSES
    # -----------------------------


    causes = (

        delays.values(
            "delay_desc"
        )

        .annotate(
            total=Count("id")
        )

        .order_by("-total")[:5]

    )





    context = {

        "shops":
            Shop.objects.all(),

        "agencies":
            Agency.objects.all(),


        "total_delays":
            total_delays,


        "total_hours":
            total_hours,


        "average_duration":
            average_duration,


        "shops_covered":
            shops_covered,


        "top_equipment":
            top_equipment,


        "months":
            months,


        "month_values":
            month_values,


        "agency_labels":
            agency_labels,


        "agency_values":
            agency_values,


        "causes":
            causes,

    }


    return render(
        request,
        "reports/dashboard.html",
        context
    )
# ==================================================
# PAGE 4 : DELAY REPORTS
# ==================================================

def delay_reports(request):


    shops=Shop.objects.all()



    delays=Delay.objects.select_related(

        "shop",

        "equipment",

        "sub_equipment",

        "agency"

    ).order_by(
        "-delay_from"
    )



    shop=request.GET.get("shop")

    from_date=request.GET.get("from_date")

    to_date=request.GET.get("to_date")



    if shop and shop!="all":

        delays=delays.filter(
            shop_id=shop
        )


    if from_date:

        delays=delays.filter(
            delay_from__date__gte=from_date
        )


    if to_date:

        delays=delays.filter(
            delay_from__date__lte=to_date
        )



    total_delays=delays.count()



    total_minutes=sum(

        int(
            d.delay_duration.total_seconds()/60
        )

        for d in delays
        if d.delay_duration

    )



    hours=total_minutes//60

    minutes=total_minutes%60



    duration_text=(

        f"{total_minutes} min "
        f"({hours}h {minutes}m)"

    )



    context={


        "shops":shops,


        "delays":delays,


        "total_delays":
        total_delays,


        "total_duration":
        duration_text,


    }



    return render(

        request,

        "reports/delay_reports.html",

        context

    )
def export_reports(request):

    workbook = openpyxl.Workbook()

    sheet = workbook.active
    sheet.title = "Delay Reports"


    # Header row

    sheet.append([
        "ID",
        "Shop",
        "Equipment",
        "Agency",
        "Delay Description",
        "Delay From",
        "Delay Upto",
        "Duration"
    ])


    for cell in sheet[1]:
        cell.font = Font(bold=True)



    delays = Delay.objects.select_related(
        'shop',
        'equipment',
        'agency'
    )


    for delay in delays:

        sheet.append([

            delay.id,

            delay.shop.shop_desc,

            delay.equipment.eqpt_desc,

            delay.agency.agency_name,

            delay.delay_desc,

            delay.delay_from.strftime("%d-%m-%Y %H:%M"),

            delay.delay_upto.strftime("%d-%m-%Y %H:%M"),

            str(delay.delay_duration)

        ])




    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


    response['Content-Disposition'] = (
        'attachment; filename="CDAS_Delay_Report.xlsx"'
    )


    workbook.save(response)


    return response