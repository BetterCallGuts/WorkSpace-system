from django.shortcuts             import render,redirect
from django.http                  import HttpRequest, JsonResponse, HttpResponse
# from .models                      import Token
# from rest_framework               import status
# from rest_framework.decorators    import api_view
# from rest_framework.response      import Response
# from .serializer                  import PeapleSerializer, TicketSerializer, RecpSerializer, Peaple, Ticket, Recp
# import json
# @api_view(["GET"])
# def get_resp_data(req:HttpRequest, format=None):
#   token = req.GET.get("token", None)
#   if token is not None:
#     tokens= Token.objects.all()
#     for i in tokens :
#       # print(type(i), type( i.token))
#       if str(token) == str(i.token):
    
#         row_recp_data = Recp.objects.all()
#         ser_recp_data = RecpSerializer(row_recp_data, many=True)
        
#         return Response(ser_recp_data.data, status=status.HTTP_200_OK)
    
#     return Response({"status": "error", "message" : "Wrong token"}, status=status.HTTP_400_BAD_REQUEST)
#   return Response({"status": "error", "message" : "No token"}, status=status.HTTP_406_NOT_ACCEPTABLE)

# @api_view(["GET"])
# def get_all_data(req:HttpRequest, format=None):
#   token = req.GET.get("token", None)
#   if token is not None:
#     tokens= Token.objects.all()
#     for i in tokens :
#       # print(type(i), type( i.token))
#       if str(token) == str(i.token):
    
#         row_recp_data = Recp.objects.all()
#         row_pple_data = Peaple.objects.all()
#         row_tick_data = Ticket.objects.all()
#         # 
#         ser_recp_data = RecpSerializer(row_recp_data, many=True)
#         ser_pple_data = PeapleSerializer(row_pple_data, many=True)
#         ser_tick_data = TicketSerializer(row_tick_data, many=True)
#         qr = {
#           "recp"  : ser_recp_data.data,
#           "pple"  : ser_pple_data.data,
#           "ticket": ser_tick_data.data
#         }
        
#         return Response(qr, status=status.HTTP_200_OK)
    
#     return Response({"status": "error", "message" : "Wrong token"}, status=status.HTTP_400_BAD_REQUEST)
#   return Response({"status": "error", "message" : "No token"}, status=status.HTTP_406_NOT_ACCEPTABLE)


# @api_view(["GET"])
# def add_resp_data(req:HttpRequest, format=None):
#   token = req.GET.get("token", None)
#   if token is not None:
#     tokens= Token.objects.all()
#     for i in tokens :
#       # print(type(i), type( i.token))
#       if str(token) == str(i.token):
    
#         data = req.GET.get("data", None)
#         # print(data, type(data))
        
#         if data is not None:
#           data = json.loads(data)
#           # print(data, type(data))
          

#           if True:
            
#             return Response({"status": "success", "message" : "Successfuly added to recp data"},status=status.HTTP_201_CREATED)
#           return Response({"status": "error", "message" : "Invalid Data"}, status=status.HTTP_400_BAD_REQUEST)


          
          
#         return Response({"status": "error", "message" : "Invalid parametars"}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
#     return Response({"status": "error", "message" : "Wrong token"}, status=status.HTTP_400_BAD_REQUEST)
#   return Response({"status": "error", "message" : "No token"}, status=status.HTTP_406_NOT_ACCEPTABLE)




# def handler(req:HttpRequest, exception):
#   # print("im in ")
  
#   return render(req, "404.html", status=404)



def redirectadmin(req:HttpRequest):
  
  
  return redirect("/Caffe/")