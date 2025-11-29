# Quick Start Guide

## Setup (First Time Only)

### 1. Install Dependencies
```powershell
cd wall-robot-backend
python -m pip install -r requirements.txt
```

### 2. Initialize Database
```powershell
python init_db.py
```

## Running the Project

### 3. Start Backend Server (Terminal 1)
```powershell
cd wall-robot-backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:
- API: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
- API Docs: http://127.0.0.1:8000/redoc

### 4. Start Frontend Server (Terminal 2 - New Window)
```powershell
cd wall-robot-backend
python -m http.server 3000 --bind 127.0.0.1 --directory frontend
```

Open your browser: http://127.0.0.1:3000/

## Testing

### Run All Tests
```powershell
cd wall-robot-backend
python -m pytest tests/test_api.py -v
```

### Run Tests with Coverage
```powershell
python -m pytest tests/ -v --cov=app
```

## Quick Test Commands

### Test API with curl (PowerShell)
```powershell
# Health check
Invoke-WebRequest -Uri http://127.0.0.1:8000/ -UseBasicParsing

# Create a plan
$body = @{
    wall_width = 5.0
    wall_height = 5.0
    obstacles = @(@{
        x = 2.0
        y = 2.0
        width = 1.0
        height = 1.0
    })
} | ConvertTo-Json

Invoke-WebRequest -Uri http://127.0.0.1:8000/api/plan -Method POST -Body $body -ContentType "application/json" -UseBasicParsing

# Get trajectory (replace 1 with actual job_id)
Invoke-WebRequest -Uri http://127.0.0.1:8000/api/trajectory/1 -UseBasicParsing
```

## Troubleshooting

### Port Already in Use
If port 8000 is busy:
```powershell
python -m uvicorn app.main:app --reload --port 8001
```

### Database Issues
Reset the database:
```powershell
python init_db.py
```

### Dependencies Issues
Reinstall:
```powershell
python -m pip install -r requirements.txt --force-reinstall
```

