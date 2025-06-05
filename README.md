# 🧘‍♀️ Fitbook API – Fitness Class Booking System

A simple fitness class booking platform built using **Flask** and **SQLite**, featuring a clean UI, timezone-aware scheduling, input validation, and test coverage. Built as part of the Omnify backend developer assignment.

---

## 📦 Features

- View upcoming fitness classes (Yoga, Zumba, HIIT)
- Book a class via UI or API
- Prevent overbooking
- Retrieve bookings by email
- Timezone-aware class scheduling (created in IST, auto-converted by browser)
- Built-in UI (no Postman required, but supported)
- Basic unit tests

---

## 🚀 Setup Instructions (Step-by-Step)

### 1. Clone the repo or unzip the folder
```bash
git clone https://github.com/your-username/fitbook-api.git
cd fitbook-api
```

### 2. Create a virtual environment

```bash
python -m venv env
```

### 3. Activate the environment

On Windows:
```bash
env\Scripts\activate
```
On macOS/Linux:
```bash
source env/bin/activate
```

### 4. Install the dependencies
```bash
pip install -r requirements.txt
```

### 5. Seed sample fitness class data
```bash
python seed_data.py
```

This will create a new SQLite database file (fitbook.db) and add sample Yoga, Zumba, and HIIT classes in IST timezone.

### 6. Run the Flask application
```bash
python app.py
```

You should see:
 * Running on http://127.0.0.1:5000/

### 7. Visit the app in your browser 
http://localhost:5000


### 8. Sample API Requests (via cURL)
View all upcoming classes
```bash
curl http://localhost:5000/classes
```
Filter classes by specific date (IST)
```bash
curl http://localhost:5000/classes?date=2025-06-07
```
Book a class
```bash
curl -X POST http://localhost:5000/book \
  -H "Content-Type: application/json" \
  -d '{"class_id": 1, "client_name": "Alice", "client_email": "alice@example.com"}'
```
Lookup bookings by email
```bash
curl http://localhost:5000/bookings?email=alice@example.com
```
