from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    def list(self, request):
        category = request.query_params.get("category")
        quantity = request.query_params.get("quantity")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_member = request.query_params.get("with_num_member") == "true"

        if by_user or by_serverid and not request.user.is_authenticated:
            raise AuthenticationFailed()
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            user_id = request.user.id
            self.queryset = self.queryset.filter(member=user_id)

        if with_num_member:
            self.queryset = self.queryset.annotate(num_member=Count("member"))

        if quantity:
            self.queryset = self.queryset[: int(quantity)]

        if by_serverid:
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverid} not found")
            except ValueError:
                raise ValidationError(detail="Server with ValueError")

        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_member})
        return Response(serializer.data)
