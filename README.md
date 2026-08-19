# 🛍️ AI Rise Global HQ Commerce API

A high-performance, asynchronous REST API engine built for modern e-commerce platforms using **FastAPI** and **Supabase (PostgreSQL)**. Engineered with Role-Based Access Control (RBAC), JWT authentication, and relational catalog mapping.

---

## ✨ Key Features

* **⚡ Async Performance:** Powered by FastAPI & Uvicorn for ultra-low latency response times.
* **🔐 Authentication & RBAC:** Secure JWT auth via Supabase with granular access rights (*Admin vs Customer*).
* **🗄️ Relational Database:** PostgreSQL foreign key mappings linking products (`items`) directly to `categories`.
* **🛡️ Data Validation:** Strict request/response payload validation using Pydantic Schemas.
* **📖 Interactive API Docs:** Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`).

---

## 🛠️ Tech Stack

* **Backend Framework:** Python 3.11+ / FastAPI
* **Database & Auth:** Supabase (PostgreSQL)
* **ASGI Server:** Uvicorn
* **Environment Management:** Python Dotenv
* **Documentation:** OpenAPI / Swagger UI

---

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.10+ installed along with a configured Supabase project.

### Installation

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/YOUR_GITHUB_USERNAME/nexus-commerce-api.git](https://github.com/YOUR_GITHUB_USERNAME/nexus-commerce-api.git)
   cd nexus-commerce-api
