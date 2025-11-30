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

        X = df.drop("label", axis=1)
        y = df["label"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        model_path = os.path.join(settings.BASE_DIR, "model.pkl")
        joblib.dump(model, model_path)

        self.stdout.write(self.style.SUCCESS("Model trained successfully!"))