# coding: utf-8
from rest_framework import (
    renderers,
    viewsets,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kpi.serializers.v2.service_usage import ServiceUsageSerializer
from kpi.utils.object_permission import get_database_user


class ServiceUsageViewSet(viewsets.ViewSet):
    """
    ## Service Usage Tracker
    Tracks the submissions for the current month
    Tracks the current total storage used
    <pre class="prettyprint">
    <b>GET</b> /api/v2/service_usage/
    </pre>

    > Example
    >
    >       curl -X GET https://[kpi]/api/v2/service_usage/
    >       {
    >           "total_nlp_asr_seconds": {integer},
    >           "total_nlp_mt_characters": {integer},
    >           "total_storage_bytes": {integer},
    >           "total_submission_count_current_month": {integer},
    >           "total_submission_count_all_time": {integer},
    >       }


    ### CURRENT ENDPOINT
    """
    renderer_classes = (
        renderers.BrowsableAPIRenderer,
        renderers.JSONRenderer,
    )
    pagination_class = None
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        """
        Extra context provided to the serializer class.
        """
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def list(self, request, *args, **kwargs):
        serializer = ServiceUsageSerializer(
            get_database_user(request.user),
            context=self.get_serializer_context(),
        )
        return Response(serializer.data)
