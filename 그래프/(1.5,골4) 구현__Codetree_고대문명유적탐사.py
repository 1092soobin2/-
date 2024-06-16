# 5*5 grid
# youmul 7종류 [1,7]

import heapq
from typing import List

# === in
K, M = map(int, input().split())
LEN_GRID = 5
grid = [list(map(int, input().split())) for _ in range(LEN_GRID)]
WALL = list(map(int, input().split()))
wall_index = 0


# === alg
def get_youmul_list(local_grid) -> list:

    youmul_list = []
    visited_yn = [[False]*LEN_GRID for _ in range(LEN_GRID)]

    # 유물이면 (크기 3 이상) 리스트 리턴
    def __dfs(start: list) -> list:

        stack = [start]
        acc_stack = [start]
        sr, sc = start
        visited_yn[sr][sc] = True
        criteria = local_grid[sr][sc]

        while stack:
            curr_r, curr_c = stack.pop()

            for dr, dc in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                nr, nc = curr_r + dr, curr_c + dc
                if 0 <= nr < LEN_GRID and 0 <= nc < LEN_GRID and not visited_yn[nr][nc] and local_grid[nr][nc] == criteria:
                    visited_yn[nr][nc] = True
                    stack.append([nr,nc])
                    acc_stack.append([nr,nc])
        
        return acc_stack if len(acc_stack) >= 3 else []

    for r in range(LEN_GRID):
        for c in range(LEN_GRID):
            if not visited_yn[r][c]:
                youmul_list.extend(__dfs([r, c]))
    
    return youmul_list
                
    
# 1. explore_youmul
def explore_youmul():
    global grid

    def get_rotated_grid(mid_r, mid_c, angle) -> List[List[int]]:
        new_grid = [grid[i][:] for i in range(LEN_GRID)]
        direction_list = [[-1,-1],[0,-1],[1,-1],[1,0], [1,1],[0,1],[-1,1],[-1,0]]
        if angle == 90:
            diff = 2
        elif angle == 180:
            diff = 4
        elif angle == 270:
            diff = 6
        else:
            print("angle 오기입")
            exit(1)
        for i in range(8):
            dr, dc = direction_list[i]
            dr2, dc2 = direction_list[(i + diff) % 8]
            new_grid[mid_r + dr][mid_c+dc] = grid[mid_r+dr2][mid_c+dc2]
        return new_grid

    pq = []
    for r in range(1, LEN_GRID - 1):
        for c in range(1, LEN_GRID - 1):
            # 3*3 선택하여 회전 90|180|270
            for angle in [90, 180, 270]:
                # 1) 유물 1차 획득 가치 최대화
                # 2) 각도가 가장 작은 방법
                # 3) min(c) -> minc(r)
                heapq.heappush(pq, (-len(get_youmul_list(get_rotated_grid(r, c, angle))), angle, c, r))

    r, c, angle = pq[0][3], pq[0][2], pq[0][1]
    grid = get_rotated_grid(r, c, angle)
    
    print_debug(f"탐사 진행, 회전 정보: {r, c, angle}")


# 2. get_youmul
def acquire_and_create_youmul() -> int:
    global grid, wall_index

    total_value = 0
    # 유물 1차 획득
    youmul_list = get_youmul_list(grid)

    # 유물 연쇄 획득
    while youmul_list:
    
        # 가치 = num(조각 개수)
        total_value += len(youmul_list)

        # 인접 동종 유물 조각이 사라짐
        # 유적 벽면 순서대로 새로운 조각이 생겨남
        # min(c) -> max(r)
        youmul_list.sort(key=lambda x:[x[1], -x[0]])

        for r, c in youmul_list:
            if wall_index >= len(WALL):
                return 0
            grid[r][c] = WALL[wall_index]
            wall_index += 1

        print_debug(f"유물 획득, 유물 위치 정보: {youmul_list}")
        
        youmul_list = get_youmul_list(grid)
    
    return total_value 


# 3. repeat K times
def one_turn() -> int:
    
    explore_youmul()
    value = acquire_and_create_youmul()

    return value


# ans: 각 턴마다 획득한 가치
def algorithm():
    
    value_list = []

    for _ in range(K):
        value = one_turn()
        if value == 0:
            break
        value_list.append(value)
        
    print(" ".join(map(str, value_list)))


def print_debug(title="", debug=False):
    if not debug:
        return
    print("==========" + title)
    for r in range(LEN_GRID):
        print(*grid[r])
    print("====================")

# === out
algorithm()
