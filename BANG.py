from Standings import team_df
from CurrentTeams import roster

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

team_df = team_df.sort_values(by=["franchise_id"])
roster = roster.sort_values(by=["franchise_id"])
X = team_df.drop(["franchise_id", "team_name", "Year", "Pts", "PtsO", "W-L%"], axis=1)
y = team_df["W-L%"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)


models = {
    'Lasso Regression': Lasso(),
    'Random Forest! (please work)': RandomForestRegressor(n_estimators=50),
    'XGBoost': XGBRegressor()
}

def evaluate(model, X, y, model_name):
    pca = PCA(n_components = 0.75)
    X_pca = pca.fit_transform(X)
    cv_mae = cross_val_score(model, X_pca, y, cv=5, scoring='neg_mean_absolute_error')
    cv_mse = cross_val_score(model, X_pca, y, cv=5, scoring='neg_mean_squared_error')
    cv_r2 = cross_val_score(model, X_pca, y, cv=5, scoring='r2')

    print(f"{model_name}:")
    print(f"mae: {cv_mae}")
    print(f"mse: {cv_mse}")
    print(f"r2: {cv_r2}\n")


#for name, model in models.items():
#    evaluate(model, X, y, name)

def hyperParam(X, y):
    for i in [0.1, 0.25, 0.4, 0.5, 0.6, 0.75, 0.8, 0.9, 0.95, 0.99]:
        pca = PCA(n_components = i)
        X_pca = pca.fit_transform(X)
        for j in [100, 150, 200, 240]:
            model = RandomForestRegressor(n_estimators=j)
            cv_mae = cross_val_score(model, X_pca, y, cv=5, scoring='neg_mean_absolute_error')
            cv_mse = cross_val_score(model, X_pca, y, cv=5, scoring='neg_mean_squared_error')
            cv_r2 = cross_val_score(model, X_pca, y, cv=5, scoring='r2')

            print(f"Random Forest, pca = {i}, estimators = {j}:")
            print(f"mae: {cv_mae.mean()}")
            print(f"mse: {cv_mse.mean()}")
            print(f"r2: {cv_r2.mean()}\n")

#hyperParam(X, y)

'''
Actually training a random forest model now, let's see what we get
'''


pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=0.8)),
    ('rf', RandomForestRegressor(n_estimators=150, random_state=42))
])

pipeline.fit(X, y)

historical_predictions = pipeline.predict(X)
mae = mean_absolute_error(y, historical_predictions)
mse = mean_squared_error(y, historical_predictions)
r2 = r2_score(y, historical_predictions)

print(f"Model Performance on Historical Data:")
print(f"Mean Absolute Error: {mae:.4f}")
print(f"Mean Squared Error: {mse:.4f}")
print(f"R-squared: {r2:.4f}")

curX = roster[['wr1_grades_offense',
       'wr2_grades_offense', 'wr3_grades_offense', 'qb_grades_pass',
       'qb_grades_run', 'qb_avg_depth_of_target', 'lt_grades_pass_block',
       'lt_grades_run_block', 'lg_grades_pass_block', 'lg_grades_run_block',
       'ce_grades_pass_block', 'ce_grades_run_block', 'rg_grades_pass_block',
       'rg_grades_run_block', 'rt_grades_pass_block', 'rt_grades_run_block',
       'teBlock_grades_pass_block', 'teBlock_grades_run_block',
       'te_targeted_qb_rating', 'rb_grades_run', 'rb_targeted_qb_rating',
       'cb1_grades_coverage_defense', 'cb2_grades_coverage_defense',
       'lb1_grades_defense', 'lb2_grades_defense', 's_grades_defense',
       'de1_grades_defense', 'de2_grades_defense', 'dt_grades_defense', 'W-L%_prev']]

pred = pipeline.predict(curX)



'''
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=0.8)
X_pca = pca.fit_transform(X_scaled)
loadings = pca.components_.T * np.sqrt(pca.explained_variance_)

loadings_df = pd.DataFrame(
    loadings, 
    columns=[f'PC{i+1}' for i in range(pca.n_components_)],
    index=X.columns
)

print("PCA Component Loadings:")
print(loadings_df)

feature_importance = loadings_df.abs().sum(axis=1).sort_values(ascending=False)

print("\nOverall feature importance across all PCs:")
print(feature_importance)


'''





#alright gotta go back to nn!
'''
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

pca = PCA(n_components=0.75)
X_train_pca = pca.fit_transform(X_train_scaled)
X_test_pca = pca.transform(X_test_scaled)


X_train_tensor = torch.FloatTensor(X_train_pca)
y_train_tensor = torch.FloatTensor(y_train.values).reshape(-1, 1)
X_test_tensor = torch.FloatTensor(X_test_pca)
y_test_tensor = torch.FloatTensor(y_test.values).reshape(-1, 1)



print(f"Original number of features: {X_train.shape[1]}")
print(f"Number of features after PCA: {X_train_pca.shape[1]}")


dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader = DataLoader(dataset, batch_size=32, shuffle=True)

class Net(nn.Module):
    def __init__(self, input_size):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(input_size, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x
    
model = Net(input_size=X_train_pca.shape[1])

criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 150
for epoch in range(num_epochs):
    model.train()
    for inputs, targets in train_loader:
        outputs = model(inputs)
        loss = criterion(outputs, targets)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    with torch.no_grad():
        test_outputs = model(X_test_tensor)
        test_loss = criterion(test_outputs, y_test_tensor)
    
    if (epoch + 1) % 10 == 0:
        print(f'Epoch [{epoch+1}/{num_epochs}], Train Loss: {loss.item():.4f}, Test Loss: {test_loss.item():.4f}')


model.eval()
with torch.no_grad():
    y_pred = model(X_test_tensor).numpy()

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("Neural Network (PyTorch):")
print(f"  MAE: {mae:.3f}")
print(f"  RMSE: {rmse:.3f}")
print(f"  R2: {r2:.3f}")
'''