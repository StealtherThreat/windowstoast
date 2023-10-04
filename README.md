# windowstoast - Python Module for sending Toast Notifications on Windows 10
[![License](https://img.shields.io/github/license/StealtherThreat/WindowsApps)](https://opensource.org/licenses/MIT)

## Installation
To install `windowstoast` from PyPi run:
```shell
pip install windowstoast
```

## Usage

### Create a Toast Notification
```python
from windowstoast import Toast

t = Toast(AppID, NotificationID, ActivationType='protocol', Duration='short', Launch='file:', Scenario='default', Popup=True)
t.show()

#AppID = The application ID from the installed applications in windows. You can get that manually or use my another module 'windowsapps' for that.
#NotificationID = ID you can assign to the notification to identify it later.
#ActivationType = Type of activation for notification. 'system' or 'protocol'.
#Duration = Can be 'short' or 'long'.
#Launch = You can specify your file path to open on notification click, or add your own protocol action.
#Popup = Notification will not pop up if set to false.
```

### Add Text to the Toast Notification
```python
t.add_text(text, maxlines=None, attribution=None)

#text = Your text title(If there is only single text) or message(If there is already other text element present).
#maxlines = No. of lines to be occupied by the text.
#attribution = For attribute text at bottom of toast notification
```
![image](https://user-images.githubusercontent.com/49994038/128413963-c9f05d96-3f36-45e6-abcb-9baa64bd22b0.png)

### Add Image to the Toast Notification
```python
t.add_image(source, placement=None, hint-crop='circle')

#source = Source to the image file
#placement = If specified as 'logo' or 'appLogoOverride' them image will appear as a logo on the left of notification.
#hint-crop = Will make the image circular if specified as 'circle' or squared if specified 'square'.
```
![image](https://user-images.githubusercontent.com/49994038/128415426-0da860da-ecb3-4aff-9a01-7fa0522df4f5.png)
![image](https://user-images.githubusercontent.com/49994038/128415545-b8218d3d-41ab-467d-9f30-0bfa8da58920.png)

### Add Custom audio to the Toast Notification
```python
t.add_audio(source="", silent=False)

#source = Source for the audio file.
#silent = Will make the notification appear silently if set True.
```

### Add Progress Bar to the Toast Notification
```python
t.add_progress(status, title, value, value_label)

#status = Text below the progress bar indicatiing its current state. Ex- 'Downloading...', 'Receiving...', etc.
#title = Title about the progress bar.
#value = A value between 0 and 1 for the progress.
#value_label = A text below the progress bar showing the current progress to the user. Ex- '26/100 Completed!', '54%', etc.
```
![image](https://user-images.githubusercontent.com/49994038/128417618-17b352e9-056b-4e55-8f45-a271e7b34b6a.png)

### Add Context Menu to the Toast Notification
```python
t.add_content_menu(content, arguments, activationType='protocol')

#content = Name for the context menu.
#argument = Specific argument for the menu.
#activationType = 'protocol' for a protocol activation in windows.
```
![image](https://user-images.githubusercontent.com/49994038/128418623-ea560273-62e7-4390-8458-6daa9eb11336.png)

### Add Button to the Toast Notification
```python
t.add_button(content='Dismiss', argument='Dismiss', activationType='system')

#content = Name for the button.
#argument = Argument specified for the button.
#activationType = Can be specified as 'system' for just dissmisal of notification on button click or set as 'protocol' to launch your custom protocol.

#You can add maximum of 5 buttons.
```
![image](https://user-images.githubusercontent.com/49994038/128419467-5cc5296c-8ec2-4f88-9d42-773e50e29d2e.png)

### Launch Custom Action on Button Click
```python

# First create your own protocol in the windows registry by:
import windowstoast

create_protocol(protocol_uri, comman_target) # Run as Admin required for this!

#protocol_uri = Your own unique protocol uri name. Ex- 'My-Custom-Uri'
#command_target = Path to your own target application with arguments. Ex- r'"Absoulute\Path\To\My\Application.exe" "%1"'

# If you want to remove your protocol:

remove_protocol('Protocol_name') # Run as Admin required for this!

#Create your own Application.exe which takes the argument. Ex- 
from sys import argv

a = argv[1:]
print(a)

# Here a is the value of argument that you will specify with the button in Notification.

#Now after making sure you have created your protocol and Application.exe, add button in the notification

t.add_button('My Button','My-Custom-Uri:My_Argument', 'protocol')

# Here you can specify your own protocol uri to execute an action or some other uri like - 'E:\Others\my_file.xyz' to open a file or 'https://www.google.com' to open website.
```

### Update Your Notification
```python

notificationID = '12345'

t = Toast('My Application ID', notificationID)
t.add_text('Title')
t.add_progress('Status...', 'Progress Title', '0', '0% Completed!')
t.show()

# To update the notification, simply create another notification with same notification id.

for i in range(10):
  t = Toast('My Application ID', notificationID, Popup=False) # Set Popup to False whenever you update, otherwise notification will popup each time.
  t.add_audio(silent=True) # Set silent to True whenever you update, otherwise audio will play each time.
  t.add_text('Title')
  t.add_progress('Status...', 'Progress Title', str(i/10), str(i)+'% Completed!')
  t.show()
  
# It is recommended to update notification only after atleast 1.5 seconds.
