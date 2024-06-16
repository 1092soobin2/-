# (0.7, gol4) Codetree_원자충돌

# N*N grid
# M atoms [Mass, Direction, Speed, Loc]



from typing import List


class Atom:
    direction_list = [[-1, 0], [-1, 1], [0, 1], [1, 1],
                      [1, 0], [1, -1], [0, -1], [-1, -1]]

    def __init__(self, mass, direction_id, speed):

        self.mass = mass
        self.direction_id = direction_id
        self.speed = speed

# ===
N, M, K = map(int, input().split())
atom_board: List[List[List[Atom]]] = [[list() for _ in range(N)] for _ in range(N)]
for _ in range(M):
    x, y, m, s, d = map(int, input().split())
    atom_board[x-1][y-1].append(Atom(m, d, s))


# ===
# 1. all atom -> 1초마다 self.direction 으로 self.speed 만큼 이동
def move_all_atom():
    global atom_board

    new_board: List[List[List[Atom]]] = [[list() for _ in range(N)] for _ in range(N)]
    for r in range(N):
        for c in range(N):
            for atom in atom_board[r][c]:
                dr, dc = Atom.direction_list[atom.direction_id]
                nr, nc = (r + dr * atom.speed) % N, (c + dc * atom.speed) % N
                new_board[nr][nc].append(atom)

    atom_board = new_board


# 2. 이동 이후 한 칸 에 2 이상의 원자가 있는 경우
def check_atom_board():
    global atom_board

    for r in range(N):
        for c in range(N):
            if len(atom_board[r][c]) > 1:
                # 1) mass, speed 를 모두 합한 1 원자로 합쳐짐
                total_mass, total_speed, num_atom = 0, 0, len(atom_board[r][c])
                direction_id = atom_board[r][c][0].direction_id % 2
                for atom in atom_board[r][c]:
                    total_mass += atom.mass
                    total_speed += atom.speed
                    if direction_id == -1:
                        continue
                    elif direction_id % 2 != atom.direction_id % 2:
                        direction_id = -1
                atom_board[r][c].clear()
                # 2) 4 원자로 나눠짐
                # 4) 질량 0인 원소는 소멸함
                if total_mass // 5 == 0:
                    continue
                # 3) mass = total_mass // 5
                #      speed = (total_speed) // num(atom)
                #      direction = 모두 상하좌우 중 하나 대각선 중 하나 -> 각각 상하좌우,  그렇지 않으면 대각 선 네 방향
                mass = total_mass // 5
                speed = total_speed // num_atom
                for d_id in range(1 if direction_id == -1 else 0, 8, 2):
                    atom_board[r][c].append(Atom(mass, d_id, speed))


# ===
def solution():
    for _ in range(K):
        move_all_atom()
        check_atom_board()

    answer = 0
    for r in range(N):
        for c in range(N):
            for atom in atom_board[r][c]:
                answer += atom.mass

    return answer


print(solution())
