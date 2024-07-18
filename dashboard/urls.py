from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'dashboard'  

urlpatterns = [
    path('', views.index, name="dashboard"),
    path('orders', views.orders, name="orders"),

    path('login', views.admin_login, name="admin_login"),
	path('logout', views.admin_logout, name="admin_logout"),

    path('order/<int:order_id>/', views.order_details, name='order_details'),
    path('add_book/', views.add_book_view, name='add_book'),
    path('books_list/', views.books_list, name='books_list'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('change_payment_status/<int:order_id>/', views.change_payment_status, name='change_payment_status'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('mark_messages_as_read/', views.mark_messages_as_read, name='mark_messages_as_read'),
    path('all_messages/', views.all_messages, name='all_messages'),
    path('add_category/', views.add_category, name='add_category'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('all_categories/', views.categoriesView, name='all_categories'),
    
    path('add_writer/', views.add_writer, name='add_writer'),
    path('writers/', views.writers, name='writers'),
    path('delete_writer/<int:writer_id>/', views.delete_writer, name='delete_writer'),





]