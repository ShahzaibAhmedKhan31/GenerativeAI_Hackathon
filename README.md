# GenerativeAI_Hackathon

## Server Setup Instructions:

1. **Create a Python virtual environment** using the following command:
    ```bash
    python -m venv myenv
    ```

2. **Activate the environment** using the following command:
    - For **Linux**:
      ```bash
      source myenv/bin/activate
      ```
    - For **Windows**:
      ```bash
      .\myenv\Scripts\activate
      ```

3. **Install dependencies** using the following command:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run FastAPI server** using the following command:
    ```bash
    uvicorn app:app --port 8000 --host '0.0.0.0' --reload
    ```

5. **Access the BikeBuddy app** by browsing the following link:
    ```text
    http://localhost:8000
    ```

### Important:
- Make sure to update the `OPENAI_API_KEY` and `GROQ_API_KEY` in the `.env` file.
