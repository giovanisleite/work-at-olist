from django.urls import re_path
from workatolist.phonecalls.views import CallView, BillView

app_name = 'phonecalls'

urlpatterns = [
    re_path(r'^call/?$', CallView.as_view(), name='call'),
    re_path(r'^bill/(?P<phone>\w{10,11})/?$', BillView.as_view(), name='bill'),
]
