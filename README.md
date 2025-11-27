# 🚗 Car Park Service

A web application for fleet management developed on Django. The system allows users to view cars, register as sellers, and manage listings, while administrators manage the list of manufacturers.

The project features a modern interface with a "Glassmorphism" effect and animations.

## 📋 Features

### 🔹 Cars (Autos)
* **View:** List of cars with pagination and search by model.
* **CRUD:** Create, edit, and delete cars.
* **Access:** Only sellers with an active license can add cars. Only the owner can edit them.
* **Validation:** Checks the validity period of the seller's license before adding a car.

### 🔹 Sellers
* **Registration:** Users can become sellers by providing a license.
* **License:** Strict validation of format (8 characters: 3 letters + 5 digits) and expiration date.
* **Profile:** View seller information.

### 🔹 Manufacturers
* **Management:** Only superusers can add, change, or delete manufacturers.
* **Search:** Search for manufacturers by name.
* **Relation:** View all cars associated with a specific manufacturer.

### 🔹 Interface (UI/UX)
* **Design:** Dark theme, semi-transparent cards (Glassmorphism).
* **Animations:** Parallax background effect, smooth element appearance.
* **Dashboard:** Statistics (number of cars, sellers, manufacturers) and a visit counter.

## 🛠 Technologies

* **Backend:** Python, Django
* **Frontend:** HTML, CSS, JavaScript (Vanilla)
* **Database:** Postgres remote database

## 🔐 Validation Features

* **License:** Must start with 3 uppercase letters and end with 5 digits (e.g., `AAA12345`).
* **Visit Counter:** Uses sessions (`request.session`) to count visits to the main page.
* **Object Modification Ban:** Backend and frontend restrictions prevent modification of objects that do not belong to the user's profile.

**Home Page:**
<img width="1919" height="956" alt="image" src="https://github.com/user-attachments/assets/172df908-34ce-4b97-9cbe-a89474b20bd8" />

**Clone the repository:**
```bash
git clone [https://github.com/BossUA1998/Car_Park](https://github.com/BossUA1998/Car_Park)
cd Car_Park
```
**Створіть віртуальне оточення:**
```bash
python -m venv venv
```

```bash
source venv/bin/activate # macOS/Linux
```

```bash
venv\Scripts\activate # Windows
```

**Встановіть залежності:**
```bash
pip install -r requirements.txt
```

**Запустіть міграції:**
```bash
python manage.py migrate
```

**Створіть суперюзера (для доступу до виробників):**
```bash
python manage.py createsuperuser
```

**Запустіть сервер:**
```bash
python manage.py runserver
```
**Або відвідайте наш сайт**
https://car-park-yb8r.onrender.com
Користувач для входу у файлі user_test.txt
