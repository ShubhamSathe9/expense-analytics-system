# 💸 Expense Analytics System  
A clean, modern and fast personal finance tracker that helps you manage expenses, set budgets, track goals, handle recurring payments, and view smart spending insights — all inside a beautiful dashboard.

<p align="center">
  <img src="https://img.shields.io/badge/BUILT%20WITH-DJANGO-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/UI-TAILWINDCSS-38bdf8?style=for-the-badge" />
  <img src="https://img.shields.io/badge/STATUS-ACTIVE-success?style=for-the-badge" />
</p>

---

## 🚀 Overview  
Expense Analytics System helps users easily track their daily expenses and understand where their money goes.  
This app focuses on **simplicity, clarity and actual finance tracking features** — no unnecessary complexity.

---

## ✨ Core Features (ONLY REAL FEATURES INCLUDED)

### 📊 **Dashboard Stats**
- Today’s total spent  
- Weekly total  
- Monthly total  
- Yearly total  
- Category-wise chart  
- Smooth, responsive card layout  
- Smart insights panel  

---

### 🧾 **Expense Management**
- Add new expenses  
- Edit expenses  
- Delete expenses  
- Category selection  
- Date selection  
- Clean table + mobile layout  

---

### 🗂️ **Category Management**
- Predefined categories  
- Add your own categories  
- Color/icon supported (UI ready)  

---

### 🔁 **Recurring Expenses**
- Add recurring bills (monthly/yearly)  
- Next due date tracking  
- Simple list UI  
- Auto reminders inside notifications  

---

### 💰 **Budgets**
- Create monthly budgets per category  
- Budget progress bar  
- Alert when spending is near/exceeded  
- Dashboard budget highlight  

---

### 🎯 **Goals**
- Add savings goals  
- Track progress visually  
- Goal progress bar  
- Mark complete  
- Shown neatly in dashboard  

---

### 🔔 **Notifications**
- Low budget alerts  
- Recurring due reminders  
- Goal updates  
- Dismiss/read notifications  

---

### 🧑‍💼 **User Profile**
- Dark / Light mode toggle  
- Mobile-first responsive design  
- Clean layout  

---

## 🛠️ Tech Stack

| Part | Technology |
|------|------------|
| Backend | Django (Python) |
| Frontend | TailwindCSS |
| Charts | Chart.js |
| Database | SQLite |
| Auth | Django Authentication |

---

## 📦 Installation

### 1️⃣ Clone the project
```bash
git clone https://github.com/ShubhamSathe9/ea.git
cd ea
```

### 2️⃣ Setup virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3️⃣ Install project requirements
```bash
pip install -r requirements.txt
```

### 4️⃣ Add `.env` file
```
SECRET_KEY=your-secret-key
DEBUG=True
```

### 5️⃣ Run migrations
```bash
python manage.py migrate
```

### 6️⃣ Start server
```bash
python manage.py runserver
```

---

## 📂 Project Structure
```
ea/
│── expenses/
│   ├── templates/expenses/
│   ├── static/expenses/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
│── ea/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
│── manage.py
│── requirements.txt
│── db.sqlite3
```

---

## ⭐ Support  
If you like this project, consider giving it a ⭐ on GitHub!
