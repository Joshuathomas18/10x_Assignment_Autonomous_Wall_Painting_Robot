# Autonomous Wall-Finishing Robot Control System
### BE Intern Assignment | 10x Construction

> **[VIDEO WALKTHROUGH LINK HERE]** > *(Please watch the video for a visual demonstration of the coverage path planning and architecture)*

---

## 1. Problem Statement
[cite_start]The objective was to design a robust, server-intensive control system for an autonomous wall-finishing robot[cite: 2]. The system required:
* [cite_start]**Coverage Planning:** A 100% coverage path for a rectangular wall (e.g., 5m x 5m) while strictly avoiding obstacles (e.g., windows)[cite: 6, 28].
* [cite_start]**High-Performance Backend:** A FastAPI server handling intensive computations without blocking[cite: 10].
* [cite_start]**Optimized Data Storage:** Storing complex trajectory data efficiently in SQLite with indexing[cite: 11].
* [cite_start]**Visualization:** A custom 2D web visualization (No Matplotlib allowed)[cite: 16].

---

## 2. The Engineering Journey: Evolution of the Algorithm
To achieve a robust industrial-grade path, I iterated through three distinct algorithmic approaches. This evolution ensures the robot respects physical constraints and avoids "local minima" traps.

### Phase 1: Naive Boustrophedon (The "For Loop")
* **Approach:** I started with a simple double `for` loop, iterating rows and columns.
* **The Failure:** While this covered the grid, it lacked spatial awareness. If an obstacle blocked the middle of a row, the algorithm simply skipped the blocked cells and "teleported" the path to the other side. [cite_start]This created physically impossible paths that clipped through the obstacle[cite: 29].

### Phase 2: Greedy Search (The "Spiral Trap")
* **Approach:** I switched to a graph-based traversal. The robot would look for the nearest unvisited neighbor and move there.
* **The Failure:** This worked for simple cases but failed in complex geometries. The robot would hug the walls of the obstacle, spiraling inward until it trapped itself in a corner, unable to escape without crossing its own path.

### Phase 3: Segment-Based Decomposition (The Final Solution)
* **Approach:** I implemented a **Segment-Based Boustrophedon** approach.
    1.  The wall is decomposed into horizontal "strips" of free space.
    2.  The algorithm prioritizes finishing an entire vertical "stack" of strips (e.g., the Left Zone) before moving to the next stack (the Right Zone).
    3.  **Connecting Moves:** When switching zones, the robot calculates a BFS (Breadth-First Search) path to travel around the obstacle.
* **Result:** A clean, predictable, and efficient path that finishes one side of the wall completely before jumping to the other, with zero clipping and zero spirals.

---

## 3. System Architecture & "Overkill" Optimizations
[cite_start]Per the assignment requirements to include "overkill" optimizations[cite: 15], I engineered the system for scale:

### Backend: FastAPI + Async SQLAlchemy
* **Server-Intensive Handling:** Path planning is CPU-intensive. I utilized FastAPI's `BackgroundTasks` to offload the calculation, ensuring the API remains non-blocking and responsive immediately after a request is received.
* [cite_start]**Structured Logging:** Implemented `structlog` to output machine-readable JSON logs for every request and calculation event[cite: 14].

### Database: The O(1) Retrieval Strategy
* **The Challenge:** Storing a path with 5,000+ coordinate points as individual database rows is inefficient and slow to query.
* **The Optimization:** I store the entire trajectory as a **zlib-compressed Binary BLOB** within a single column in SQLite.
* [cite_start]**The Result:** Retrieving a complex trajectory takes **O(1)** time (one disk seek) regardless of path length, drastically reducing latency compared to querying thousands of rows[cite: 11].

### Frontend: Native Canvas API
* [cite_start]**No Matplotlib:** The visualization uses the HTML5 Canvas API and JavaScript[cite: 16].
* **Animation:** Instead of a static image, the path is rendered using `requestAnimationFrame` to simulate the robot's physical movement speed.

---

## 4. How to Run

### Prerequisites
* Python 3.9+
* `pip`

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
