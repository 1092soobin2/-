# 준 선물 개수 비교
    # A > B                             -> A += 1 
    # ( A == 0 && B == 0 ) || (A == B)  -> 선물 지수 더 큰 사람 += 1
    # 선물 지수도 같은                      -> 주고 받지 않음
    
# 선물 지수 = (준 선물 - 받은 선물)

# ans: num(max(가장 많이 선물 받은 사람))
from collections import defaultdict

def solution(friends, gifts):
    
    len_friends = len(friends)
    
    # 한 사람이 친구별로 준 선물 개수
    gift_dict = dict([(name, defaultdict(int)) for name in friends])
    # 한 사람이 주고받은 선물 총 개수
    total_gift_dict = dict([(name, [0,0]) for name in friends])
    give, receive = 0, 1
    
    
    # 선물 세기
    for gift in gifts:
        giver, receiver = gift.split()
        total_gift_dict[giver][give] += 1
        total_gift_dict[receiver][receive] += 1
        
        gift_dict[giver][receiver] += 1
        
    # print(gift_dict)
    # print(total_gift_dict)
    
    # 선물 주고 받기
    this_month_gift_dict = defaultdict(int)
    for i in range(len_friends):
        f1 = friends[i]
        for f2 in friends[i+1:]:
            f1_give, f2_give = gift_dict[f1][f2], gift_dict[f2][f1]
            
            # A > B                             -> A += 1 
            # ( A == 0 && B == 0 ) || (A == B)  -> 선물 지수 더 큰 사람 += 1
            if f1_give > f2_give:
                this_month_gift_dict[f1] += 1
            elif f1_give < f2_give:
                this_month_gift_dict[f2] += 1
            else:
                # 선물 지수도 같은                      -> 주고 받지 않음 
                f1_index, f2_index = total_gift_dict[f1][give] - total_gift_dict[f1][receive],  total_gift_dict[f2][give] - total_gift_dict[f2][receive]
                if f1_index > f2_index:
                    this_month_gift_dict[f1] += 1
                elif f1_index < f2_index:
                    this_month_gift_dict[f2] += 1
                else:
                    pass
                
    
    answer = max(this_month_gift_dict.values()) if this_month_gift_dict.values() else 0
    return answer
