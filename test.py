import uiautomation as auto
import time

time.sleep(10)
control = auto.GetFocusedControl()
print("Control:", control)
print("Name:", control.Name)
print("Class:", control.ClassName)
