from rest_framework import permissions


class IsOrganizerMyEvent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.organizer.id == request.user.id