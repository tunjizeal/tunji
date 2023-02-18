from rest_framework import (
    renderers,
    viewsets,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kpi.models.asset import Asset
from kpi.paginators import AssetPagination
from kpi.serializers.v2.service_usage import AssetUsageSerializer


class AssetUsageViewSet(viewsets.ViewSet):
    """
    ## Asset Usage Tracker
    Tracks the total and monthly submissions per assert

    <pre class="prettyprint">
    <b>GET</b> /api/v2/asset_usage/
    </pre>

    > Example
    >
    >       curl -X GET https://[kpi]/api/v2/asset_usage/
    >       [
    >           {
    >               "asset": {asset_url},
    >               "asset_name": {string},
    >               "nlp_usage_current_month": {
    >                   "google_asr_seconds": {integer},
    >                   "google_mt_characters": {integer},
    >                   ...
    >               }
    >               "nlp_usage_all_time": {
    >                   "google_asr_seconds": {integer},
    >                   "google_mt_characters": {integer},
    >                   ...
    >               }
    >               "storage_bytes": {integer},
    >               "submission_count_current_month": {integer},
    >               "submission_count_all_time": {integer},
    >           },{...}
    >       ]
    """
    renderer_classes = (
        renderers.BrowsableAPIRenderer,
        renderers.JSONRenderer,
    )
    pagination_class = AssetPagination
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
        queryset = Asset.objects.filter(owner=self.request.user)
        serializer = AssetUsageSerializer(
            queryset,
            many=True,
            read_only=True,
            context=self.get_serializer_context(),
        )
        return Response(serializer.data)

