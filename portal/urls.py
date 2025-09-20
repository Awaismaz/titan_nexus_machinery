from django.urls import path

from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.LandingPageView.as_view(), name='landing'),
    path('catalogue/', views.MachineListView.as_view(), name='machine_list'),
    path('catalogue/<slug:slug>/', views.MachineDetailView.as_view(), name='machine_detail'),
    path('custom-request/', views.CustomRequestCreateView.as_view(), name='custom_request'),
    path('request/thanks/', views.RequestThankYouView.as_view(), name='request_thanks'),
    path('landing/request/', views.LandingRequestView.as_view(), name='landing_request'),
]
