# Supply Chain Management

A Django-based web application designed to streamline and manage supply chain operations, including product management, supplier coordination, and order tracking.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Technologies and Libraries Used](#technologies-and-libraries-used)
- [Installation](#installation)
- [Usage](#usage)
- [Kafka Integration](#kafka-integration)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Product Management** – Add, update, and delete products with detailed information.
- **Supplier Coordination** – Manage supplier details and associate them with products.
- **Order Tracking** – Monitor orders, their statuses, and related logistics.
- **User Authentication** – Secure login and registration system for users.
- **Kafka Integration** – Real-time processing of supply chain events using Apache Kafka.

---

## Architecture

```
SupplyChainManagement/
├── management/           # Django app for core functionalities
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── supplyChain/          # Project settings and configurations
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/            # Global templates
├── manage.py             # Django's command-line utility
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

---

## Technologies and Libraries Used

### 💻 Backend

- **Django**: High-level Python web framework for rapid development and clean design.
- **Django REST Framework (DRF)**: Powerful toolkit for building Web APIs.
- **PostgreSQL**: Robust and scalable relational database.
- **psycopg2**: PostgreSQL adapter for Python/Django.

### 🔌 Messaging and Streaming

- **Apache Kafka**: Distributed event streaming platform.
- **Zookeeper**: Kafka’s coordination service.
- **kafka-python**: Kafka client for Python used to consume/produce messages.

### ⚙️ Dev Tools

- **pip**: Python package manager.
- **venv**: For isolated Python environments.
- **Logging**: Used to track Kafka events and system behavior.
- **Django Admin**: Auto-generated admin interface for data management.

---

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL (13+)
- Apache Kafka + Zookeeper

### PostgreSQL Setup

```bash
# Access PostgreSQL
sudo -u postgres psql

# Run the following SQL:
CREATE DATABASE scm_db;
CREATE USER scm_user WITH PASSWORD 'yourpassword';
ALTER ROLE scm_user SET client_encoding TO 'utf8';
ALTER ROLE scm_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE scm_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE scm_db TO scm_user;
\q
```

Update `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'scm_db',
        'USER': 'scm_user',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

### App Setup

```bash
# Clone repository
git clone https://github.com/VladAVG07/SupplyChainManagement.git
cd SupplyChainManagement

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## Usage

- **Admin Panel**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Products, Suppliers, Orders**: Manage via admin interface or frontend templates.
- **User Auth**: Register, login, and access role-specific dashboards.

---

## Kafka Integration

Apache Kafka is used for processing supply chain events in real-time (e.g., order status changes, stock updates).

### Start Kafka and Zookeeper

```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka broker
bin/kafka-server-start.sh config/server.properties
```

### Start Kafka Consumer

```bash
python manage.py start_kafka_consumer
```

This command listens to specified Kafka topics and processes relevant events.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/YourFeature`
3. Commit changes: `git commit -m 'Add YourFeature'`
4. Push: `git push origin feature/YourFeature`
5. Submit a pull request

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---


---

## Geolocation Services

The application integrates geolocation capabilities to enhance supply chain visibility. It leverages IP-based and coordinate-based geolocation to:

- Track suppliers and warehouses on an interactive map.
- Visualize shipment movements and order delivery paths.
- Help users assign products or orders to geographical zones.

### Features

- Geolocation lookups for users, suppliers, or any addressable object.
- Automatic map rendering on detail pages using Leaflet.
- Marker clustering for better performance and usability when multiple items are close geographically.

---

## Leaflet Map Integration

The application utilizes **Leaflet.js**, an open-source JavaScript library for mobile-friendly interactive maps. This feature enables real-time and historical views of the supply chain network.

### Functionality

- Display products, suppliers, or orders on a map with markers.
- Popups with relevant info (e.g., product name, supplier name, order status).
- Interactive zoom and pan features.
- Responsive layout compatible with desktop and mobile.

### Example Integration (in templates)

```html
<div id="map" style="height: 500px;"></div>
<script>
  var map = L.map('map').setView([51.505, -0.09], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
  }).addTo(map);

  // Example marker
  L.marker([51.5, -0.09]).addTo(map)
      .bindPopup('Supplier A<br>London')
      .openPopup();
</script>
```

Make sure you include Leaflet’s CSS and JS in your templates:

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
```

---

## Map Use Cases

- **Warehouse Management**: View all warehouse locations and their stock levels.
- **Order Fulfillment**: Track where orders are being dispatched from and where they’re going.
- **Supplier Analysis**: Visually compare supplier density and geographic coverage.