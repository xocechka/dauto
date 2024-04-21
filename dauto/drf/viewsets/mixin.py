from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response


# noinspection PyUnresolvedReferences
class CreateVerboseModelMixin(mixins.CreateModelMixin):
    """
    Description:
        This class is a mixin that extends the functionality of the CreateModelMixin class. It provides additional methods for handling the creation of objects with verbose output.

    Methods:
    - get_read_object: Returns the read object.
    - get_read_serializer: Returns the serializer instance.
    - create: Returns a response containing the created object data.
    """
    # noinspection PyMethodMayBeStatic
    def get_read_object(self, instance):
        return instance

    def get_read_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        method = self.request.method
        self.request.method = "GET"
        serializer_class = self.get_serializer_class()
        self.request.method = method
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        read_serializer = self.get_read_serializer(self.get_read_object(serializer.instance))
        return Response(
            read_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


# noinspection PyUnresolvedReferences
class UpdateVerboseModelMixin(mixins.UpdateModelMixin):
    """
    Description:
        This class is a mixin that provides additional functionality for updating models with verbose output.

    Methods:
    - get_read_object: Returns the object being read.
    - get_read_serializer: Returns the serializer instance used for validating, deserializing input, and serializing output.
    - update: Updates the model instance with the provided data and returns the serialized read data.
    """
    # noinspection PyMethodMayBeStatic
    def get_read_object(self, instance):
        return instance

    def get_read_serializer(self, *args, **kwargs):
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        method = self.request.method
        self.request.method = "GET"
        serializer_class = self.get_serializer_class()
        self.request.method = method
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        read_serializer = self.get_read_serializer(self.get_read_object(serializer.instance))
        return Response(read_serializer.data)
