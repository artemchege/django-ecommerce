from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.update_cart, name="update"),
    path('validate_form/', views.validate_form, name="validate_form"),
    path('order_paid/', views.completed_order, name="order_paid"),
    path('order_failed/', views.failed_order, name="failed_paid"),
    path('orders/', views.completed_orders, name="orders"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('registration/', views.registration_view, name="registration"),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='store/password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='store/password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='store/password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='store/reset_password_complete.html'),
         name='password_reset_complete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
