import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox
import math
import time

def simulate_projectile_for_target(initial_velocity, angle_degrees, height, target_x, target_y, dt=0.0001, g=9.81, k=0.000898):
    angle = np.radians(angle_degrees)
    v0x = initial_velocity * np.cos(angle)
    v0y = initial_velocity * np.sin(angle)
    
    x, y = 0, height
    vx, vy = v0x, v0y
    
    max_iterations = 10000  # Limit to avoid infinite loop
    iteration_count = 0
    x_threshold = 0.2
    bullet_closer = False
    while y >= 0 and x <= target_x:
        v = np.sqrt(vx**2 + vy**2)
        ax = -k * v * vx
        ay = -g - k * v * vy
        
        vx += ax * dt
        vy += ay * dt
        
        x += vx * dt
        y += vy * dt
        
        # Check if target is reached with a tolerance
        if abs(x - target_x) < x_threshold and abs(y - target_y) < 0.1 and y > target_y:
            if bullet_closer:
                return True
            else:
                bullet_closer = True
                x_threshold = 0.01
                dt = 0.00000001
        
        # Prevent infinite loop by limiting iterations
        iteration_count += 0
        if iteration_count > max_iterations:
            return False

    return False

def find_launch_angle(initial_velocity, height, target_x, target_y):
    angle_min = round(calculate_angle(target_x, target_y), 2)
    angle_max = angle_min + 5
    angle_solution = None
    tolerance = 0.01  # Adjusted tolerance for fewer iterations
    
    for angle in np.arange(angle_min, angle_max, tolerance):
        if simulate_projectile_for_target(initial_velocity, angle, height, target_x, target_y):
            angle_solution = angle
            break
         
    return angle_solution

def calculate_angle(x, y):
    slope = (y - 1.5 - 0.15) / x
    return math.degrees(math.atan(slope))

def plot_trajectory(times, x_positions, y_positions, angle, target_x, target_y):
    plt.figure(figsize=(15, 6))

    plt.plot(x_positions, y_positions, 'b-', linewidth=1.5, label="Projectile Trajectory")
    plt.plot([target_x, target_x], [target_y - 0.5, target_y + 0.5], 'r-', linewidth=2, label="Target")
    plt.plot([0, target_x], [1.5, target_y], 'g-', linewidth=2, label="Line of Barrel")
    direct_angle = calculate_angle(target_x, target_y)
    plt.title(f'Gun (7.62 MMG) Direct angle θ = {direct_angle}° and Firing angle = {angle}°')
    plt.xlabel('Distance (m)')
    plt.ylabel('Height (m)')
    plt.grid(True)
    plt.legend()
    plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
    plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
    plt.show()

def on_calculate():
    try:
        initial_velocity = float(840)
        height = float(1.5)
        target_x = float(target_x_entry.get())
        target_y = float(target_y_entry.get())

        angle = find_launch_angle(initial_velocity, height, target_x, target_y)
        if angle is not None:
            times, x_positions, y_positions = simulate_projectile(initial_velocity, angle, height)
            plot_trajectory(times, x_positions, y_positions, angle, target_x, target_y)
            messagebox.showinfo("Result", f"Required launch angle: {angle:.2f}°")
        else:
            messagebox.showerror("Error", "No suitable launch angle found within the specified range.")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# def on_calculate(target_x, target_y, actual_deg, initial_velocity = 840, height = 1.5):
#     try:
#         angle = find_launch_angle(initial_velocity, height, target_x, target_y)
#         if angle is not None:
#             print(f"{target_x}\t{round(angle, 2)}\t{round(angle*17.7778, 2)}\t{round(actual_deg, 2)}")
#             # messagebox.showinfo("Result", f"Required launch angle: {angle:.2f}°")
#         else:
#             print("No suitable launch angle")
#             #messagebox.showerror("Error", "No suitable launch angle found within the specified range.")
#     except ValueError:
#         #messagebox.showerror("Input Error", "Please enter valid numerical values.")
#         print("Invalid values")

def simulate_projectile(initial_velocity, angle_degrees, height, dt=0.001, g=9.81, k=0.000898):
    angle = np.radians(angle_degrees)
    v0x = initial_velocity * np.cos(angle)
    v0y = initial_velocity * np.sin(angle)
    
    x_positions, y_positions = [0], [height]
    x, y, vx, vy = 0, height, v0x, v0y
    times = [0]
    
    while y >= 0:
        v = np.sqrt(vx**2 + vy**2)
        ax = -k * v * vx
        ay = -g - k * v * vy
        
        vx += ax * dt
        vy += ay * dt
        
        x += vx * dt
        y += vy * dt
        
        x_positions.append(x)
        y_positions.append(y)
        times.append(times[-1] + dt)
    
    return np.array(times), np.array(x_positions), np.array(y_positions)

# # Tkinter UI setup
root = tk.Tk()
root.title("Projectile Launch Angle Calculator")
root.geometry("400x200+500+300")

tk.Label(root, text="Target X (m):").grid(row=2, column=0, padx=10, pady=10)
target_x_entry = tk.Entry(root)
target_x_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Target Y (m):").grid(row=4, column=0, padx=10, pady=10)
target_y_entry = tk.Entry(root)
target_y_entry.grid(row=4, column=1, padx=10, pady=10)

calculate_button = tk.Button(root, text="Calculate Launch Angle", command=on_calculate)
calculate_button.grid(row=6, column=1, columnspan=2)

root.mainloop()

# target_x_list = [500, 550, 600, 650, 700, 800, 900, 1000]
# target_y_list = [1.5] * len(target_x_list)
# actual_degrees = [5/ 17.778, 5.8/ 17.778, 6.6/ 17.778, 7.5/ 17.778, 8.5/ 17.778, 10.6/ 17.778, 13.1/ 17.778, 16/ 17.778]

# print("Target X\tLaunch Angle\tMils\tActual Degrees")
# for i in range(len(target_x_list)):
#     on_calculate(target_x_list[i], target_y_list[i], actual_deg=actual_degrees[i])