from django.urls import path
from workatolist.phonecalls.views import CallView

app_name = 'phonecalls'

urlpatterns = [
    path('call/', CallView.as_view(), name='call'),

]
