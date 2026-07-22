from django.urls import path
from . import views

urlpatterns = [

    path(
        "",
        views.report_home,
        name="report_home"
    ),


    path("dashboard/", views.reports_dashboard, name="reports_dashboard"),


    path(
        "delay-reports/",
        views.delay_reports,
        name="delay_reports"
    ),


    path(
        "shop-wise/",
        views.shop_wise_report,
        name="shop_wise_report"
    ),


    path(
        "equipment-wise/",
        views.equipment_wise_report,
        name="equipment_wise_report"
    ),


    path(
        "agency-wise/",
        views.agency_wise_report,
        name="agency_wise_report"
    ),


    path(
        "date-wise/",
        views.date_wise_report,
        name="date_wise_report"
    ),


    path(
        "monthly/",
        views.monthly_report,
        name="monthly_report"
    ),


    path(
        "export-excel/",
        views.export_excel,
        name="export_excel"
    ),


    path(
        "export-pdf/",
        views.export_pdf,
        name="export_pdf"
    ),


    path(
        "print/",
        views.print_report,
        name="print_report"
    ),
    path(
    "activity-log/",
    views.activity_log,
    name="activity_log"
),


path(
    "backup/",
    views.backup_database,
    name="backup_database"
),
path(
    'export/',
    views.export_reports,
    name='export_reports'
),

]