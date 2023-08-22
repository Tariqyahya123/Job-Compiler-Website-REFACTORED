from django.contrib import admin
from django.urls import path
from scrape.views import returnHome, renderResults, renderStarred


urlpatterns = [
 #   path('admin/', admin.site.urls),
    path('results/', renderResults),
    path('starred/', renderStarred),
    path('', returnHome, name ='scrape-data'),
]
