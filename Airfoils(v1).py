# 4-Digit NACA Plotter

import matplotlib.pyplot as plt
import numpy as np

# User input for 4-digit NACA airfoil code

print("\n| 4-Digit NACA Airfoil Plotter |")
print("--------------------------------")
try:
    code = input("Enter 4-Digit NACA Airfoil Number (without spaces): ")
    if len(code) != 4 or not code.isdigit():
        raise ValueError("Invalid NACA code. Please enter a 4-digit number.")
except ValueError:
    print("Invalid input! Using default NACA 2412.")
    code = '2412'

# If statement to check if the first two digits are '00' or not

if int(code[0]) == 0 and int(code[1]) == 0:
    def naca00xx(code, chord=1):
        x = np.arange(0, chord, 0.0001)
        t = ((10 * int(code[2])) + int(code[3])) / 100

        # Thickness calculation
        y = list(map(lambda num: 5 * t * (0.2969 * (num ** 0.5) - 0.1260 * num - 0.3516 * (num ** 2) +
                                         0.2843 * (num ** 3) - 0.1036 * (num ** 4)), x))
        yy = list(map(lambda num: -num, y))  # Negate y for lower surface

        plt.plot(x, y, label="NACA" + ' -' + " " + str(code[0]) + str(code[1]) + str(code[2]) + str(code[3]),
                 color='black', linewidth=1.4)
        plt.plot(x, yy, color='black', linewidth=1.4)
        plt.plot([0, 1], [0, 0], '--', color='black', linewidth=1.25)
        plt.ylim(-0.5, 0.5)
        plt.legend()
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("NACA" + " - " + str(code[0]) + str(code[1]) + str(code[2]) + str(code[3]) + " Airfoil Plot")
        plt.grid()
        plt.show()

    naca00xx(code)

else:
    def nacaxxxx(code, chord=1):
        x = np.arange(0, chord, 0.0001)
        t = ((10 * int(code[2])) + int(code[3])) / 100
        m_input = int(code[0])
        p_input = int(code[1])
        m = m_input / 100
        p = p_input / 10

        # Camber line calculation
        yc = list(map(lambda num: (m / (p ** 2)) * (2 * p * num - num ** 2)
                      if 0 <= num <= p else
                      (m / ((1 - p) ** 2)) * ((1 - 2 * p) + 2 * p * num - num ** 2), x))

        # Thickness calculation
        yt = list(map(lambda num: 5 * t * (0.2969 * (num ** 0.5) - 0.1260 * num - 0.3516 * (num ** 2) +
                                          0.2843 * (num ** 3) - 0.1036 * (num ** 4)), x))

        # Derivative of camber line
        dycdx = list(map(lambda num: ((2 * m) / (p ** 2)) * (p - num)
                         if 0 <= num <= p else
                         (2 * m) / ((1 - p) ** 2) * (p - num), x))

        
        theta = list(map(np.arctan, dycdx))

        # Upper and lower surface coordinates
        xv = list(map(lambda num, yt_val, theta_val: num - yt_val * np.sin(theta_val), x, yt, theta))
        yv = list(map(lambda yc_val, yt_val, theta_val: yc_val + yt_val * np.cos(theta_val), yc, yt, theta))
        xl = list(map(lambda num, yt_val, theta_val: num + yt_val * np.sin(theta_val), x, yt, theta))
        yl = list(map(lambda yc_val, yt_val, theta_val: yc_val - yt_val * np.cos(theta_val), yc, yt, theta))

        plt.ylim(-0.5, 0.5)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("NACA" + " - " + str(code[0]) + str(code[1]) + str(code[2]) + str(code[3]) + " Airfoil Plot")
        plt.plot(x, yc, label='Mean Camber Line', linestyle='--', color='black', linewidth=1.25)
        plt.plot(xv, yv, color='black', label='NACA' + " - " + str(code[0]) + str(code[1]) + str(code[2]) + str(code[3]),
                 linewidth=1.4)
        plt.plot(xl, yl, color='black', linewidth=1.4)
        plt.legend()
        plt.grid()
        plt.show()

    nacaxxxx(code)