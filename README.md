# Atlan Integration Backend

A Flask-based backend application for integrating with Atlan's data catalog platform.

## Overview

This backend provides a comprehensive API for interacting with Atlan's data catalog. It includes functionality for:

- Authentication and authorization
- Asset management
- Data lineage
- Glossary and term management
- Search capabilities
- Administrative operations

## Architecture

The application follows a layered architecture:

1. **API Layer**: RESTful endpoints for client interaction
2. **Service Layer**: Business logic and integration with Atlan's API
3. **Configuration**: Environment-based configuration management

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)
- Atlan API credentials

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-organization/atlan-integration.git
   cd atlan-integration
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```
   export ATLAN_API_URL=https://api.atlan.com
   export ATLAN_API_KEY=your_api_key
   export ATLAN_API_SECRET=your_api_secret
   export JWT_SECRET_KEY=your_jwt_secret
   ```

   On Windows:
   ```
   set ATLAN_API_URL=https://api.atlan.com
   set ATLAN_API_KEY=your_api_key
   set ATLAN_API_SECRET=your_api_secret
   set JWT_SECRET_KEY=your_jwt_secret
   ```

## Running the Application

Start the development server:

```
python app.py
```

The API will be available at `http://localhost:5000`.

## API Documentation

### Authentication

#### Login

```
POST /api/auth/login
```

Request body:
```json
{
  "username": "user@example.com",
  "password": "password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "user-id",
    "username": "user@example.com",
    "name": "User Name"
  }
}
```

#### Refresh Token

```
POST /api/auth/refresh
```

Request body:
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Assets

#### Get Assets

```
GET /api/assets?limit=10&offset=0
```

Response:
```json
{
  "entities": [
    {
      "guid": "asset-guid-1",
      "name": "Asset 1",
      "typeName": "Table",
      "qualifiedName": "db.schema.table1"
    },
    {
      "guid": "asset-guid-2",
      "name": "Asset 2",
      "typeName": "Column",
      "qualifiedName": "db.schema.table1.column1"
    }
  ],
  "totalCount": 100,
  "offset": 0,
  "limit": 10
}
```

#### Get Asset by GUID

```
GET /api/assets/{guid}
```

Response:
```json
{
  "guid": "asset-guid-1",
  "name": "Asset 1",
  "typeName": "Table",
  "qualifiedName": "db.schema.table1",
  "attributes": {
    "description": "This is a table",
    "owner": "user-id",
    "createTime": 1620000000000,
    "updateTime": 1620100000000
  }
}
```

### Lineage

#### Get Lineage

```
GET /api/lineage?guid={guid}&direction=BOTH&depth=3
```

Response:
```json
{
  "baseEntityGuid": "asset-guid-1",
  "lineageDirection": "BOTH",
  "lineageDepth": 3,
  "guidEntityMap": {
    "asset-guid-1": {
      "guid": "asset-guid-1",
      "name": "Asset 1",
      "typeName": "Table"
    },
    "asset-guid-2": {
      "guid": "asset-guid-2",
      "name": "Asset 2",
      "typeName": "Table"
    }
  },
  "relations": [
    {
      "fromEntityId": "asset-guid-1",
      "toEntityId": "asset-guid-2",
      "relationshipId": "relation-guid-1"
    }
  ]
}
```

### Glossary

#### Get Glossaries

```
GET /api/glossary?limit=10&offset=0
```

Response:
```json
{
  "glossaries": [
    {
      "guid": "glossary-guid-1",
      "name": "Business Glossary",
      "qualifiedName": "business-glossary"
    }
  ],
  "totalCount": 1,
  "offset": 0,
  "limit": 10
}
```

#### Get Terms

```
GET /api/glossary/terms?glossaryGuid={glossaryGuid}&limit=10&offset=0
```

Response:
```json
{
  "terms": [
    {
      "guid": "term-guid-1",
      "name": "Customer",
      "qualifiedName": "business-glossary.customer",
      "glossaryGuid": "glossary-guid-1"
    }
  ],
  "totalCount": 100,
  "offset": 0,
  "limit": 10
}
```

### Search

#### Basic Search

```
POST /api/search
```

Request body:
```json
{
  "query": "customer",
  "limit": 10,
  "offset": 0
}
```

Response:
```json
{
  "entities": [
    {
      "guid": "asset-guid-1",
      "name": "Customer Table",
      "typeName": "Table",
      "qualifiedName": "db.schema.customer"
    }
  ],
  "totalCount": 10,
  "offset": 0,
  "limit": 10
}
```

### Admin

#### Get Users

```
GET /api/admin/users?limit=10&offset=0
```

Response:
```json
{
  "users": [
    {
      "id": "user-id-1",
      "username": "user1@example.com",
      "name": "User One"
    }
  ],
  "totalCount": 100,
  "offset": 0,
  "limit": 10
}
```

## Error Handling

All API endpoints return appropriate HTTP status codes and error messages:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details"
  }
}
```

Common error codes:
- `BAD_REQUEST`: Invalid request parameters
- `UNAUTHORIZED`: Authentication required or failed
- `FORBIDDEN`: Permission denied
- `NOT_FOUND`: Resource not found
- `INTERNAL_SERVER_ERROR`: Server-side error

## Development

### Project Structure

```
atlan-integration/
├── app.py
├── admin.py
├── assets.py
├── auth.py
├── glossary.py
├── lineage.py
├── search.py
├── admin_service.py
├── asset_service.py
├── auth_service.py
├── glossary_service.py
├── lineage_service.py
├── search_service.py
├── docs/
│   ├── architecture/
│   └── api-reference/
├── Dockerfile
├── requirements.txt
└── README.md
```

_Note: a `tests/` directory is not currently included._

### Adding New Features

1. Create or modify the appropriate service module (e.g., `*_service.py`) in the repository root
2. Create or modify API route modules (e.g., `auth.py`, `assets.py`) in the repository root
3. Register any new blueprints in `app.py`
4. Update documentation as needed

## Testing

This repository currently does not include automated tests. When tests are added,
run them with:

```
pytest
```

## Deployment

### Docker

Build the Docker image:

```
docker build -t atlan-integration .
```

Run the container:

```
docker run -p 5000:5000 \
  -e ATLAN_API_URL=https://api.atlan.com \
  -e ATLAN_API_KEY=your_api_key \
  -e ATLAN_API_SECRET=your_api_secret \
  -e JWT_SECRET_KEY=your_jwt_secret \
  atlan-integration
```

## License

[MIT License](LICENSE)

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -am 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request
