
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import log_loss

# Load Iris dataset
data = load_iris()
X = data['data']
y = data['target']

# Filter to include only versicolor and virginica classes
vv_filter = (y == 1) | (y == 2)
X_vv = X[vv_filter][:, :2]  # Using only two features: sepal length and sepal width
y_vv = y[vv_filter]

# Split the filtered data into training and testing sets
X_train_vv, X_test_vv, y_train_vv, y_test_vv = train_test_split(X_vv, y_vv, test_size=0.3, random_state=42)

# Initialize the SGDClassifier as logistic regression
sgd_logistic = SGDClassifier(loss='log_loss', learning_rate='constant', eta0=0.01, max_iter=1, tol=None, random_state=42)

# Manual training to track loss over epochs
num_epochs = 50
losses = []

for epoch in range(num_epochs):
    sgd_logistic.partial_fit(X_train_vv, y_train_vv, classes=np.unique(y_train_vv))
    # Calculate probabilities for the log loss calculation
    probabilities = sgd_logistic.predict_proba(X_train_vv)
    # Calculate log loss
    epoch_loss = log_loss(y_train_vv, probabilities)
    losses.append(epoch_loss)
    print(f"Epoch {epoch + 1}, Loss: {epoch_loss:.4f}")
