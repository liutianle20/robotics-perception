# Extract frames from video.
# %%
import cv2
import os

def extract_frames(video_path, output_folder):
    cap = cv2.VideoCapture(video_path)
    frame_cnt = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_filename = os.path.join(output_folder, f'engSlo_{frame_cnt:02d}.jpg')
        cv2.imwrite(frame_filename, frame)
        frame_cnt += 1
    cap.release

video_path = '/Users/vincent/Downloads/clip.mp4'
output_folder = 'images/engSlo'

# %%
extract_frames(video_path, output_folder)

# %%
