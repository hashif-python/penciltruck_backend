from django.contrib.auth.decorators import user_passes_test


def is_superadmin(user):
    return user.is_authenticated and user.is_superuser 
