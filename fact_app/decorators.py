from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.admin.views.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin

def superuser_required(
  function= None, redirect_field_name= REDIRECT_FIELD_NAME, login_url=None
):
  
  
  actual_decorator = user_passes_test(
    lambda u: u.is_active and u.is_superuser,
    login_url= login_url,
    redirect_field_name=redirect_field_name,
  )
  if function:
    return actual_decorator(function)
  return actual_decorator

class LoginRequiredSuperuserMixim(UserPassesTestMixin):
  
    def test_func(self):
      return self.request.user.is_superuser