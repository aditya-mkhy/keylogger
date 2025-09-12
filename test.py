import uiautomation as auto
import time
control = auto.GetFocusedControl()

print("Control:", control)
print("Name:", control.Name)
print("Class:", control.ClassName)
