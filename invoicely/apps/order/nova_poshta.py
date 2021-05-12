from novaposhta import NovaPoshtaApi
from rest_framework.decorators import api_view, authentication_classes, permission_classes, action
from rest_framework.response import Response
from .models import NPWarehouse, Order
from pprint import pprint

client = NovaPoshtaApi(api_key='c3027600bfa68b877b52238709481c66')


def request_status_order(consignment_note):

    request_status = client.internet_document.get_status_documents(consignment_note)

    return request_status.json()['data'][0]['StatusCode']


@api_view(['GET'])
def get_all_warehouse(request):
    return Response([warehouse.title for warehouse in NPWarehouse.objects.all()])


def nowa_poshta(request):
    response = NovaPoshtaApi(api_key='c3027600bfa68b877b52238709481c66').address.get_warehouses()
    pprint(response.json()['data'][0])

    for warehouses in response.json()['data']:
        city_json = warehouses['CityDescriptionRu']
        title_json = warehouses['DescriptionRu']
        name_json = city_json + ", " + title_json
        NPWarehouse.objects.create(title=name_json)

    print('Victory')
