# render synthetic animation using given camera focal length and camera
# position
#
# Input:
# - f: double camera focal length
# - pos: double represent camera center position in z axis.
# - points: 3D coordinates for vertices on polygons (use "load points.mat" to get)
# Output:
# - img: 1080*1920*3 matrix, the output render image
#
# after running Dolly_Zoom

import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.animation import FuncAnimation, PillowWriter


def project_objects(f, pos, points, fid):
    points_A = points['points_A']
    points_B = points['points_B']
    points_C = points['points_C']
    
    fig, ax = plt.subplots(figsize=(19.2, 10.8), num=fid)

    # Init function for init an Animation object
    def init():
        ax.set_xlim(0, 1920)
        ax.set_ylim(0, 1080)
        plt.axis('off')
        return []
    
    # Update function for init an Animation object
    def update(frame):
        ax.clear()
        ax.set_xlim(0, 1920)
        ax.set_ylim(0, 1080)
        plt.axis('off')
        focal_length = f[frame]
        position = pos[frame]
    
        # Object 3
        p2d = project(points_C, focal_length, position)
        ax.add_patch(Polygon(p2d[[0, 1, 3, 2]], closed=True, edgecolor='black'))
        ax.add_patch(Polygon(p2d[[2, 3, 5, 4]], closed=True, edgecolor='black'))
        
        # Object 1
        p2d = project(points_A, focal_length, position)
        ax.add_patch(Polygon(p2d[[0, 1, 3, 2]], closed=True, edgecolor='black'))
        ax.add_patch(Polygon(p2d[[2, 3, 5, 4]], closed=True, edgecolor='black'))
        
        # Object 2
        p2d = project(points_B, focal_length, position)
        ax.add_patch(Polygon(p2d[[0, 1, 2]], closed=True, edgecolor='black'))
        ax.add_patch(Polygon(p2d[[1, 2, 3]], closed=True, edgecolor='black'))
        return []
    
    ani = FuncAnimation(fig, update, len(f), init, blit=True, repeat=False, interval=20)
    writer = PillowWriter(fps=30)
    ani.save('/Users/vincent/Documents/main/learn/robotics/robotics-perception/week_01/Week1 Assignment/RoboticsPerceptionWeek1AssignmentCodeFrame/output/dolly_zoom_animation.gif', writer=writer)    
    plt.show()

def project_objects_image(f, pos, points, fid):
    points_A = points['points_A']
    points_B = points['points_B']
    points_C = points['points_C']
    
    fig, ax = plt.subplots(figsize=(19.2, 10.8), num=fid)

    ax.set_xlim(0, 1920)
    ax.set_ylim(0, 1080)
    plt.axis('off')

    # Object 3
    p2d = project(points_C, f, pos)
    ax.add_patch(Polygon(p2d[[0, 1, 3, 2]], closed=True, edgecolor='black'))
    ax.add_patch(Polygon(p2d[[2, 3, 5, 4]], closed=True, edgecolor='black'))
    
    # Object 1
    p2d = project(points_A, f, pos)
    ax.add_patch(Polygon(p2d[[0, 1, 3, 2]], closed=True, edgecolor='black'))
    ax.add_patch(Polygon(p2d[[2, 3, 5, 4]], closed=True, edgecolor='black'))
    
    # Object 2
    p2d = project(points_B, f, pos)
    ax.add_patch(Polygon(p2d[[0, 1, 2]], closed=True, edgecolor='black'))
    ax.add_patch(Polygon(p2d[[1, 2, 3]], closed=True, edgecolor='black'))

    fig.savefig('/Users/vincent/Documents/main/learn/robotics/robotics-perception/week_01/Week1 Assignment/RoboticsPerceptionWeek1AssignmentCodeFrame/output/dolly_zoom_image.png')    
    plt.show()

def project(p3d, f, pos):
    """
    Compute vertex image position from given vertex 3D position and
    camera focal length and camera position.

    Parameters:
    - p3d: n by 3 numpy array, 3D vertex position in world coordinate system
    - f: float, camera focal length
    - pos: float, camera center position

    Returns:
    - p2d: n by 2 numpy array, each row represents vertex image position, in pixel unit
    """
    p2d = np.zeros((p3d.shape[0], 2))
    p2d[:, 0] = p3d[:, 0] * f / (p3d[:, 2] - pos) + 960
    p2d[:, 1] = p3d[:, 1] * f / (p3d[:, 2] - pos) + 540
    
    return p2d
# Example usage
# Assuming points is a dictionary loaded from a file
# points = load('points.mat')
# project_objects(f, pos, points, 1)