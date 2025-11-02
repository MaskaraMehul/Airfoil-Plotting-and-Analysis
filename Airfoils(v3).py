import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
import pandas as pd

print("\n| 4-Digit NACA Airfoil Plotter |")
print("--------------------------------")
code = input("Enter 4-Digit NACA Airfoil Number (without spaces): ")
print("NACA - " + str(code))

def xfoil_plot(code, vel=400, alpha_i=0, alpha_f=30, alpha_step=0.5, chord=1):
    rho = 1.225
    mu = 1.789e-5
    mach = vel/1235
    re = rho*vel*(5/18)*chord/mu
    n_iter = 100

    # remove old polar file
    if os.path.exists("polar.txt"):
        os.remove("polar.txt")

    # write XFOIL input file
    with open("xfoil_input.inp", 'w') as f:
        f.write(f"NACA {code}\n")
        f.write("PANE\n")
        f.write("OPER\n")
        f.write(f"MACH {mach}\n")
        f.write(f"VISC {re}\n")
        f.write("PACC\n")
        f.write("polar.txt\n\n")
        f.write(f"ITER {n_iter}\n")
        f.write(f"ASEQ {alpha_i} {alpha_f} {alpha_step}\n")
        f.write("PACC\n")
        f.write("QUIT\n")

    # run XFOIL cleanly
    with open("xfoil_input.inp", "rb") as inp:
        subprocess.run(r"C:\Users\ACER\Desktop\my files\python\XFOIL6.99\xfoil.exe",stdin=inp)

    
    df = pd.read_csv("polar.txt", delim_whitespace=True, skiprows=12, header=None)

    fig2,ax2 = plt.subplots(2,2)
    plt.style.use('ggplot')
    ax2[0,0].plot(df[0], df[1] / df[2], label='L/D Ratio')
    ax2[0,0].scatter(df[0][np.argmax(np.array(df[1]/df[2]))],
                     np.max(np.array(df[1]/df[2])), marker = 'x', color = 'black', label = "Max L/D = " + str(format(np.max(np.array(df[1]/df[2])),'.2f') +
                     ', ' + str(df[0][np.argmax(np.array(df[1]/df[2]))]) + 'deg'))
    ax2[0,0].axvline(df[0][np.argmax(df[1])], color = 'black', linestyle = '--', linewidth = 0.75)
    ax2[0,0].set_xlabel('Alpha')
    ax2[0,0].set_ylabel('L/D Ratio')
    ax2[0,0].set_title("L/D Ratio v/s Alpha")
    ax2[0,0].legend()
    ax2[0,0].grid(True)
    
    ax2[0,1].plot(df[0], df[1], label="Cl")
    ax2[0,1].plot(df[0], df[2], label='Cd')
    ax2[0,1].plot(df[0], np.abs(df[4]), label="|Cm|")
    ax2[0,1].scatter(df[0][np.argmax(np.array(df[1]))], 
                     np.max(np.array(df[1])), marker = 'x', c = 'black',
                     label = 'Max Cl = ' + str(format(np.max(np.array(df[1])), '.2f') + ', ' + str(df[0][np.argmax(np.array(df[1]))]) + 'deg'))
    ax2[0,1].axvline(df[0][np.argmax(df[1])], color = 'black', linestyle = '--', linewidth = 0.75)
    ax2[0,1].set_xlabel('Alpha')
    ax2[0,1].set_ylabel('Cl, Cd')
    ax2[0,1].set_title("Cl, Cd v/s Alpha")
    ax2[0,1].legend(loc = 'center right')
    ax2[0,1].grid(True)

    ax2[1,0].plot(df[0], df[2], label = "Cd")
    ax2[1,0].plot(df[0], df[3], label = "Cd Pressure")
    ax2[1,0].plot(df[0], df[2]-df[3], label = "Skin Drag")
    ax2[1,0].axvline(df[0][np.argmax(df[1])], color = 'black', linestyle = '--', linewidth = 0.75)
    ax2[1,0].set_xlabel('Alpha')
    ax2[1,0].set_ylabel('Cd, Cdp, Skin Drag')
    ax2[1,0].set_title("Cd,Cdp,Skin Drag v/s Alpha")
    ax2[1,0].legend()
    ax2[1,0].grid(True)

    ax2[1,1].plot(df[0],df[5], label = "Upper Separtion Point")
    ax2[1,1].plot(df[0], df[6], label = "Lower Separation Point")
    ax2[1,1].axvline(df[0][np.argmax(df[1])], color = 'black', linestyle = '--',linewidth = 0.75)
    ax2[1,1].set_xlabel('Alpha')
    ax2[1,1].set_ylabel('Upper/Lower Separation Point')
    ax2[1,1].set_title("Upper/Lower Separation Point v/s Alpha")
    ax2[1,1].legend()
    ax2[1,1].grid(True)

    plt.suptitle(f"NACA {code} Polar Data")
    plt.subplots_adjust(hspace = 0.25, wspace = 0.125,left = 0.05, right = 1-0.05, top = 0.9, bottom = 0.075)
    plt.show(block=False)

    fig3 = plt.figure("Cl v/s Cd")
    plt.plot(df[1], df[0])
    plt.title("Cl v/s Cd")
    plt.xlabel("Coefficient of Drag")
    plt.ylabel("Coefficient of Lift")
    
    plt.grid(True)
    plt.show()

