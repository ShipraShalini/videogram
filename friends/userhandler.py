from django.contrib.auth.models import User
from django.forms import model_to_dict



class UserHandler:

    def create(self, username, first_name, last_name, email, password):
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        user.set_password(password)
        user.save()
        return model_to_dict(user)

    def retrieve(self, user):
        return model_to_dict(user)

    def modify(self, user, first_name, last_name, email):
        """Delete User"""
        user.first_name = first_name or user.first_name,
        user.last_name = last_name or user.last_name,
        user.email = email or user.email
        user.save()
        return model_to_dict(user)

    def delete(self, user):
        """Delete user."""
        user.delete()
