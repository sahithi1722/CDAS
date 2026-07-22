from django.urls import path
from . import views

urlpatterns = [

    # Masters Home
    path(
        "",
        views.master_home,
        name="master_home"
    ),

    # Shop Master
    path(
        "shops/",
        views.shop_list,
        name="shop_list"
    ),

    path(
        "shops/add/",
        views.shop_add,
        name="shop_add"
    ),

    path(
        "shops/delete/<int:id>/",
        views.shop_delete,
        name="shop_delete"
    ),

    # Equipment Master
    path(
        "equipment/",
        views.equipment_list,
        name="equipment_list"
    ),

    path(
        "equipment/add/",
        views.equipment_add,
        name="equipment_add"
    ),
    path(
    "shops/edit/<int:id>/",
    views.shop_edit,
    name="shop_edit"),
    path(
    "equipment/edit/<int:id>/",
    views.equipment_edit,
    name="equipment_edit"),
    path(
    "equipment/delete/<int:id>/",
    views.equipment_delete,
    name="equipment_delete"),
    path("subequipment/", views.subequipment_list, name="subequipment_list"),
    path("subequipment/add/", views.subequipment_add, name="subequipment_add"),
    path("subequipment/edit/<int:id>/", views.subequipment_edit, name="subequipment_edit"),
    path("subequipment/delete/<int:id>/", views.subequipment_delete, name="subequipment_delete"),
    path("agency/", views.agency_list, name="agency_list"),
    path("agency/add/", views.agency_add, name="agency_add"),
    path("agency/edit/<int:id>/", views.agency_edit, name="agency_edit"),
    path("agency/delete/<int:id>/", views.agency_delete, name="agency_delete"),
]