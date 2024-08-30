import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from joblib import dump

# Load the dataset
df = pd.read_csv("cropdata.csv")

# Prepare the dataset
new_df = df.copy()
new_df.drop(columns=['N', 'P', 'K'], axis=1, inplace=True)
X = new_df.drop(['label'], axis=1)
y = new_df['label']

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Initialize the models
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
lr_model = LogisticRegression(solver='liblinear', random_state=42)
dt_model = DecisionTreeClassifier(random_state=42)

# Train the models
rf_model.fit(X_train, y_train)
lr_model.fit(X_train, y_train)
dt_model.fit(X_train, y_train)

# Save the models
dump(rf_model, 'rf_model.joblib')
dump(lr_model, 'lr_model.joblib')
dump(dt_model, 'dt_model.joblib')

print("Models trained and saved successfully.")
