from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.elegirVotacion),
    path('exportCSV/<int:idVotacion>', views.exportarCenso),
    path('create/', views.CensusCreate.as_view(), name='census_create'),
    path('<int:voting_id>/', views.CensusDetail.as_view(), name='census_detail'),
]
