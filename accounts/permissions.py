from rest_framework.permissions import BasePermission


class IsAdministrator(BasePermission):
    """
    Allows access to administrators only.
    """

    message = "You must be an administrator to perform this action."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.role == "ADMIN"
        )


class IsTeacher(BasePermission):
    """
    Allows access to teachers only.
    """

    message = "You must be a teacher to perform this action."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.role == "TEACHER"
        )


class IsStudent(BasePermission):
    """
    Allows access to students only.
    """

    message = "You must be a student to perform this action."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.role == "STUDENT"
        )


class IsTeacherOrAdministrator(BasePermission):
    """
    Allows access to teachers and administrators.
    """

    message = "You must be a teacher or administrator to perform this action."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.role in ("TEACHER", "ADMIN")
        )


class IsStudentOrAdministrator(BasePermission):
    """
    Allows access to students and administrators.
    """

    message = "You must be a student or administrator to perform this action."

    def has_permission(self, request, view):
        user = request.user

        return bool(
            user
            and user.is_authenticated
            and user.role in ("STUDENT", "ADMIN")
        )
