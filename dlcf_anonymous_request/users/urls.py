from django.urls import path

from dlcf_anonymous_request.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    request_create_view,
    # request_successful_submit,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
