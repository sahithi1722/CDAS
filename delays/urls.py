from django.urls import path
from . import views

urlpatterns = [
    path("entry/", views.delay_entry, name="delay_entry"),
    path("list/", views.delay_list, name="delay_list"),

    path("edit/<int:id>/", views.edit_delay, name="edit_delay"),
    path("delete/<int:id>/", views.delete_delay, name="delete_delay"),

    path("ajax/get-equipment/", views.get_equipment, name="get_equipment"),
    path("ajax/get-sub-equipment/", views.get_sub_equipment, name="get_sub_equipment"),
path(
    "history/<int:id>/",
    views.equipment_history,
    name="equipment_history"
),
path(
    "history-log/<int:id>/",
    views.delay_history,
    name="delay_history",
),
]