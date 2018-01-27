from django.urls import path
from workatolist.phonecalls.views import CallView, BillView

app_name = 'phonecalls'

urlpatterns = [
    path('call/', CallView.as_view(), name='call'),
    path('bill/<str:phone>', BillView.as_view(), name='bill'),
]
