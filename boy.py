from pico2d import load_image, get_time

from state_machine import StateMachine, time_out, space_down, right_down, left_down, right_up, left_up


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.face_dir = 1
        self.action = 3
        self.start_time = get_time()
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self) # 소년 객체의 레퍼런스 전달
        self.state_machine.start(Idle) # 초기상태 Idle
        self.state_machine.set_transitions(
            {
                Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, time_out: Sleep},
                Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle},
                Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: Idle}
            }
        )

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        # event : 입력 이벤트 key mouse
        # 우리가 전달할 내용은 튜플
        self.state_machine.add_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        #self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)

#상태를 클래스를 통해서 정의
class Idle:
    @staticmethod  # @ 데코레이터
    def enter(boy, e):

        if boy.face_dir == -1:
            boy.action = 2
        elif boy.face_dir == 1:
            boy.action = 3

        boy.dir = 0
        boy.frame = 0
        #현재 시각 저장
        boy.start_time = get_time()
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = ( boy.frame + 1 ) % 8

        if get_time() - boy.start_time > 3:
           boy.state_machine.add_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)

class Sleep:
    @staticmethod
    def enter(boy, e):
        if boy.face_dir == -1:
            boy.action = 2
        elif boy.face_dir == 1:
            boy.action = 3
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        pass

    @staticmethod
    def draw(boy):
        if boy.action == 2:
            boy.image.clip_composite_draw(
                boy.frame * 100, boy.action * 100, 100, 100,
                -3.141592 / 2, '', boy.x + 25, boy.y - 25, 100, 100)
            return

        boy.image.clip_composite_draw(
            boy.frame * 100, boy.action * 100, 100, 100,
            3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)



class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.dir = 1 # 우
            boy.face_dir = 1
            boy.action = 1
        elif left_down(e) or right_up(e):
            boy.dir = -1 # 좌
            boy.face_dir = -1
            boy.action = 0
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.x += boy.dir * 5
        boy.frame = ( boy.frame + 1 ) % 8
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(
            boy.frame * 100, boy.action * 100, 100, 100,
            boy.x, boy.y
        )
        pass
