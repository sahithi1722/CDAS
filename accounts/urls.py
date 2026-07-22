from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # LOGIN
    # =========================

    path(
        "",
        views.login,
        name="login"
    ),


    # =========================
    # DASHBOARD
    # =========================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),


    # =========================
    # LOGOUT
    # =========================

    path(
        "logout/",
        views.logout,
        name="logout"
    ),


    # =========================
    # CHANGE PASSWORD
    # =========================

    path(
        "change-password/",
        views.change_password,
        name="change_password"
    ),


    # =========================
    # USER MANAGEMENT
    # =========================

    path(
        "users/",
        views.user_list,
        name="user_list"
    ),


    path(
        "users/add/",
        views.user_add,
        name="user_add"
    ),


    path(
        "users/edit/<int:id>/",
        views.user_edit,
        name="user_edit"
    ),


    path(
        "users/delete/<int:id>/",
        views.user_delete,
        name="user_delete"
    ),


    # =========================
    # PROFILE
    # =========================

    path(
        "profile/",
        views.profile,
        name="profile"
    ),


    path(
        "profile/update/",
        views.update_profile,
        name="update_profile"
    ),


    # =========================
    # AUDIT LOG
    # =========================

    path(
        "audit-log/",
        views.audit_log,
        name="audit_log"
    ),


    # =========================
    # LOGIN HISTORY
    # =========================

    path(
        "login-history/",
        views.login_history,
        name="login_history"
    ),

]