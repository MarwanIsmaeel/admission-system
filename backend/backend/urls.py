from django.contrib import admin 
from django.urls import include, path
from applications import views



urlpatterns = [ path("admin/", admin.site.urls),
               path(
                    "media/documents/applications/<path:filename>",
                    views.protected_application_document,
                    name="protected_application_document",
                    ),

                path("", include("applications.urls")),
               ]