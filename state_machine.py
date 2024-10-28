from tabnanny import check

from sdl2 import SDL_KEYDOWN, SDLK_SPACE


class StateMachine:
    def __init__(self, o):
        self.obj = o    # 어떤 객체를 위한 상태 머신인지 알려줌.
        self.event_q = [] # 이벤트 보관 튜플 리스트(큐)
    def add_event(self, e):
        self.event_q.append(e)

    def start(self, state):
        self.cur_state = state

    def update(self):
        self.cur_state.do(self.obj)
        # 혹시 이벤트가 있나
        if self.event_q: #list는 멤버가 있으면 참 없으면 거짓
            e = self.event_q.pop(0)
            # 현재 상태와 현재 발생한 이벤트에 따라 다음 상태를 결정
            # 상태 변환 테이블 활용
            for check_event, next_state in self.transitions[self.cur_state].items():
                if check_event(e): #
                    self.cur_state.exit(self.obj)
                    self.cur_state = next_state
                    self.cur_state.enter(self.obj)

    def draw(self):
        self.cur_state.draw(self.obj)

    def set_transitions(self, transitions):
        self.transitions = transitions


    #   이벤트 체크 함수
    #상태 이벤트 e = (종류, 실제값) 튜플로 정의
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'