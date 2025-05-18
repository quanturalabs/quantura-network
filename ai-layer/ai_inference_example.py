# ai-layer/ai_inference_example.py

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
import numpy as np

def simulate_ai_oracle():
    # Load dataset and train a model (offline)
    iris = load_iris()
    model = DecisionTreeClassifier()
    model.fit(iris.data, iris.target)

    # Simulate on-chain verification of a prediction
    test_input = np.array([[5.1, 3.5, 1.4, 0.2]])  # Example flower features
    prediction = model.predict(test_input)

    print("🌸 Predicted Iris Class:", prediction[0])
    print("🧠 (In real Quantura, this output would be hashed and verifiable on-chain)")

if __name__ == "__main__":
    simulate_ai_oracle()
