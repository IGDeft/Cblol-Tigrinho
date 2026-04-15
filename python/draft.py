from enum import Enum

class Fase(Enum):
    BAN_1  = "BAN_1"
    BAN_2  = "BAN_2"
    BAN_3  = "BAN_3"
    BAN_4  = "BAN_4"
    BAN_5  = "BAN_5"
    BAN_6  = "BAN_6"
    BAN_7  = "BAN_7"
    BAN_8 = "BAN_8"
    BAN_9  = "BAN_9"
    BAN_10  = "BAN_10"
    PICK_1 = "PICK_1"
    PICK_2 = "PICK_2"
    PICK_3 = "PICK_3"
    PICK_4 = "PICK_4"
    PICK_5 = "PICK_5"
    PICK_6 = "PICK_6"
    PICK_7 = "PICK_7"
    PICK_8 = "PICK_8"
    PICK_9 = "PICK_9"
    PICK_10 = "PICK_10"
    FIM    = "FIM"

ORDEM_DRAFT = [
    
    (Fase.BAN_1,   True),  
    (Fase.BAN_2,   False), 
    (Fase.BAN_3,   True),
    (Fase.BAN_4,   False),
    (Fase.BAN_5,   True),
    (Fase.BAN_6,   False),

    (Fase.PICK_1,  True),
    (Fase.PICK_2,  False),
    (Fase.PICK_3,  False),
    (Fase.PICK_4,  True),
    (Fase.PICK_5,  True),
    (Fase.PICK_6,  False),

     
    (Fase.BAN_7,   False),  
    (Fase.BAN_8,   True), 
    (Fase.BAN_9,   False),
    (Fase.BAN_10,   True),
    
    (Fase.PICK_7,  False),
    (Fase.PICK_8,  True),
    (Fase.PICK_9,  True),
    (Fase.PICK_10, False),

    (Fase.FIM,     None),
]

def proxima_fase(fase_atual: Fase, is_first_pick: bool) -> tuple[Fase, str]:
    fases = [f for f, _ in ORDEM_DRAFT]
    index = fases.index(fase_atual)
    
    proxima, age_first_pick = ORDEM_DRAFT[index + 1]
    
    if proxima == Fase.FIM:
        return Fase.FIM, "FIM"
    
    if age_first_pick == is_first_pick:
        jogador_atual = "PLAYER"
    else:
        jogador_atual = "IA"
    
    return proxima, jogador_atual