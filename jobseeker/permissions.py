from rest_framework import permissions



# permission defined for job_seeker user
class IsJobSeekerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        print("User:", request.user)

        # all the viewer (if users are not authenticated) can view
        if request.method in permissions.SAFE_METHODS:
            return True
        # also, the Authenticated users & jobseeker only can see list view
        if request.user.is_authenticated and request.user.user_type == 'jobseeker':
            return True
        else:
            return False
    
    
    # N.B.: the below declared 'has_object_permission' function will only execute if the above created 'has_permission' function returns True

    def has_object_permission(self, request, view, obj):
        # providing read permission (GET, HEAD or options request)  by allowing SAFE_METHODS to all users
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            # providing Write permission (PUT or PATCH)  only to  the jobseeker of a post
            if request.user.user_type == 'jobseeker':
                return True
            else:
                return False
    



    
# permission defined for job-seeker type user
class IsJobSeekerUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.user_type == 'jobseeker':
            return True
        else:
            return False