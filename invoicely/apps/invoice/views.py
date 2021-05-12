from django.shortcuts import render
import pdfkit
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from rest_framework import viewsets, status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .serializers import InvoiceSerializer, ItemSerializer
from .models import Invoice, Item

from apps.team.models import Team


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        team = self.request.user.teams.first()
        team.first_invoice_number += 1
        team.save()

        serializer.save(created_by=self.request.user, team=team, modified_by=self.request.user,
                        invoice_number=(team.first_invoice_number - 1), bankaccount=team.bankaccount)

    def perform_update(self, serializer):

        obj = self.get_object()

        if self.request.user != obj.created_by:
            raise PermissionDenied('Wrong object owner')

        serializer.save()


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get_queryset(self):
        invoice_id = self.request.GET.get('invoice_id', 0)

        return self.queryset.filter(invoice__id=invoice_id)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()

    template_name = 'pdf_1.html'
    if invoice.is_credited:
        template_name = 'pdf_creditnote.html'
    template = get_template(template_name)
    html = template.render({'invoice': invoice, 'team': team})
    pdf = pdfkit.from_string(html, False, options={})

    response = HttpResponse(pdf, content_type='aplication/pdf')
    response['Content-Dispositions'] = 'attachment; filename="invoice.pdf"'

    return response


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def send_reminder(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id, created_by=request.user)
    team = Team.objects.filter(created_by=request.user).first()

    subject = 'Unpaid invoice'
    from_email = team.email
    to = [invoice.client.email]
    text_content = 'You have unpaid invoice. Invoice number: #' + str(invoice.invoice_number)
    html_content = 'You have unpaid invoice. Invoice number: #' + str(invoice.invoice_number)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    template = get_template('pdf_1.html')
    html = template.render({'invoice': invoice, 'team': team})
    pdf = pdfkit.from_string(html, False, options={})

    if pdf:
        name = f'invoice_{invoice.invoice_number}.pdf'
        msg.attach(name, pdf, 'application/pdf')

    msg.send()

    return Response()

