from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from .models import AutomobileVO, SalesPerson, SaleRecord, Customer
from .encoders import AutomobileVOEncoder, SalesPersonEncoder, CustomerEncoder, SaleRecordListEncoder

@require_http_methods(["GET", "POST"])
def api_sales_person(request):
    if request.method == "GET":
        sales_person = SalesPerson.objects.all()
        return JsonResponse(
            {"sales_person": sales_person},
            encoder=SalesPersonEncoder,
        )
    else:
        content = json.loads(request.body)
        try:
            salesperson = SalesPerson.objects.create(**content)
            return JsonResponse(
                salesperson,
                encoder=SalesPersonEncoder,
                safe=False,
            )
        except:
            response = JsonResponse(
                {"message": "Could not create salesperson"}
            )
            response.status_code = 400
            return response


@require_http_methods(["GET", "POST"])
def api_customer(request):
    if request.method == "GET":
        customer = Customer.objects.all()
        return JsonResponse(
            {"customer": customer},
            encoder=CustomerEncoder,
            safe=False,
        )
    else:
        try:
            content = json.loads(request.body)
            customer = Customer.objects.create(**content)
            return JsonResponse(
                customer,
                encoder=CustomerEncoder,
                safe=False,
            )
        except:
            response = JsonResponse(
                {"message": "Could not create customer"}
            )
            response.status_code = 400
            return response

@require_http_methods(["DELETE"])
def api_customer_delete(request, pk):
    if request.method == "DELETE":
        count, _ = Customer.objects.filter(id=pk).delete()
        return JsonResponse({"message": count > 0})


@require_http_methods(["GET", "POST"])
def api_sale_record_list(request):
    if request.method == "GET":
        sale_record = SaleRecord.objects.all()
        return JsonResponse(
            {"sale_record": sale_record},
            encoder=SaleRecordListEncoder,
            safe=False,
        )
    else:
        try:
            content = json.loads(request.body)
            content = {
                **content,
                "sales_person": SalesPerson.objects.get(pk=content["sales_person"]),
                "automobile": AutomobileVO.objects.get(vin=content["automobile"]),
                "customer": Customer.objects.get(pk=content["customer"]),
            }

            sold_status = content["automobile"].sold
            if sold_status == False:
                content["automobile"].sold = True
                content["automobile"].save()

            sale_record = SaleRecord.objects.create(**content)
            return JsonResponse(
                    {"sale_record": sale_record},
                    encoder=SaleRecordListEncoder,
                    safe=False,
                )
        except:
            response = JsonResponse(
                {"message": "Sales Record cannot be created"}
            )
            response.status_code = 400
            return response

@require_http_methods(["DELETE"])
def api_sale_record_list_delete(request, pk):
    if request.method == "DELETE":
        count, _ = SaleRecord.objects.filter(id=pk).delete()
        return JsonResponse({"message": count > 0})




@require_http_methods(["GET"])
def api_automobile_vo(request):
    if request.method == "GET":
        automobile = AutomobileVO.objects.all()
        return JsonResponse(
            {"automobile": automobile},
            encoder=AutomobileVOEncoder,
            safe=False,
        )
