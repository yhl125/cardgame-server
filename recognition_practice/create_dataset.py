import cv2
import mediapipe as mp
import numpy as np
import time, os

actions = ['one', 'two', 'three', 'quit']  # 액션 매칭
seq_length = 30 # 1개씩 넣을 이미지의 윈도우 사이즈 
secs_for_action = 15    # 학습 녹화 시간

# MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils # 손가락 마디를 표시
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,   # 최소 탐지 신뢰도 -> 손이 감지되는 모델의 최소 신뢰값
    min_tracking_confidence=0.5     # 최소 추적 신뢰도 -> 손의 랜드마크 추적의 최소 신뢰값
)    

cap = cv2.VideoCapture(0)   # 웹캠을 열어줌

created_time = int(time.time())
os.makedirs('dataset', exist_ok=True)   #dataset을 만들 폴더 생성

while cap.isOpened():
    for idx, action in enumerate(actions):  # enumerate는 inedx와 데이터 값을 함께 반환함
        data = []

        ret, img = cap.read()   # True or False와 함께 1개의 프레임(이미지)을 반환받음

        img = cv2.flip(img, 1)  # flip은 이미지를 반전시킴

        cv2.putText(img, f'Waiting for collecting {action.upper()} action...', org=(10, 30), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
        cv2.imshow('img', img)
        cv2.waitKey(3000) # 3초간 대기

        start_time = time.time()

        while time.time() - start_time < secs_for_action:   # 30초 동안
            ret, img = cap.read()   # 한 프레임씩 뽑아서
            img = cv2.flip(img, 1)  # 이미지를 반전시키고
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 미디어파이프에서 처리가능하도록 RGB로 변환
            result = hands.process(img) # 데이터 전처리
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # openCV에서 처리가능하도록 BGR로 변환

            if result.multi_hand_landmarks is not None: # multi_hand_landmarks: 감지/추적된 손의 집합. 손은 21개의 랜드마크 리스트로 표현
                for res in result.multi_hand_landmarks:
                    joint = np.zeros((21, 4))   # 21행 4열(x, y, z, visibility)
                    for j, lm in enumerate(res.landmark):
                        joint[j] = [lm.x, lm.y, lm.z, lm.visibility]    # visibility는 노드가 보이는지 안보이는지에 대한 정보

                    # Compute angles between joints
                    v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3] # Parent joint
                    v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3] # Child joint
                    v = v2 - v1 # [20, 3]
                    # Normalize v
                    v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                    # Get angle using arcos of dot product
                    angle = np.arccos(np.einsum(
                                'nt,nt->n',
                                v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:], 
                                v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])
                            )   # [15,]

                    angle = np.degrees(angle) # Convert radian to degree

                    angle_label = np.array([angle], dtype=np.float32)
                    angle_label = np.append(angle_label, idx)   # 라벨을 붙여줌

                    d = np.concatenate([joint.flatten(), angle_label])  # x,y,z와 visibility 데이터를 펼침 -> 행렬

                    data.append(d)

                    mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

            cv2.imshow('img', img)
            if cv2.waitKey(1) == ord('q'):
                break

        data = np.array(data)

        # Create sequence data
        full_seq_data = []
        for seq in range(len(data) - seq_length):
            full_seq_data.append(data[seq:seq + seq_length])

        full_seq_data = np.array(full_seq_data)
        print(action, full_seq_data.shape)
        np.save(os.path.join('dataset', f'seq_{action}'), full_seq_data)
    break
