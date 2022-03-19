from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from .forms import LoginForm, UserPasswordChangeForm

urlpatterns = [
    path('', views.ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('mobile/', views.mobile, name='mobile'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    path('resetpasswordsuccess/', auth_views.PasswordChangeDoneView.as_view(template_name='app/resetpasswordsuccess.html'), name='resetpasswordsuccess'),

    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name='app/resetpassword.html', form_class=UserPasswordChangeForm, success_url='/resetpasswordsuccess/'), name='changepassword'),
    
    path('cart/', views.add_to_cart, name='add-to-cart'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    
    
    path('checkout/', views.checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
