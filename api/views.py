from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Mine
from .serializers import MineSerializer
from .pagination import StandardResultsSetPagination
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse

@api_view(['GET'])
def custom_api_root(request, format=None):
    return Response({
        'Mines API Database': reverse('mine-list', request=request, format=format),
        'Raw Data List (Unpaginated)': request.build_absolute_uri('/api/mines/raw_list/'),
        'Mines Summary Statistics': request.build_absolute_uri('/api/mines/summary/'),
        'Mines by Region': request.build_absolute_uri('/api/mines/by_region/'),
        'Interactive OpenAPI Docs': request.build_absolute_uri('/api/docs/'),
    })

class MineViewSet(viewsets.ModelViewSet):
    queryset = Mine.objects.all().order_by('mine_site_name')
    serializer_class = MineSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering
    filterset_fields = {
        'certification_status': ['exact'],
        'activity_status': ['exact'],
        'license_type': ['exact'],
        'admin1': ['exact'],
        'admin2': ['exact'],
        'country_iso2': ['exact'],
    }
    
    # Search
    search_fields = ['mine_site_name', 'national_id', 'license_id', 
                    'owner_company_id', 'operator_company_id']
    
    # Ordering
    ordering_fields = ['mine_site_name', 'certification_status', 
                      'activity_status', 'last_inspection_date']
    ordering = ['mine_site_name']
    
    # Removed get_serializer_class to allow list views to use the primary MineSerializer
    
    @extend_schema(responses=MineSerializer(many=True), description="Get an unpaginated pure list array of all mine data")
    @action(detail=False, methods=['get'])
    def raw_list(self, request):
        """Get an unpaginated pure list array of all mine data"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get summary statistics"""
        summary = {
            'total_mines': Mine.objects.count(),
            'by_certification': dict(Mine.objects.values_list('certification_status')
                                     .annotate(count=Count('id'))),
            'by_activity': dict(Mine.objects.values_list('activity_status')
                               .annotate(count=Count('id'))),
            'by_license_type': dict(Mine.objects.values_list('license_type')
                                   .annotate(count=Count('id'))),
            'by_region': dict(Mine.objects.values_list('admin1')
                             .annotate(count=Count('id'))),
        }
        return Response(summary)
    
    @action(detail=False, methods=['get'])
    def by_region(self, request):
        """Get mines grouped by region"""
        region = request.query_params.get('region', None)
        queryset = self.get_queryset()
        
        if region:
            queryset = queryset.filter(admin1=region)
        
        regions = queryset.values('admin1', 'admin2').annotate(
            count=Count('id'),
            active_count=Count('id', filter=Q(activity_status='Active')),
            certified_count=Count('id', filter=~Q(certification_status='Red'))
        )
        return Response(regions)
    
    @action(detail=False, methods=['get'])
    def search_advanced(self, request):
        """Advanced search with multiple parameters"""
        queryset = self.get_queryset()
        
        # Get query parameters
        name = request.query_params.get('name', None)
        status_param = request.query_params.get('status', None)
        cert = request.query_params.get('certification', None)
        region = request.query_params.get('region', None)
        mineral = request.query_params.get('mineral', None)
        
        # Apply filters
        if name:
            queryset = queryset.filter(mine_site_name__icontains=name)
        if status_param:
            queryset = queryset.filter(activity_status=status_param)
        if cert:
            queryset = queryset.filter(certification_status=cert)
        if region:
            queryset = queryset.filter(Q(admin1=region) | Q(admin2=region))
        if mineral:
            queryset = queryset.filter(
                Q(primary_mineral_hs_code=mineral) |
                Q(additional_minerals_hs_codes__icontains=mineral)
            )
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data
        })
