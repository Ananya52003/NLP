import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# **1. Load Dataset**
df = pd.read_csv("cleaned_healthcare_dataset.csv")

# **2. Data Preprocessing**
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Handle missing values correctly
df = df.ffill()  # Forward fill (alternative to deprecated method)

# **Check for Non-Numeric Data**
print("🛠 Checking data types before encoding:")
print(df.dtypes)

# **Find columns with string values**
non_numeric_columns = df.select_dtypes(include=['object']).columns.tolist()
print(f"🔍 Non-numeric columns before encoding: {non_numeric_columns}")

# **Encode categorical columns safely**
encoder = LabelEncoder()
for col in non_numeric_columns:
    df[col] = encoder.fit_transform(df[col].astype(str))  # Convert all strings to numbers

# **Check if encoding was successful**
print("✅ Encoding complete. Checking data types after encoding:")
print(df.dtypes)

# **3. Feature Selection**
drop_columns = ['test_results', 'date_of_admission', 'discharge_date', 'room_number']
X = df.drop(columns=[col for col in drop_columns if col in df.columns])  # Drop only existing columns
y = df["test_results"]

# **4. Train/Test Split**
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# **5. Data Normalization (Fixing the Error)**
scaler = StandardScaler()

# Ensure all data is numeric before scaling
print("🛠 Checking X_train types before scaling:")
print(X_train.dtypes)

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# **6. Train Model**
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# **7. Evaluate Model**
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"✅ Model Accuracy: {accuracy:.2f}")

# **8. Save the Trained Model**
joblib.dump(model, "healthcare_model.pkl")  
joblib.dump(scaler, "scaler.pkl")  

print("✅ Model training complete. File saved as 'healthcare_model.pkl'")