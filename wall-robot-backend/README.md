# Autonomous Wall Painting Robot - Coverage Path Planning

A production-grade modular monolith system for generating optimal coverage paths for a wall-finishing robot, avoiding obstacles using Boustrophedon (Ox-plowing) cellular decomposition.

## Architecture

This system follows a **Modular Monolith** pattern—a single deployable unit (FastAPI) with clear internal separation of concerns:

- **`app/core/`**: Pure business logic (geometry, algorithms) - No I/O dependencies
- **`app/api/`**: FastAPI routers - HTTP interface, validation
- **`app/db/`**: SQLite + Async SQLAlchemy - Data persistence layer
- **`frontend/`**: HTML5 Canvas visualizer - User interface
- **`tests/`**: Automated unit and integration tests

## Project Structure

```
wall-robot-backend/
├── app/
│   ├── __init__.py
│   ├── api/                 # API Endpoints
│   │   ├── __init__.py
│   │   ├── endpoints.py     # POST/GET routes
│   │   └── schemas.py       # Pydantic models
│   ├── core/                # Business Logic
│   │   ├── __init__.py
│   │   └── planner.py       # Path planning algorithm
│   ├── db/                  # Database
│   │   ├── __init__.py
│   │   ├── database.py      # DB connection
│   │   └── models.py        # SQLite models
│   └── main.py              # FastAPI app
├── frontend/                # Frontend
│   └── index.html           # Canvas visualizer
├── tests/                   # Tests
│   ├── __init__.py
│   └── test_api.py          # API tests
├── .gitignore
├── requirements.txt
└── README.md
```


## Quick Start

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Initialize Database
```powershell
python init_db.py
```

### 3. Start Backend Server (Terminal 1)
```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API will be available at:
- http://127.0.0.1:8000/ (Health check)
- http://127.0.0.1:8000/docs (Swagger UI)

### 4. Start Frontend Server (Terminal 2)
```powershell
python -m http.server 3000 --bind 127.0.0.1 --directory frontend
```

Open browser: http://127.0.0.1:3000/

### 5. Run Tests
```powershell
pytest tests/test_api.py -v
```

See `QUICKSTART.md` for detailed commands and troubleshooting.

## Technical Decisions

1. **Segment-Based Boustrophedon**: Breaks wall into horizontal segments, prioritizes vertical adjacency
2. **BFS Pathfinding**: Handles obstacle navigation when segments are disconnected
3. **BLOB Storage**: Compressed JSON storage (zlib) for efficient retrieval vs row-per-point
4. **Async API**: Non-blocking endpoints with background tasks and job polling



