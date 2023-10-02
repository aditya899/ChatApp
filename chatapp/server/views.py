from django.db.models import Count
from rest_framework import viewsets
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response

from .models import Server
from .schema import server_list_doc
from .serializer import ServerSerializer


class ServerListViewSet(viewsets.ViewSet):
    queryset = Server.objects.all()

    @server_list_doc
    def list(self, request):
        category = request.query_params.get("category")
        quantity = request.query_params.get("quantity")
        by_user = request.query_params.get("by_user") == "true"
        by_serverid = request.query_params.get("by_serverid")
        with_num_member = request.query_params.get("with_num_member") == "true"

        # if by_user or by_serverid and not request.user.is_authenticated:
        #     raise AuthenticationFailed()
        if category:
            self.queryset = self.queryset.filter(category__name=category)

        if by_user:
            if request.user.is_authenticated:
                user_id = request.user.id
                self.queryset = self.queryset.filter(member=user_id)
            else:
                raise AuthenticationFailed()

        if with_num_member:
            self.queryset = self.queryset.annotate(num_member=Count("member"))

        if quantity:
            self.queryset = self.queryset[: int(quantity)]

        if by_serverid:
            if not request.user.is_authenticated:
                raise AuthenticationFailed()
            try:
                self.queryset = self.queryset.filter(id=by_serverid)
                if not self.queryset.exists():
                    raise ValidationError(detail=f"Server with id {by_serverid} not found")
            except ValueError:
                raise ValidationError(detail="Server with ValueError")

        serializer = ServerSerializer(self.queryset, many=True, context={"num_members": with_num_member})
        return Response(serializer.data)
