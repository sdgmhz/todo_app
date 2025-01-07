from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """ check to see if the author of the duty is implementing with it """
    def has_object_permission(self, request, view, obj):
        return obj.author.profile.user == request.user
    

""" I think I have done this functionality in view by get_queryset method and this code is unnecessary """