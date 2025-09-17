import tkinter as tk
import subprocess
from tkinter import ttk

def run_command(command):
    # Run command and return output as list
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result.stdout.strip().split('\n')

def setBright():
	# ~ print("will set brightness by calling xrandr")
		
	slidervalue=slider.get()
	#calculate brightness for slidervalue > 40
	if (slidervalue >= 40):
		# ~ print(slidervalue)
		newBrightness = 1 + (slidervalue - 40)/20 
	#calculate brightness for slidervalue < 40 ; finer grained 
	elif (slidervalue < 40):
		newBrightness = 1 - (40 - slidervalue)/40
		
	#run command for every connected device
	for device in deviceList:
		#xrandr --output HDMI-1 --brightness 0.
		run_command(f"xrandr --output {device} --brightness {newBrightness}")
		# ~ print(newBrightness)

	# ~ print(slider.get())
	root.after(500, setBright)

# ~ def on_slider_change(value):
    # ~ print(f"Schiebereglerwert: {value}")

def on_help_button_click():
    print("This software changes brightness of graphical output by sliding the slider. Backends are xrandr, grep etc.")

def on_close_button_click():
    print("Goodebye-Signal detected!")
    root.destroy()

def on_plus_button_click():
    # Neues Fenster erstellen
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    # Label erstellen
    label = tk.Label(settings_window, text="Settings", font=("Helvetica", 16, "bold", "italic"))
    label.pack(pady=10)

    # Dropdown-Menü erstellen
    dropdown_var = tk.StringVar()
    dropdown = ttk.Combobox(settings_window, textvariable=dropdown_var)
    dropdown['values'] = ["Option 1", "Option 2", "Option 3"]  # Dummy-Werte
    dropdown.pack(pady=10)
    dropdown.bind("<<ComboboxSelected>>", on_dropdown_change)

    # Eingabefeld mit Label
    entry_label1 = tk.Label(settings_window, text="Eingabe 1:")
    entry_label1.pack(pady=5)
    entry1 = tk.Entry(settings_window)
    entry1.pack(pady=5)

    # Checkbox
    checkbox_var = tk.BooleanVar()
    checkbox = tk.Checkbutton(settings_window, text="Checkbox", variable=checkbox_var, command=on_checkbox_change)
    checkbox.pack(pady=10)

    # Eingabefeld mit Label
    entry_label2 = tk.Label(settings_window, text="Eingabe 2:")
    entry_label2.pack(pady=5)
    entry2 = tk.Entry(settings_window)
    entry2.pack(pady=5)

    # Zwei Buttons nebeneinander
    button1 = tk.Button(settings_window, text="Button 1", command=on_button1_click)
    button1.pack(side=tk.LEFT, padx=5, pady=10)
    button2 = tk.Button(settings_window, text="Button 2", command=on_button2_click)
    button2.pack(side=tk.LEFT, padx=5, pady=10)

    # Eingabefeld mit Label
    entry_label3 = tk.Label(settings_window, text="Eingabe 3:")
    entry_label3.pack(pady=5)
    entry3 = tk.Entry(settings_window)
    entry3.pack(pady=5)

    # Zwei Buttons nebeneinander
    button3 = tk.Button(settings_window, text="Button 3", command=on_button3_click)
    button3.pack(side=tk.LEFT, padx=5, pady=10)
    button4 = tk.Button(settings_window, text="Button 4", command=on_button4_click)
    button4.pack(side=tk.LEFT, padx=5, pady=10)

def on_dropdown_change(event):
    print("Dropdown-Auswahl geändert!")

def on_checkbox_change():
    print("Checkbox-Zustand geändert!")

def on_button1_click():
    print("Button 1 geklickt!")

def on_button2_click():
    print("Button 2 geklickt!")

def on_button3_click():
    print("Button 3 geklickt!")

def on_button4_click():
    print("Button 4 geklickt!")

# Hauptfenster erstellen
root = tk.Tk()
root.title("Enlighter")

# X-Button erstellen
close_button = tk.Button(root, text="X", command=on_close_button_click, fg="red", font=("Helvetica", 16, "bold"), width=2)
close_button.pack(side=tk.TOP, pady=5)

# Schieberegler erstellen
slider = tk.Scale(root, from_=80, to=0, orient=tk.VERTICAL, length=300, showvalue=False) #command=on_slider_change,
slider.set(40)  # Standardwert auf 40 setzen
slider.pack(pady=10)

# X-Button erstellen
close_button2 = tk.Button(root, text="X", command=on_close_button_click, fg="red", font=("Helvetica", 16, "bold"), width=2)
close_button2.pack(side=tk.TOP, pady=5)

# Hilfe-Button erstellen
help_button = tk.Button(root, text="?", command=on_help_button_click, fg="blue", width=2)
# ~ help_button.pack(side=tk.TOP, pady=5)

# Plus-Button erstellen
plus_button = tk.Button(root, text="+", command=on_plus_button_click, fg="green", width=2)
# ~ plus_button.pack(side=tk.BOTTOM, pady=5)

# xrandr --verbose | grep -i bright
brightnList = run_command("xrandr --verbose | grep -i bright | cut -f2 -d' '")
# xrandr | egrep "\bconnected" | cut -f1 -d" "
deviceList = run_command("xrandr | egrep '\\bconnected' | cut -f1 -d' '")

print("Devices connected:")
for value in deviceList:
	print(value)
	
print("Brightnesses is as follows:")
for brightness in brightnList:
	print(brightness)
	
	#calculate slider position for brightness > 1.0
	if (float(brightness) >= 1.0):
		sliderpos = 40 + round( (float(brightness) - 1)*20 )
		# ~ print(sliderpos)
		
	#calculate slider position for brightness < 1.0
	elif (float(brightness) < 1.0):
		sliderpos = round( ( float(brightness) ) * 40 )
		# ~ print(sliderpos)
		
slider.set(sliderpos)		
	
setBright() #start time-loop

# start main loop
root.mainloop()