def naca00xx(code, chord=1):
    x = np.arange(0, chord, 0.0001)
    t = ((10 * int(code[2])) + int(code[3])) / 100
    yt = [5 * t * (0.2969 * np.sqrt(num) - 0.1260 * num - 0.3516 * (num ** 2) +
                   0.2843 * (num ** 3) - 0.1036 * (num ** 4)) for num in x]
    yu = [-num for num in yt]

    
    fig1 = plt.figure("Airfoil Geometry")
    plt.style.use("ggplot")
    plt.plot(x, yt, label=f"NACA - {code}", color='black', linewidth=1.4)
    plt.plot(x, yu, color='black', linewidth=1.4)
    plt.plot([0, 1], [0, 0], '--', color='black', linewidth=1.25)

    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(-0.5, 0.5)
    
    plt.title(f"NACA - {code} Airfoil Plot")
    plt.grid(True)
    plt.legend()
    plt.show(block=False)
    xfoil_plot(code)

def nacaxxxx(code, chord=1):
    x = np.arange(0, chord, 0.0001)
    t = ((10 * int(code[2])) + int(code[3])) / 100
    m_input = int(code[0])
    p_input = int(code[1])
    m = m_input / 100
    p = p_input / 10

    # Mean camber line
    yc = [(m / (p ** 2)) * (2 * p * num - num ** 2) if num <= p else
          (m / ((1 - p) ** 2)) * ((1 - 2 * p) + 2 * p * num - num ** 2) for num in x]

    # Thickness distribution
    yt = [5 * t * (0.2969 * np.sqrt(num) - 0.1260 * num - 0.3516 * (num ** 2) +
                   0.2843 * (num ** 3) - 0.1036 * (num ** 4)) for num in x]

    dycdx = [((2 * m) / p ** 2) * (p - num) if num <= p else
             (2 * m) / ((1 - p) ** 2) * (p - num) for num in x]
    theta = [np.arctan(dy) for dy in dycdx]

    # Upper and lower surfaces
    xv = [num - yt_i * np.sin(th) for num, yt_i, th in zip(x, yt, theta)]
    yv = [yc_i + yt_i * np.cos(th) for yc_i, yt_i, th in zip(yc, yt, theta)]
    xl = [num + yt_i * np.sin(th) for num, yt_i, th in zip(x, yt, theta)]
    yl = [yc_i - yt_i * np.cos(th) for yc_i, yt_i, th in zip(yc, yt, theta)]

    
    fig1 = plt.figure("Airfoil Geometry")
    plt.plot(x, yc, label='Mean Camber Line', linestyle='--', color='black', linewidth=1.25)
    plt.plot(xv, yv, color='black', label=f'NACA - {code} Upper', linewidth=1.4)
    plt.plot(xl, yl, color='black', label=f'NACA - {code} Lower', linewidth=1.4)
    plt.style.use("ggplot")

    plt.xlabel("x")
    plt.ylabel("y")
    plt.ylim(-0.5, 0.5)

    plt.title(f"NACA - {code} Airfoil Plot")
    plt.grid(True)
    plt.legend()
    plt.show(block=False)
    xfoil_plot(code)

if int(code[0]) == 0 and int(code[1]) == 0:
    naca00xx(code)
else:
    nacaxxxx(code)


plt.show()
