from django.urls import path, include
from . import views

urlpatterns = [
    path('/new', views.new_user),
    path('/edit', views.edit_self),
    path('/update_info', views.update_info),
    path('/update_pw', views.update_pw),
    path('/update_desc', views.update_desc),
    path('/edit/<int:num>', views.edit_user),
    path('/show/<int:num>', views.show_user),
    path('/<int:num>/post', views.post),
    path('/<int:num>/<int:num1>/comment', views.comment)
]