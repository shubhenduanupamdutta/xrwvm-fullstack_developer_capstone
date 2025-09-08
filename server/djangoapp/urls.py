from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = "djangoapp"
urlpatterns = [
    path(route="registration", view=views.registration, name="registration"),
    path(route="login", view=views.login_user, name="login"),
    path(route="logout", view=views.logout_request, name="logout"),
    # path for dealer reviews view
    # path for add a review view
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
