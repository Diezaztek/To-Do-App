"""todo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.go_home, name='home'),

    #Auth
    path('signup/', views.sign_up, name='sign_up'),
    path('logout/', views.log_out, name='log_out'),
    path('login/', views.log_in, name='log_in'),

    #Tasks
    path('tasks/', views.show_current_tasks, name='tasks'),
    path('completed/', views.show_completed_tasks, name='completed_tasks'),
    path('create/', views.create_task, name='create'),
    path('tasks/<int:task_pk>', views.edit_task, name='edit_task'),
    path('tasks/<int:task_pk>/complete', views.complete_task, name='complete_task'),
    path('tasks/<int:task_pk>/delete', views.delete_task, name='delete_task'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
