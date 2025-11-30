from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,"home.html")
 

def sign(request):
    return render(request,"sign.html")

def login(request):
    return render(request,"login.html")


def predict_page(request):
    return render(request,"predict.html")

def attendance(request):
    return render(request,"attendance.html")

def dashboard(request):
    return render(request,"dashboard.html")

def staff(request):
    return render(request,"staff.html")

def staffmanagement(request):
    return render(request,"staffmanagement.html") 

def salary(request):
    return render(request,"salary.html")


# Create your views here.
# staffmgmt/views.py
import os
from django.conf import settings
import json
import joblib
import pandas as pd
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
MODEL_PATH = os.path.join(settings.BASE_DIR, "core", "savedModels", "model.joblib")

@method_decorator(csrf_exempt, name='dispatch')
class PredictUnderstaffed(View):

    def load_model(self):
        try:
            model = joblib.load(MODEL_PATH)
            return model
        except:
            return None

    # Optional GET endpoint
    def get(self, request):
        return JsonResponse({
            "message": "ML API running. Send POST with JSON data to get prediction."
        })

    def post(self, request):
        model = self.load_model()   # <-- uses load_model()
        if model is None:
            return JsonResponse({"error": "Model file missing."}, status=400)

        try:
            data = json.loads(request.body)
        except:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        required = ["scheduled_shifts", "emergencies_count", "patient_count"]
        for key in required:
            if key not in data:
                return JsonResponse({"error": f"Missing '{key}'"}, status=400)

        df = pd.DataFrame([{
            "scheduled_shifts": data["scheduled_shifts"],
            "emergencies_count": data["emergencies_count"],
            "patient_count": data["patient_count"]
        }])

        pred = model.predict(df)[0]

        return JsonResponse({"prediction": int(pred)})
    
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Staff, Attendance

def attendance(request):
    today = timezone.now().date()
    staff_list = Staff.objects.all()

    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        status = request.POST.get("status")

        staff = Staff.objects.get(id=staff_id)

        Attendance.objects.create(
            staff=staff,
            status=status
        )

        return redirect('attendance')

    context = {
        'staff_list': staff_list,
        'today': today,
    }
    return render(request, "attendance.html", context)
