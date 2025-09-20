from django.urls import path
from .views import Visual_aid

urlpatterns = [
    path('visual-aid/' , Visual_aid.as_view() , name='visual-aid')
]