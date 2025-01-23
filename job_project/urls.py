from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('contact_us/', include('contact_us.urls')),
    path('employer/', include('employer.urls')),
    path('applications/', include('applications.urls')),
    # path('catagory/', include('job_catagory.urls')),
    # path('job_post/', include('job_post.urls')),
    path('jobseeker/', include('jobseeker.urls')),
    path('jobs/', include('jobs.urls')),
    # path('service/', include('service.urls')),
    
    # to implement authentication facility only in DRF panel
    path("api-auth/", include("rest_framework.urls")),

    
]

# adding onto the urlpatterns
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)