from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
from myapp.views import ResetPasswordView

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'login/', views.user_login, name='login'),
    path(r'logout/', views.user_logout, name='logout'),
    path(r'about', views.about, name='about'),
    path(r'<int:cat_no>', views.detail, name='detail'),
    path(r'products/', views.products, name='products'),
    path(r'place_order/', views.place_order, name='placeOrder'),
    path(r'products/<int:prod_id>/', views.productdetail, name='productDetail'),
    path(r'myorders/', views.myorders, name='myorders'),
    path(r'register', views.register, name="register"),
    path(r'profile/', views.profile, name='users-profile'),

    path(r'password-reset/', ResetPasswordView.as_view(), name='password_reset'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='myapp/password_reset_complete.html'),
         name='password_reset_complete'),

]
