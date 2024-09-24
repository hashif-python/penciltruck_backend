import re
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from penciltruckapp.serializers import GallerySerializer,VolunteerRequestSerializer
from penciltruckadmin.models import Banner, Gallery,VolunteerRequest,OtpInfo
from rest_framework import status
from django.conf import settings
import random
from django.core.mail import send_mail
import requests
from .models import StudyMaterialDonation
from .serializers import StudyMaterialDonationSerializer

class GalleryData(APIView):
    
    def get(self, request):
        try:
            obj=Gallery.objects.filter(active=True)
            serializer = GallerySerializer(obj, many=True)
            res = serializer.data
            return Response({'data': res}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
class VerifyOtpView(APIView):

    def generate_otp(self):
        """Helper function to generate a random 6-digit OTP"""
        return random.randint(1000, 9999)

    def send_otp_email(self, email, otp):
        """Send an email with the OTP"""
        subject = 'Your Email Verification OTP'
        message = f'Your OTP is {otp}.'
        html_message = f'''
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center;">
                <h2 style="color: #333;">Verify your Email</h2>
                <p>Your OTP is <strong style="font-size: 24px;">{otp}</strong></p>
                <p>Please enter this code to verify your email. The OTP is valid for 5 minutes.</p>
                <br>
                <p>Thank you,</p>
                <p>Pencil Truck Team</p>
            </body>
            </html>
        '''
        from_email = settings.DEFAULT_FROM_EMAIL
        
        otp_info, created = OtpInfo.objects.get_or_create(email=email)
        otp_info.email_otp = otp
        otp_info.save()
        
        send_mail(subject, message, from_email, [email], html_message=html_message)
        
    def send_otp_sms(self, phone,email):
        url = "https://cpaas.messagecentral.com/verification/v3/send?countryCode=91&customerId=C-39945CBCFC264D1&flowType=SMS&mobileNumber="+str(phone)

        payload = {}
        headers = {
        'authToken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJDLTM5OTQ1Q0JDRkMyNjREMSIsImlhdCI6MTcyNzA4Mjg1MSwiZXhwIjoxODg0NzYyODUxfQ.3bID8eHIpsHFaHMgVvGhDjfqgTQcHWIfq-5okIP2dbSeR3LlAByozNYr6Ah0-QuVUz-LKk-yasGkEPdOGdMRXA'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        data = response.json()
        otp_info, created = OtpInfo.objects.get_or_create(email=email)
        otp_info.phone = phone
        otp_info.phone_otp = data['data']['verificationId']
        otp_info.save()
        


    def post(self, request):
        try:
            email = request.data.get('email')
            mobile = request.data.get('phone')

            if not email:
                return Response({'message': 'Email is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not mobile:
                return Response({'message': 'Phone number is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Check if email exists in the database
            existing_email_request = VolunteerRequest.objects.filter(email=email).first()

            if existing_email_request and existing_email_request.status == "Pending":
                return Response({'message': 'A request with this email is already pending. Please wait until the admin accepts.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            if existing_email_request and existing_email_request.status == "Rejected":
                days_since_rejection = (timezone.now() - existing_email_request.created_at).days
                if days_since_rejection < 30:
                    remaining_days = 30 - days_since_rejection
                    return Response({'message': f'Your request with this email was rejected. Please try again in {remaining_days} days.'},
                                    status=status.HTTP_400_BAD_REQUEST)

            # Check if mobile exists in the database
            existing_mobile_request = VolunteerRequest.objects.filter(phone=mobile).first()

            if existing_mobile_request and existing_mobile_request.status == "Pending":
                return Response({'message': 'A request with this phone number is already pending. Please wait until the admin accepts.'}, 
                                status=status.HTTP_400_BAD_REQUEST)

            if existing_mobile_request and existing_mobile_request.status == "Rejected":
                days_since_rejection = (timezone.now() - existing_mobile_request.created_at).days
                if days_since_rejection < 30:
                    remaining_days = 30 - days_since_rejection
                    return Response({'message': f'Your request with this phone number was rejected. Please try again in {remaining_days} days.'},
                                    status=status.HTTP_400_BAD_REQUEST)

            # If neither email nor phone number has an active or recent rejected request, generate OTP
            otp = self.generate_otp()

            # Send OTP email
            self.send_otp_email(email, otp)
            self.send_otp_sms(mobile, email)

            return Response({'message': 'OTP sent to your email and phone.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class VolunteerRequestCreate(APIView):
    
    
    def verify_otp(self, email, phone, email_otp, phone_otp):
        """Helper function to verify email and phone OTP"""
        # Check email OTP
        otp_record = OtpInfo.objects.filter(email=email).first()
        if not otp_record:
            return False, 'Invalid email OTP'
        
        if int(otp_record.email_otp) != int(email_otp):
            return False, 'Incorrect email OTP'


        # Check phone OTP
        phone_otp_record = OtpInfo.objects.filter(phone=phone).first()
        if not phone_otp_record:
            return False, 'Invalid phone OTP'
        
        url = "https://cpaas.messagecentral.com/verification/v3/validateOtp?countryCode=91&mobileNumber="+ str(phone) + "&verificationId=" +str(phone_otp_record.phone_otp)+"&customerId=C-39945CBCFC264D1&code="+str(phone_otp)    

        print(url)
        payload = {}
        headers = {
        'authToken': 'eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJDLTM5OTQ1Q0JDRkMyNjREMSIsImlhdCI6MTcyNzA4Mjg1MSwiZXhwIjoxODg0NzYyODUxfQ.3bID8eHIpsHFaHMgVvGhDjfqgTQcHWIfq-5okIP2dbSeR3LlAByozNYr6Ah0-QuVUz-LKk-yasGkEPdOGdMRXA'
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        
        data=response.json()

        print(data)
        if data['responseCode'] != 200:
            return False, 'Incorrect phone OTP'

        # Check if the phone OTP has expired (5 minutes validity)
        

        return True, 'OTP verified'
    
    def post(self, request):
        try:
            email = request.data.get('email')
            phone = request.data.get('phone')
            email_otp = request.data.get('emailOtp')
            phone_otp = request.data.get('mobileOtp')
            print(email,phone,email_otp,phone_otp)
            # Check if the same email or phone exists in the databas
                    
                    
            otp_verified, message = self.verify_otp(email, phone, email_otp, phone_otp)
            if not otp_verified:
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

            # If no "Pending" or recent "Rejected" request exists, proceed to create a new request
            serializer = VolunteerRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()  # Status will be automatically set to 'Pending'
                return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
            
            # If invalid, return detailed errors
            print(serializer.errors)  # Debugging: print errors in the console
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
# penciltruckapp/views.py



class StudyMaterialDonationListCreate(APIView):
    """
    View to list all study material donations and allow creating a new donation
    """
    
    def get(self, request):
        donations = StudyMaterialDonation.objects.all()
        serializer = StudyMaterialDonationSerializer(donations, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = StudyMaterialDonationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

