# Green Count – Backend

This is the Flask-based backend for the Green Count app. It handles carbon emissions logging, summaries, food impact calculations, AI-powered tips, and user authentication. It connects to Supabase for data storage and OpenAI for intelligent suggestions.

## 🚀 Features

- 🌍 `/add` – Add general emissions data
- 📥 `/get` – Get all entries from `test_table`
- 📊 `/summarize` – Calculate total/average for a specific metric
- 🔄 `/convert` – Convert between units and estimate emissions
- 🍽️ `/food-impact` – Calculate food emissions based on weight
- 🔐 `/auth/signup` & `/auth/login` – Supabase auth for users
- 🔒 `/add-user-emission` – Add emission data linked to logged-in user
- 📂 `/get-user-emissions` – Get data belonging to the current user only
- 🧠 `/chat` – AI suggestions using OpenAI's GPT-3.5 model
- 🧪 `/test-emission`, `/test-db` – Manual database testing endpoints (optional for dev)
- 🧾 `/model-info` – Placeholder for future machine learning info

## 🛠️ Technologies Used

- **Python 3.12**
- **Flask** – Lightweight Python web framework
- **Supabase-py** – Supabase client for database and auth
- **OpenAI API** – AI assistant for user suggestions
- **Flask-CORS** – Cross-origin request handling for frontend communication
- **dotenv** – Secure `.env` configuration loading
- **GitHub Actions** – Automated CI on every push

## 📂 Project Structure

/backend/  
├── app.py – Main Flask application and routes  
├── requirements.txt – Project dependencies  
├── .env – Environment variables (not committed to Git)

## ⚙️ Setup Instructions

1. Create and activate a virtual environment:

   Run:
```bash
   python -m venv venv
```

   Then activate it:
   - On macOS/Linux:
```bash
     source venv/bin/activate
```
   - On Windows:
     venv\Scripts\activate

2. Install dependencies:
```bash
   pip install -r requirements.txt
```

3. Create a `.env` file with the following values:

   SUPABASE_URL=your_supabase_url  
   SUPABASE_KEY=your_supabase_anon_key  
   SUPABASE_SERVICE_KEY=your_supabase_service_key  
   OPENAI_API_KEY=your_openai_key

4. Run the Flask server:
```bash
   flask run
```

