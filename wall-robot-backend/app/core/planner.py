import numpy as np
from collections import deque
from typing import List, Dict, Tuple

class CoveragePlanner:
    def __init__(self, wall_width: float, wall_height: float, tool_size: float = 0.1):
        self.width = wall_width
        self.height = wall_height
        self.tool_size = tool_size
        self.cols = int(np.ceil(self.width / self.tool_size))
        self.rows = int(np.ceil(self.height / self.tool_size))
        self.grid = np.zeros((self.rows, self.cols), dtype=int) # 0=Free, 1=Obstacle

    def add_obstacle(self, x: float, y: float, w: float, h: float):
        # Mark cells that overlap with obstacle
        for r in range(self.rows):
            for c in range(self.cols):
                cx = (c * self.tool_size) + (self.tool_size / 2)
                cy = (r * self.tool_size) + (self.tool_size / 2)
                if (x - 1e-3 <= cx <= x + w + 1e-3) and (y - 1e-3 <= cy <= y + h + 1e-3):
                    self.grid[r, c] = 1

    def _grid_to_world(self, r, c, is_spraying=True):
        x = round((c * self.tool_size) + (self.tool_size / 2), 3)
        y = round((r * self.tool_size) + (self.tool_size / 2), 3)
        return {"x": x, "y": y, "is_spraying": is_spraying}

    def _get_path_bfs(self, start: Tuple[int, int], end: Tuple[int, int]):
        if start == end: return []
        q = deque([(start, [])])
        seen = set([start])
        
        while q:
            (r, c), path = q.popleft()
            if (r, c) == end:
                return path
            
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr, nc] == 0 and (nr, nc) not in seen:
                        seen.add((nr, nc))
                        q.append(((nr, nc), path + [(nr, nc)]))
        return []

    def plan_path(self) -> List[Dict[str, float]]:
        # Break grid into horizontal segments
        segments = []
        for r in range(self.rows):
            c = 0
            while c < self.cols:
                if self.grid[r, c] == 0:
                    start = c
                    while c < self.cols and self.grid[r, c] == 0:
                        c += 1
                    end = c - 1
                    segments.append({'r': r, 'c_start': start, 'c_end': end, 'visited': False})
                else:
                    c += 1

        if not segments: return []

        # Chain segments together
        final_path = []
        segments.sort(key=lambda s: (s['r'], s['c_start']))
        
        current_seg = segments[0]
        current_pos = (current_seg['r'], current_seg['c_start'])
        final_path.append(self._grid_to_world(*current_pos, is_spraying=True))

        VERTICAL_BOOST = 999
        
        while True:
            current_seg['visited'] = True
            
            dist_to_start = abs(current_pos[1] - current_seg['c_start'])
            dist_to_end = abs(current_pos[1] - current_seg['c_end'])
            
            if dist_to_start < dist_to_end:
                path_r = current_seg['r']
                for c in range(current_seg['c_start'], current_seg['c_end'] + 1):
                    final_path.append(self._grid_to_world(path_r, c, is_spraying=True))
                current_pos = (path_r, current_seg['c_end'])
            else:
                path_r = current_seg['r']
                for c in range(current_seg['c_end'], current_seg['c_start'] - 1, -1):
                    final_path.append(self._grid_to_world(path_r, c, is_spraying=True))
                current_pos = (path_r, current_seg['c_start'])

            next_seg = None
            best_cost = float('inf')
            
            unvisited = [s for s in segments if not s['visited']]
            if not unvisited: break
            
            for seg in unvisited:
                d1 = abs(seg['r'] - current_pos[0]) + abs(seg['c_start'] - current_pos[1])
                d2 = abs(seg['r'] - current_pos[0]) + abs(seg['c_end'] - current_pos[1])
                dist = min(d1, d2)
                cost = dist
                
                if abs(seg['r'] - current_pos[0]) == 1:
                    overlap = max(0, min(current_seg['c_end'], seg['c_end']) - max(current_seg['c_start'], seg['c_start']))
                    if overlap > 0:
                        cost -= VERTICAL_BOOST
                
                if cost < best_cost:
                    best_cost = cost
                    next_seg = seg

            target_entry = (next_seg['r'], next_seg['c_start'])
            if abs(current_pos[0] - next_seg['r']) + abs(current_pos[1] - next_seg['c_end']) < \
               abs(current_pos[0] - next_seg['r']) + abs(current_pos[1] - next_seg['c_start']):
               target_entry = (next_seg['r'], next_seg['c_end'])
            
            travel_path = self._get_path_bfs(current_pos, target_entry)
            for r, c in travel_path:
                final_path.append(self._grid_to_world(r, c, is_spraying=False))
                
            current_seg = next_seg
            current_pos = target_entry

        return final_path
