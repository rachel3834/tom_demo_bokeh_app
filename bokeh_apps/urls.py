from django.urls import path
from . import views

app_name = 'bokeh_apps'

urlpatterns = [path("", views.TableView.as_view(), name="tableview")]