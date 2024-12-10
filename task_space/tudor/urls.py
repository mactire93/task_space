from django.urls import path
from . import views # importuję widoki z kat. równorzędnego

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('update_password/', views.update_password, name='update_password'),
    path('view_task/<int:pk>', views.view_task, name='view_task'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('check_boxes', views.check_boxes, name='check_boxes'),
    path('add_task', views.add_task, name='add_task'),
    path('delete_task/<int:pk>', views.delete_task, name='delete_task'),
    path('finish_task/<int:pk>', views.finish_task, name='finish_task'),
    path('return_task/<int:pk>', views.return_task, name='return_task'),
    path('delete_note/<int:note_id>/<int:pk>', views.delete_note, name='delete_note'),
    path('delete_item/<int:pk>/<int:item_id>', views.delete_item, name='delete_item'),
    path('edit_task/<int:pk>', views.edit_task, name='edit_task'),
    path('edit_note/<int:pk>/<int:note_id>', views.edit_note, name='edit_note'),
    path('finished_tasks', views.finished_tasks, name='finished_tasks'),
]
