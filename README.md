# FinGuard AI

FinGuard AI is a Flask-based financial fraud detection web application that combines an ensemble of machine learning models, SHAP-based explainability, and an LLM-style contextual explanation layer for transaction analysis.

The project includes:

- a **user portal** for submitting transactions
- an **admin dashboard** for viewing fraud trends and feature importance
- an **ensemble inference pipeline** using multiple pretrained models
- **SHAP explanations** for model transparency
- a **Gemini-backed or fallback explanation layer** for natural-language summaries

## Features

- Real-time fraud scoring for submitted transactions
- Ensemble model consensus across multiple architectures
- SHAP-based feature importance for interpretability
- Session-based admin analytics dashboard
- Model-wise fraud probability breakdown
- Natural-language transaction explanation
- Auto-calculated sender and receiver balances in the UI

## Project Architecture

### Main flow

1. A user submits transaction details from the web interface.
2. The Flask backend receives the transaction through `/api/transaction`.
3. The transaction is converted into core numerical features.
4. The ML ensemble computes fraud probabilities.
5. SHAP is used to identify the most important features.
6. A contextual explanation is generated using Gemini if configured, otherwise a local fallback is used.
7. The result is returned to the user interface and stored in memory for the admin dashboard.

### Core components

- [`app.py`](./app.py): Flask routes, session handling, API endpoints, admin aggregation
- [`utils/ml_stub.py`](./utils/ml_stub.py): model loading, ensemble prediction, SHAP explainability
- [`utils/llm_stub.py`](./utils/llm_stub.py): Gemini integration and fallback explanation logic
- [`templates/`](./templates): user, admin, and login HTML templates
- [`static/`](./static): CSS, JavaScript, and UI assets
- [`models/`](./models): pretrained model artifacts and notebook assets

## Models Used

The runtime ensemble currently loads these model families:

- **TCN**
- **TCN + BiLSTM + Multihead Attention**
- **CNN + BiLSTM**
- **LSTM + RF Hybrid**

The inference pipeline is built around 5 core numerical transaction features:

- `amount`
- `oldbalanceOrg`
- `newbalanceOrig`
- `oldbalanceDest`
- `newbalanceDest`

Some models use engineered features and sequence reshaping internally.

## Tech Stack

### Backend

- Flask
- Python

### Machine Learning

- TensorFlow / Keras
- PyTorch
- Scikit-learn
- NumPy
- SHAP
- Joblib

### Frontend

- HTML
- CSS
- JavaScript
- Chart.js

### LLM / Utilities

- Google Gemini (`google-generativeai`)
- `python-dotenv`

## Installation

It is recommended to run this project in a clean **Python 3.11** environment.

### 1. Create and activate an environment

Using Conda:

```powershell
conda create -n finguard python=3.11 -y
conda activate finguard
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
pip install google-generativeai
```

If you hit TensorFlow / protobuf issues, install a compatible protobuf version:

```powershell
pip install protobuf==6.31.1
```

### 3. Optional: configure Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

If this key is not provided, the app still runs and falls back to a local mock explanation.

## Running the App

Start the Flask server:

```powershell
python app.py
```

Open the app in your browser:

- User portal: `http://127.0.0.1:5000/`
- Admin login: `http://127.0.0.1:5000/login`

### Default admin credentials

- Username: `admin`
- Password: `admin`

## Test Scripts

The repository includes a few helper scripts for verification:

- [`test_loader_only.py`](./test_loader_only.py): checks model loading and a single forward pass
- [`verify_app.py`](./verify_app.py): runs a dummy transaction through prediction and explanation
- [`test_4_models.py`](./test_4_models.py): prints a sample prediction payload
- [`debug_loader.py`](./debug_loader.py): older loader debugging script

Run them with:

```powershell
python test_loader_only.py
python verify_app.py
python test_4_models.py
```

## Project Structure

```text
FinGuardAI/
├── app.py
├── requirements.txt
├── README.md
├── verify_app.py
├── test_4_models.py
├── test_loader_only.py
├── debug_loader.py
├── models/
├── static/
├── templates/
└── utils/
```

## Notes and Current Limitations

- Transactions are stored in an **in-memory list**, so admin analytics reset when the app restarts.
- Admin authentication is currently **hard-coded** for demonstration.
- Some benchmark numbers shown in the admin UI are static presentation values.
- SHAP must be installed correctly for explainability to work.
- TensorFlow may print oneDNN / CPU optimization logs on startup; these are informational.

## Troubleshooting

### `ModuleNotFoundError: No module named 'google.generativeai'`

Install the Gemini package:

```powershell
pip install google-generativeai
```

### TensorFlow protobuf version error

Install a compatible protobuf version:

```powershell
pip install protobuf==6.31.1
```

### SHAP not installed

Install SHAP:

```powershell
pip install shap
```

### TensorFlow startup warnings

These messages are often informational. To reduce startup noise:

```powershell
$env:TF_CPP_MIN_LOG_LEVEL="3"
$env:TF_ENABLE_ONEDNN_OPTS="0"
python app.py
```

## Future Improvements

- Persistent database storage for transactions
- Secure admin authentication
- Live-computed dashboard metrics
- Better model/version management
- More robust deployment configuration
- Faster or cached SHAP generation

## License

No license file is currently included in the repository.
