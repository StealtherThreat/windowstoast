import subprocess
import xml.etree.ElementTree as ET, os, time, threading, winreg

def create_protocol(protocol_uri, command_target):
    try:
        reg_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, protocol_uri+"\shell\open\command")
        winreg.SetValue(winreg.HKEY_CLASSES_ROOT, protocol_uri+"\shell\open\command", winreg.REG_SZ, command_target)
        reg_key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, protocol_uri, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(reg_key, 'URL protocol', 0, winreg.REG_SZ, '')
    except Exception as e:
        print(e)

def remove_protocol(protocol_uri):
    try:
        def get_key_list(protocol_uri):
            key_list = []

            def iterate_keys(parent_key, sub_key):
                k=[]
                parent_key = winreg.OpenKey(parent_key, sub_key, 0, winreg.KEY_ALL_ACCESS)
                info = winreg.QueryInfoKey(parent_key)
                if info[0] != 0:
                    for i in range(info[0]):
                        sub_key = winreg.EnumKey(parent_key, i)
                        k.append(parent_key)
                        iterate_keys(parent_key, sub_key)
                    key_list.append(k)

            iterate_keys(winreg.HKEY_CLASSES_ROOT, protocol_uri)
            return key_list

        for each in get_key_list(protocol_uri):
            for every in each:
                winreg.DeleteKey(every, winreg.EnumKey(every, 0))
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, protocol_uri)
    except Exception as e:
        print(e)

class NotificationDispatcher:

    __Dispatcher = None
    __Timeout = 5
    __Toasts = []

    @classmethod
    def add_toast(cls, toast):
        cls.__Toasts.append(toast)
        cls.__Timeout = 5
        if not cls.is_running():
            cls.__start()

    @classmethod
    def is_running(cls):
        try:
            if not cls.__Dispatcher.poll():
                return True
            return False
        except:
            return False


    @classmethod
    def __start(cls):
        command = '''$file = ($PWD).path+'/Toast.ps1'
                    $Previous = 0
                    while(1){
                        if((Test-Path -Path $file -PathType Leaf)){
                            $fileContents = Get-Content $file -raw
                            if(-not(($fileContents).Equals(($Previous)))){
                                .($file)
                                $Previous = $fileContents
                            }
                        }
                        Start-Sleep -s 1
                    }'''
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        cls.__Dispatcher = subprocess.Popen(['powershell','-windowstyle','hidden','-ExecutionPolicy','ByPass',command], startupinfo=startupinfo)
        cls.__timeout()
        cls.__show_toast()
        return 'Started'

    @classmethod
    def __timeout(cls):
        def thread_func(cls):
            while cls.__Timeout!=0:
                cls.__Timeout-=1
                time.sleep(1)
            cls.__stop()
        t = threading.Timer(0, thread_func, [cls])
        t.setDaemon = True
        t.start()

    @classmethod
    def __show_toast(cls):
        def thread_func(cls):
            while cls.is_running():
                if len(cls.__Toasts)>0:
                    with open(os.path.abspath('Toast.ps1'),'w') as f:
                        try:
                            f.write(cls.__Toasts[0])
                        except:
                            pass
                        cls.__Toasts.pop(0)
                time.sleep(1.5)
        t = threading.Timer(0, thread_func, [cls])
        t.setDaemon = True
        t.start()

    @classmethod
    def __stop(cls):
        if cls.is_running():
            cls.__Dispatcher.terminate()
            os.remove(os.path.abspath('Toast.ps1'))
        else:
            print("NotificationDispatcher not running!")

class Toast:

    def __init__(self, App_ID="Application_ID", Notification_ID="", ActivationType="protocol", Duration='short', Launch="file:", Scenario="default", Popup=True):
        self.App_ID = App_ID
        self.Notification_ID = Notification_ID
        self.toast = ET.Element('toast')
        self.toast.set('activationType', ActivationType)
        self.toast.set('duration',Duration)
        self.toast.set('launch',Launch)
        self.toast.set('scenario',Scenario)
        self.Popup = Popup

        self.visual = ET.SubElement(self.toast,'visual',{'branding':'logo'})
        self.binding = ET.SubElement(self.visual,'binding',{'template':'ToastGeneric'})

        self.actions = ET.SubElement(self.toast,'actions')

    def add_button(self, content='Dismiss', arguments='Dismiss', activationType='system'):
        ET.SubElement(self.actions,'action',{'content':content,'arguments':arguments,'activationType':activationType})

    def add_image(self, source, placement=None, hint_crop='circle'):
        source = os.path.abspath(source)
        if placement == "logo" or placement == "appLogoOverride":
            ET.SubElement(self.binding, 'image', {'placement':"appLogoOverride", 'hint-crop':hint_crop, 'src': source})
        else:
            ET.SubElement(self.binding, 'image', {'hint-crop':hint_crop, 'src': source})

    def add_text(self, text=" ", maxlines=None, attribution=False):
        t = None
        if maxlines:
            t = ET.SubElement(self.binding,'text',{'hint-maxlines':str(maxlines)})
        elif attribution:
            t = ET.SubElement(self.binding,'text',{'placement':"attribution"})
        else:
            t = ET.SubElement(self.binding,'text')
        t.text = text

    def add_audio(self, source="", silent=False):
        if silent:
            ET.SubElement(self.toast,'audio',{'silent':"true"})
        elif source != "":
            ET.SubElement(self.toast,'audio',{'src':source})

    def add_progress(self, status, title, value, value_label):
        ET.SubElement(self.binding,'progress',{'status':status, 'title':title, 'value':value, 'valueStringOverride':value_label})

    def add_context_menu(self, content='Context Menu', arguments='Context Menu Argument', activationType='protocol'):
        ET.SubElement(self.actions,'action',{'content':content,'arguments':arguments,'activationType':activationType,'placement':"ContextMenu"})

    def show(self):

        START = '''[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
                [Windows.UI.Notifications.ToastNotification, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
                [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null\n'''

        TAG = '''$tag = "{0}"\n'''.format(self.Notification_ID)

        APP_ID = '''$APP_ID = "{0}"
    
                $template = @"\n'''.format(self.App_ID)

        END = '''\n"@
            $xml = New-Object Windows.Data.Xml.Dom.XmlDocument
            $xml.LoadXml($template)
            $toast = New-Object Windows.UI.Notifications.ToastNotification $xml
            $toast.tag = $tag\n'''

        POPUP = ""
        if not self.Popup:
            POPUP = '''$toast.SuppressPopup = $True\n'''

        SHOW = '''[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($APP_ID).Show($toast)'''

        toast = START  + TAG + APP_ID + ET.tostring(self.toast).decode('utf-8') + END + POPUP + SHOW
        
        NotificationDispatcher.add_toast(toast)

if __name__=="__main__":
    pass