# FastAPI + Vue Data Generation Service

A professional full-stack application featuring a FastAPI backend with a Vue frontend for versatile data generation and processing.

## 🌟 Features

- **Data Generation API** : Create customizable datasets with various data types
- **Sample Datasets** : Ready-to-use sample data for users, products, and transactions
- **Multiple Output Formats** : Export data as CSV or JSON
- **File Upload & Analysis** : Process and analyze uploaded CSV and JSON files
- **Modern Frontend** : Intuitive UI built with Vue 3 and modern components
- **Docker Ready** : Containerized application setup with docker-compose
- **Professional Architecture** : Well-structured project with clear separation of concerns

## 🏗️ Project Structure

```
./
├── backend/               # FastAPI backend application
│   ├── app/               # Application code
│   │   ├── api/           # API routes, dependencies, and utilities
│   │   ├── core/          # Core functionality (config, events, logging)
│   │   ├── models/        # Database models
│   │   ├── schemas/       # Pydantic schemas for request/response validation
│   │   ├── services/      # Business logic services
│   ├── tests/             # Test suite
│   ├── main.py            # Application entry point
│   ├── Dockerfile         # Backend container definition
│
├── frontend/              # Vue 3 frontend application
│   ├── src/               # Source code
│   │   ├── assets/        # Static assets
│   │   ├── components/    # Vue components
│   │   ├── pages/         # Page components
│   │   ├── router/        # Vue Router configuration
│   │   ├── services/      # API client services
│   ├── public/            # Public static files
│   ├── index.html         # Entry HTML file
│
├── docker-compose.yml     # Container orchestration
├── README.md              # Project documentation
```

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development)
- Node.js 16+ (for local frontend development)

### Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fastapi-vue-data-service.git
   cd fastapi-vue-data-service
   ```
2. Create a `.env` file based on the example:
   ```bash
   cp backend/.env.example backend/.env
   ```
3. Start the application:
   ```bash
   docker-compose up
   ```
4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development

#### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python main.py
   ```

#### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

## 📊 API Endpoints

### Health Check

```
GET /health
```

Verifies the service is running properly.

### Data Generation

```
GET /api/data/generate
```

Generate custom datasets with parameters:

- `rows`: Number of rows (1-1000)
- `columns`: Number of columns (1-20)
- `data_types`: List of data types for columns
- `format`: Output format (csv or json)

### Sample Datasets

```
GET /api/data/sample/{sample_type}
```

Get pre-configured sample datasets:

- `sample_type`: Type of sample (users, products, transactions)
- `rows`: Number of rows to generate
- `format`: Output format (csv or json)

### File Upload

```
POST /api/data/upload
```

Upload and analyze a CSV or JSON file.

## 🧪 Testing

Run the backend test suite:

```bash
cd backend
pytest
```

Run the frontend tests:

```bash
cd frontend
npm run test:unit
```

## 🔒 Security

This project includes CORS configuration, exception handling, and request audit logging. In production, make sure to:

1. Set specific CORS origins instead of the wildcard `*`
2. Enable HTTPS
3. Set `DEBUG=False` in the backend environment

## 📄 License

[MIT](https://claude.ai/chat/LICENSE)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
