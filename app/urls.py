from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .forms import LoginForm, UserPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm

urlpatterns = [
    path('', views.ProductSneekPeak.as_view(), name='home'),

    # Basic urls
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('ram/<slug:data>', views.ram, name='ramdata'),
    path('ram/', views.ram, name='ram'),

    # Auth
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm, next_page='/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Change password
    path('changepasswordsuccess/', auth_views.PasswordChangeDoneView.as_view(template_name='app/changepasswordsuccess.html'), name='changepasswordsuccess'),
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/changepassword.html', form_class=UserPasswordChangeForm, success_url='/changepasswordsuccess/'), name='changepassword'),

    # Reset password
    path('resetpassword/', auth_views.PasswordResetView.as_view(template_name='app/reset_password.html', form_class=MyPasswordResetForm), name="resetpassword"),
    path('resetpassword/done/', auth_views.PasswordResetDoneView.as_view(template_name='app/reset_password_done.html'), name="password_reset_done"),
    path('resetpasswordconfirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='app/reset_password_confirm.html', form_class=MySetPasswordForm), name="password_reset_confirm"),
    path('resetpasswordsuccess', auth_views.PasswordResetCompleteView.as_view(template_name='app/reset_password_complete.html'), name="password_reset_complete"),
    
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    
    
    path('checkout/', views.checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
