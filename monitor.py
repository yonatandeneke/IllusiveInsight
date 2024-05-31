import pygame
import cv2
import numpy as np

# Initialize Pygame
pygame.init()

# Set the display mode to Windowed
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

# Load the video
cap = cv2.VideoCapture('video.mp4')

# Check if the video is loaded successfully
if not cap.isOpened():
    print("Error: Couldn't open video file.")
    pygame.quit()
    exit()

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Scale factor for the video
scale_factor = min(screen.get_height() / (3 * frame_height), screen.get_height() / (3 * frame_width))

# New dimensions for the video
new_width = int(frame_width * scale_factor)
new_height = int(frame_width * scale_factor)

# Blit the video onto the screen
running = True
while running:
    ret, frame = cap.read()
    if not ret:
        # Reset the video capture to the beginning
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Resize the frame
    frame = cv2.resize(frame, (new_width, new_height))

    # Convert OpenCV BGR image to RGB (Pygame uses RGB)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert the frame to Pygame surface
    frame = pygame.image.frombuffer(frame.tobytes(), (new_width, new_height), 'RGB')

    # Calculate the coordinates to place the frames in each quadrant
    center_x = (screen.get_width() - new_width) // 2
    center_y = (screen.get_height() - new_width) // 2

    # Blit the frame onto the screen in each quadrant
    screen.blit(frame, (center_x, 0))
    screen.blit(pygame.transform.rotate(frame, 180), (center_x, center_y + new_width))
    screen.blit(pygame.transform.rotate(frame, 90), (center_x - new_width, center_y))
    screen.blit(pygame.transform.rotate(frame, 270), (center_x + new_width, center_y))

    # Update the display
    pygame.display.flip()

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Release the video capture and quit Pygame
cap.release()
pygame.quit()
