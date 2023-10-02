from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

from .serializer import ChannelSerializer, ServerSerializer

server_list_doc = extend_schema(
    responses=ServerSerializer(many=True),
    parameters=[
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="Category of servers to retrieve",
        ),
        OpenApiParameter(
            name="quantity",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Number of servers to retrieve",
        ),
        OpenApiParameter(
            name="by_user",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Filter servers by given user",
        ),
        OpenApiParameter(
            name="with_num_member",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="Include the number of servers for each member",
        ),
        OpenApiParameter(
            name="by_serverid",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Include server by id",
        ),
    ],
)
