*OpenPII-Anonymizer

The **PII Anonymization API** is a RESTful service designed to detect, resolve, and anonymize personally identifiable information (PII) in text. The system leverages **Large Language Models (LLMs)** to provide accurate and context-aware anonymization, including features like:

- **PII Detection**: Identifies sensitive entities like names, locations, and organizations.
- **Anaphora/Coreference Resolution**: Ensures consistent placeholders for references like pronouns or repeated entities.
- **Public-Interest vs. PII Differentiation**: Redacts sensitive PII while retaining and tagging public-interest information.

### **Current State**
- **LLM Integration**: The project currently uses **commercial LLMs** (Azure OpenAI Service) for its capabilities. 
- **Future Plans**: Transition to fine-tuned **open-source LLMs** for greater flexibility and reduced dependency on external APIs.
- **Data Logging**: Inputs and outputs are logged to a database for future fine-tuning of open-source models, ensuring ethical and secure handling of sensitive data.

---

## **Getting Started**

### **Prerequisites**
1. **Python**: Install Python 3.8 or later.
2. **Environment Variables**: Ensure the following keys are available:
   - `AZURE_API_KEY`: Azure OpenAI API key.
   - `AZURE_ENDPOINT`: Azure OpenAI endpoint URL.
   - `AZURE_ENGINE`: Azure deployment name (e.g., `gpt-4o-2`).
   - `AZURE_API_VERSION`: API version (e.g., `2024-08-01-preview`).
   - `DATABASE_URL`: Database connection string (default: `sqlite:///./local.db`).

### **Installation**
Clone the repository and install dependencies:

```bash
git clone https://github.com/iurshina/openpii-anonymizer.git
cd openpii-anonymizer
pip install -r requirements.txt
```

### **Configuration**
1. Create a `.env` file in the project root:
   ```plaintext
   DATABASE_URL=sqlite:///./local.db
   AZURE_API_KEY=your-azure-api-key
   AZURE_ENDPOINT=https://your-azure-resource-name.openai.azure.com/
   AZURE_ENGINE=gpt-4o-2
   AZURE_API_VERSION=2024-08-01-preview
   ```
2. Customize settings in `utils/config.py` as needed.

---

## **Running the Project**

### **Start the Server**
Use `uvicorn` to run the API locally:
```bash
uvicorn anonymizer.main:app --reload
```
The API will be available at `http://127.0.0.1:8000`.

### **Access the API**
- **Root Endpoint**: Visit `http://127.0.0.1:8000/` to check if the API is running.
- **API Documentation**: Interactive API docs are available at `http://127.0.0.1:8000/docs`.

---

## **Testing**

### **Run Unit Tests**
The project includes tests for endpoints and core functionalities. Use `unittest` to run the test suite:

```bash
python -m unittest discover -s tests
```
---

## **Features**

### **Endpoints**
#### **1. `/api/v1/anonymize` (POST)
- **Input**:
  ```json
  {
      "input_text": "John lives in New York. The library on Main Street is open to the public.",
      "pii_types": ["person", "location"]
  }
  ```
- **Response**:
  ```json
  {
      "anonymized_text": "<Person 1> lives in <Location 1>. <PUBLIC>The library on Main Street is open to the public.</PUBLIC>",
      "redacted_pii": ["John", "New York"]
  }
  ```

---

## **Future Roadmap**

1. **Transition to Open-Source LLMs**:
   - Replace commercial LLMs (e.g., Azure OpenAI) with fine-tuned open-source models like **LLaMA** for greater control and cost efficiency.
   - Utilize logged data to fine-tune these models for PII anonymization tasks.

2. **Advanced Features**:
    - Expand the PII detection schema to include additional entity types (e.g., financial data, medical terms).
    - Introduce user-defined rules for anonymization.
    - Explore rephrasing capabilities to reduce more subtle forms of PII.

3. **TODOs**:
    - Set up extended evaluation.
    - Improve prompt engineering.
    - Refine logging.
    - Prepare the system for scalability.