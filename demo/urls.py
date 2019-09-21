from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>',views.xinxi_detail,name = "xinxi_detail"),
    path('query/',views.xinxi_query,name = "xinxi_query"),
    path('check/',views.xinxi_check,name = "xinxi_check"),
    path('type/<int:id>',views.xinxi_type,name="xinxi_type"),
]