import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Create plots directory if it doesn't exist
if not os.path.exists('plots'):
    os.makedirs('plots')

# Load the dataset
df = pd.read_csv('data/telco_churn.csv')

# Basic info
print("Dataset Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())

print("\nColumn Types and Missing Values:")
print(df.info())

# TotalCharges is object, need to convert to numeric
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
print("\nMissing values after converting TotalCharges:", df.isnull().sum())

# Drop rows with null TotalCharges (only a few usually)
df.dropna(inplace=True)

# Target Variable Distribution
plt.figure(figsize=(8, 6))
sns.countplot(x='Churn', data=df, palette='viridis')
plt.title('Churn Distribution')
plt.savefig('plots/churn_distribution.png')
plt.close()

# Numerical Features Analysis
num_features = ['tenure', 'MonthlyCharges', 'TotalCharges']
plt.figure(figsize=(15, 5))
for i, col in enumerate(num_features):
    plt.subplot(1, 3, i+1)
    sns.histplot(df[col], kde=True, color='blue')
    plt.title(f'Distribution of {col}')
plt.tight_layout()
plt.savefig('plots/numerical_distribution.png')
plt.close()

# Categorical Features Analysis (Top components)
cat_features = ['gender', 'SeniorCitizen', 'Partner', 'Dependents', 'Contract', 'PaymentMethod']
plt.figure(figsize=(20, 10))
for i, col in enumerate(cat_features):
    plt.subplot(2, 3, i+1)
    sns.countplot(x=col, hue='Churn', data=df, palette='magma')
    plt.title(f'Churn by {col}')
    plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plots/categorical_analysis.png')
plt.close()

print("\nEDA completed. Plots saved in 'plots/' directory.")
