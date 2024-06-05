# Foreign University Admission Prediction

## Project Overview

This project aims to predict the admission chances of students applying to foreign universities using various machine learning models. The models include Decision Trees, Linear Regression, and Gradient Boosting. The project leverages Google Vertex AI for training and deployment, ensuring high scalability and performance.

## Table of Contents

1. [Introduction](#introduction)
2. [Data Description](#data-description)
3. [Modeling](#modeling)
4. [Google Vertex AI Integration](#google-vertex-ai-integration)
5. [Results](#results)
6. [Usage](#usage)
7. [Contributing](#contributing)
8. [License](#license)

## Introduction

The objective of this project is to develop a predictive model that can accurately determine the likelihood of a student's admission to a foreign university based on their profile. The models are trained and deployed using Google Vertex AI, taking advantage of its robust infrastructure and machine learning capabilities.


## Data Description

The dataset contains various features relevant to a student's application, including:

- GRE Score
- TOEFL Score
- University Rating
- Statement of Purpose (SOP) Strength
- Letter of Recommendation (LOR) Strength
- Undergraduate GPA
- Research Experience (Yes/No)
- Admission Probability

The data is divided into training and testing sets for model evaluation.

## Modeling

The project employs the following machine learning models:

1. **Decision Tree:** A tree-based model that splits the data based on feature values to predict the outcome.
2. **Linear Regression:** A linear approach to modeling the relationship between the dependent and independent variables.
3. **Gradient Boosting:** An ensemble technique that builds multiple models sequentially, each correcting the errors of its predecessor.

## Google Vertex AI Integration

### Steps to Integrate with Vertex AI

1. **Setup Google Cloud Project:**
   - Enable Vertex AI API.
   - Set up a service account with the required permissions.

2. **Data Upload:**
   - Upload the dataset to Google Cloud Storage (GCS).

3. **Training:**
   - Train models using Vertex AI's custom training service.
   - Scripts and notebooks for training are available in the `notebooks/` and `scripts/` directories.

4. **Deployment:**
   - Deploy the trained model to Vertex AI for online predictions.
   - Use the provided `deploy_model.py` script for deployment.

## Results

The results are evaluated based on accuracy, precision, recall, and F1-score. Gradient Boosting emerged as the best-performing model with the highest accuracy.

## Usage

### Prerequisites

- Python 3.7+
- Google Cloud SDK
- Required Python packages (listed in `requirements.txt`)

### Steps to Run

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/foreign-university-admission-prediction.git
   cd foreign-university-admission-prediction
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Cloud:**
   - Set up your Google Cloud project and authentication as described in the Vertex AI documentation.

4. **Preprocess Data:**

   ```bash
   python scripts/data_preprocessing.py
   ```

5. **Train Model:**

   ```bash
   python scripts/train_model.py
   ```

6. **Deploy Model:**

   ```bash
   python scripts/deploy_model.py
   ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

By following this README, you should be able to understand, run, and extend the Foreign University Admission Prediction project using Google Vertex AI. If you have any questions or need further assistance, feel free to reach out.
