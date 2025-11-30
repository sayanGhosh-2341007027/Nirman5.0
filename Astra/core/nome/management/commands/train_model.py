from django.core.management.base import BaseCommand
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
from django.conf import settings
import os
class Command(BaseCommand):
    help = 'Train ML model from CSV'

    def handle(self, *args, **kwargs):
        csv_path = os.path.join(settings.BASE_DIR, "understaffing_dataset.csv")

        df = pd.read_csv(csv_path)

        # Correct columns based on your dataset
        X = df[["scheduled_shifts", "emergencies_count", "patient_count"]]  
        y = df["understaffed"]   # <-- target column

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Save model inside core/savedModels/model.joblib
        model_path = os.path.join(settings.BASE_DIR, "core", "savedModels", "model.joblib")
        joblib.dump(model, model_path)

        self.stdout.write(self.style.SUCCESS("Model trained successfully!"))