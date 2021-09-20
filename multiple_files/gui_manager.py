'''
Classes to manage a Tkinter GUI program

Best way to structure tkinter app
https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

Pass arguments to a tkinter button 
https://stackoverflow.com/questions/6920302/how-to-pass-arguments-to-a-button-command-in-tkinter
'''
from enum import IntEnum, auto
import tkinter as tk
from tkinter import ttk


# to open non gif images
#from PIL import ImageTk

class StatusCode(IntEnum):
    ''' Codes passed as parameters to the function notify(status_code : StatusCode)
    So it calls the respective method on the Controler.update() function.'''
    CLOSE_BROWSER_DRIVER = auto()
    CHECK_LOGIN = auto()
    LOG_IN = auto()
    DUMMY_TEST = auto()
    DO_SOMETHING = auto()
    POS_GENERATED_BIND = auto()


program_version = 'Alpha 0.0'

class GUI_Event_Handler:
    '''Sends Events to the Controller'''
    # observers/subscribers list
    observers = []

    def attach_observer(self, observer):
        '''Adds a observer.'''
        self.observers.append(observer)
        return


    def detach_observer(self, observer):
        '''Removes a observer '''
        self.observers.remove(observer)
        return


    def notify(self, status_code : StatusCode, *args, **kwargs):
        '''### Descrição
        Notifies the observers/subscribers about states changes inside GUI_Manager
        calling the function update() on each observer

        ### Param
        @status_code : int -- Event Status_Code
        '''
        for observer in self.observers:
            observer.update(status_code, *args, **kwargs)
        return



class GUI_Manager:
    ''' Manages Every GUI related classes. Each widget is a different class

    ### OBS
    The Event_Hander is injected by dependency injection
    '''
    def __init__(self, master : tk.Tk, event_handler):
        self.master = master
        ''' Classes '''
        self.notify = event_handler
        self.menu = Menu(self)
        #self.main = Main(self)
        self.login = Login(self)
        self.login_status = LoginStatus(self.master)
        self.status_bar = StatusBar(self.master)
        self.notebook = Notebook(self.master, self.notify)

        ''' Icon '''
        icon = tk.PhotoImage(file = 'file.gif')
        self.master.iconphoto(False, icon)

        ''' Master Configs '''
        #self.master.state('zoomed')
        self.master.minsize(500, 450)
        self.master.title('Tkinter MVC + Event Handler')
        self.master.config(menu=self.menu.menubar)
        self.master.protocol("WM_DELETE_WINDOW", self.close_program)

        self.button_exit = tk.Button(self.master, text='Exit', command=self.close_program)
        self.configure_grid()



    def configure_grid(self):
        self.master.grid_columnconfigure(0, weight=0)
        self.master.grid_columnconfigure(1, weight=1)
        self.master.grid_columnconfigure(2, weight=0)
        self.button_exit.grid(row = 5, column = 1, padx=5, pady=5)
        self.master.grid()

    def close_program(self):
        '''Notifies observers about program closing so they can end their processes.'''
        self.notify(StatusCode.CLOSE_BROWSER_DRIVER, 'Dummy Object Notificado - CLOSE_BROWSER_DRIVER.')
        self.master.quit()
        return


class Notebook:
    def __init__(self, master : tk.Tk, notifier : GUI_Event_Handler):
        self.master = master
        self.notify = notifier
        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=1, column=0, columnspan=3, sticky=(tk.N,tk.S,tk.E,tk.W))
        self.create_tabs()
        self.add_tabs()

        self.master.bind("<Configure>", self.conf)


    # IMPORTANT: Do not erase the 'event' param or the function 
    # won´t work even tho 'event' is not being used here.
    def conf(self, event):
        ''' Sets Notebook´s height and width equals to the window´s.'''
        self.notebook.config(height=self.master.winfo_height() -150,width=self.master.winfo_width()-145)


    def create_tabs(self):
        '''Creates notebook´s tabs.'''
        self.tab1 = Tab1(self.notebook, self.notify)
        self.tab2 = Tab2(self.notebook, self.notify)
        
    def add_tabs(self):
        '''Adds tabs to the notebook.'''
        self.notebook.add(self.tab1, text='TAB 1')
        self.notebook.add(self.tab2, text='TAB 2')


class Tab1(ttk.Frame):
    '''Notebook Tab 1'''
    def __init__(self, master, notifier, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.notify = notifier
        self.label = ttk.Label(self, text='TAB 1', style='Heading.TLabel')
        self.button_notify = ttk.Button(self, text = 'Notify', width = 25, command = lambda : self.notify(StatusCode.DUMMY_TEST, 'Dummy Test Called'))
        self.button_destroy = ttk.Button(self, text = 'Close TAB', width = 25, command = lambda : self.destroy())
        self.configure_styles()
        self.configure_grid()


    def configure_grid(self):
        '''Grid'''
        self.grid_columnconfigure(1, weight=0)
        self.label.grid(row=0, column=1)
        self.button_notify.grid(row = 1, column = 0)
        self.button_destroy.grid(row = 2, column = 0)

    def configure_styles(self):
        '''style sheet'''
        self.style = ttk.Style(self)
        self.style.configure('Heading.TLabel', font=('Helvetica', 12), background='#ffffff')
        self.style.configure('TFrame', background='#ffffff')


class Tab2(ttk.Frame):
    '''Notebook Tab 2'''
    def __init__(self, master, notifier=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.notify = notifier
        self.button_notify = ttk.Button(self, text = 'Do Something', width = 25, command = lambda : self.notify(StatusCode.DO_SOMETHING))
        self.image = tk.PhotoImage(file='file.gif')
        self.button_new_window = tk.Button(self, text = 'Open New Window', width = 25, command = lambda: NewWindow2(self.master, notifier = self.notify))
        self.button_window_historico = tk.Button(self, image = self.image, text = 'History', compound= tk.TOP, command = lambda : Window_Historico(self.master, notifier=self.notify))

        self.configure_grid()
        self.configure_styles()

        # Caso um notifier não seja passado para a função
        if self.notify == None:
            print(f'No notifier arg passed on creation: {type(self)}. Event_Handler.notify')


    def configure_grid(self):
        '''Grid'''
        self.button_new_window.grid(row = 0, column = 0, padx=5, pady=5)
        self.button_notify.grid(row = 1, column = 0)
        self.button_window_historico.grid(row = 2, column = 0, padx=5, pady=5)


    def configure_styles(self):
        '''Style sheet'''
        self.style = ttk.Style(self)
        self.style.configure('Heading.TLabel', font=('Helvetica', 12), background='#ffffff')
        self.style.configure('TFrame', background='#ffffff')
    

"""
class Main:
    '''### Descrição
    Responsible for the main part of the interface
    '''
    def __init__(self, parent):
        self.master = parent.master
        self.notify = parent.notify
        self.frame = tk.Frame(self.master, bg = '#eeffff', pady = 10)
        self.image = tk.PhotoImage(file='file.gif')
        self.button_new_window = tk.Button(self.frame, text = 'Open New Window', width = 25, command = lambda: NewWindow2(self.master, notifier = self.notify))
        self.button_window_historico = tk.Button(self.frame, image = self.image, text = 'Históricos', compound= tk.TOP, command = lambda : Window_Historico(self.master, notifier=self.notify))

        self.frame.grid(row = 1, column = 0, padx=5, pady=5)
        self.button_new_window.grid(row = 0, column = 0, padx=5, pady=5)
        self.button_window_historico.grid(row = 1, column = 0, padx=5, pady=5)

        ''' Dummy button to test bind.'''
        self.button_dummy_bind = tk.Button(self.master, text="Dummy Bind")
        self.button_dummy_bind.grid(row = 5, column = 1, padx=5, pady=5)

        ''' Dummy button to test notify.'''
        self.button_dummy_notification = tk.Button(self.master, text="Dummy notification", command= lambda : self.notify(69))
        self.button_dummy_notification.grid(row = 6, column = 1, padx=5, pady=5)

        '''Dummy button to test new window opening.'''
        self.button_teste = tk.Button(self.master, text="teste", command = lambda : Window_Historico(self.master, notifier=self.notify))
        self.button_teste.grid(row =7, column = 1, padx=5, pady=5)
"""
"""
    # https://www.smashingmagazine.com/2020/12/practical-introduction-dependency-injection/
    def open_new_window(self, window_class, event_notifier = None):
        '''### Descrição
        Abre uma nova janela.
        
        ### Injeção Dependência
        É feita a Injeção de dependência, assim, fica fácil definir qual
        janela será aberta passando a Window_Class diretamente como argumento
        para a função chamada pelo command no botão.

        ### Inversão de controle
        Antes, o corpo da função definia qual Window_Class seria criada, criando
        acoplamento. Para mudar a Window_Class teria que se alterar a assinatura da função.
        Agora, para mudar a Window_Class, basta mudar o argumento passado quando
        a função for chamada.

        @app : Window_Class -- A Classe da janela a ser exibida.
        '''
        self.toplevel = tk.Toplevel(self.master)
        self.new_window = window_class(self.toplevel, event_notifier)
    """


class NewWindow2(tk.Toplevel):
    def __init__(self, master = None, notifier = None):
        self.notify = notifier
        super().__init__(master = master)
        self.frame = tk.Frame(self)
        self.button_notify = tk.Button(self.frame, text = 'Notify', width = 25, command = lambda : self.notify(StatusCode.POS_GENERATED_BIND))
        self.button_close = tk.Button(self.frame, text = 'Close', width = 25, command = self.destroy)

        self.frame.grid(row = 0, column = 0)
        self.button_notify.grid(row = 1, column = 0)
        self.button_close.grid(row = 2, column = 0)

        if self.notify == None:
            print(f'No notifier arg passed on creation: {type(self)}. Event_Handler.notify')


class Window_Historico(tk.Toplevel):
    def __init__(self, master = None, notifier = None):
        self.notify = notifier
        super().__init__(master = master)
        self.title('History')
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid()

        self.tipo_historico = tk.IntVar(None, 2)
        self.radio_concluinte = tk.Radiobutton(self.frame, text='Finished', variable = self.tipo_historico, value = 1, command=self.select)
        self.radio_transferencia = tk.Radiobutton(self.frame, text='Transference', variable = self.tipo_historico, value = 2, command=self.select)
        self.label_selection = tk.Label(self.frame, text = 'Status: ')
        self.label_title = tk.Label(self.frame, text="Insert the ID to do the thing:")
        self.stringvar1 = tk.StringVar(self.frame)
        self.stringvar1.trace("w", self.validate_entry_ra)
        self.entry_ra = tk.Entry(self.frame, textvariable=self.stringvar1, width=15)
        self.button_check_login = tk.Button(self.frame, text='Do the thing:', width = 25, state='disabled', command = lambda: self.notify(StatusCode.CHECK_LOGIN, ra=self.get_ra(), tipo_historico = self.tipo_historico.get()))
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.destroy)

        self.label_title.grid(row = 0, column = 0, columnspan=2)
        self.radio_concluinte.grid(row=1, column=0, columnspan=2)
        self.radio_transferencia.grid(row=2, column=0)
        self.label_selection.grid(row=3, column=0)
        self.entry_ra.grid(row=4, column=0)
        self.button_check_login.grid(row=5, column=0, columnspan=2, sticky='ew')
        self.quitButton.grid(row=6, column=0, columnspan=2, sticky='ew')


    def select(self):
        selection = "Status: You selected" + str(self.tipo_historico.get())
        self.label_selection.config(text = selection)


    def validate_entry_ra(self, *args):
        '''
        ### Descrição
        Habilita o botão de login se a quantidade de caracteres no campo 
        de RA corresponde à quantidade de caracteres presentes em um RA.

        ### OBS
        O método StringVar.trace() dispara um evento toda vez que há alteração
        no campo tk.Entry() ao qual ele está vinculado e chama validate_entry_ra()
        a cada evento disparado.
        '''
        if len(self.stringvar1.get()) >= 7:
            self.button_check_login['state'] = 'normal'
        else:
            self.button_check_login['state'] = 'disabled'

    def get_ra(self):
        return self.entry_ra.get()


class About:
    '''### Descrição
    Class responsible for About Window.
    '''
    def __init__(self, master):
        self.master = master
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=0)

        self.program_name = tk.Label(self.master, text='Tkinter MVC - Event Handler Example.')
        self.version = tk.Label(self.master, text=f"Version: {program_version}")
        self.button_close = tk.Button(self.master, text = 'Close', command = self.master.destroy)

        self.program_name.grid(row = 0, column = 0)
        self.version.grid(row = 1, column = 0)
        self.button_close.grid(row = 2, column = 0)


class Login:
    '''### Descrição
    Responsible for Login User Interface - UI.
    '''
    def __init__(self, parent):
        self.master = parent.master
        self.notify = parent.notify

        self.login_button1 = tk.Button(self.master, text='Login', command = self.display_login_window)
        self.user_logged = tk.Label(self.master, text = "Offline", fg='#ff0000')

        self.login_button1.grid(row = 0, column = 2)
        self.user_logged.grid(row = 0, column = 1)

    login = None
    password = None

    def get_login(self):
        return self.login


    def get_password(self):
        return self.password


    def close_login_window(self):
        ''' Closes the login Window(tk.Toplevel).'''
        self.login_window.destroy()


    def display_login_window(self):
        '''Opens Login Window(tk.Toplevel)'''
        self.login_window = tk.Toplevel(self.master)
        self.label_nao_logado = tk.Label(self.login_window, text="Not logged in.")

        self.label_usuario = tk.Label(self.login_window, text="User:", pady=5)
        self.entry_username = tk.Entry(self.login_window, textvariable=self.login, width=15)

        self.label_password = tk.Label(self.login_window, text="password:")
        self.entry_password = tk.Entry(self.login_window, textvariable=self.password, show="*", width=15)

        self.button_enviar = tk.Button(self.login_window, text='Submit', command=self.set_login_credentials)

        # O método bind envia um event como parâmetro para a função passada como 2º argumento
        # porém, nossa função não faz uso desse parâmetro, por isso a chamamos com
        # a lambda, para não passar o parâmetro desnecessário à função.
        self.entry_password.bind('<Return>', lambda x:self.set_login_credentials())

        self.label_error_message = tk.Label(self.login_window, fg='#ff0000', text="")
    
        self.quitButton = tk.Button(self.login_window, text = 'Sair', pady=5, width = 25, command = self.close_login_window)

        self.label_nao_logado.grid(row=0, column=0, columnspan=2)
        self.label_usuario.grid(row=1, column=0)
        self.entry_username.grid(row=1, column=1)
        self.label_password.grid(row=2, column=0)
        self.entry_password.grid(row=2, column=1)
        self.label_error_message.grid(row=3, column=0, columnspan=2)
        self.button_enviar.grid(row=4, column=0, columnspan=2, sticky='ew')
        self.quitButton.grid(row=5, column=0, columnspan=2, sticky='ew')

        self.login_window.grid_columnconfigure(0, weight=1)
        self.login_window.grid_columnconfigure(1, weight=1)


    def set_login_credentials(self):
        ''' Stores login and password '''
        #self.login = self.entry_username.get()
        #self.password = self.entry_password.get()

        if not self.entry_username.get() or not self.entry_password.get():
            self.label_error_message['text'] = 'Insert username and password'
        else:
            self.label_error_message['text'] = ''
            self.notify(StatusCode.LOG_IN, self.entry_password.get(), self.entry_password.get())
            self.login_window.destroy()


class LoginStatus:
    def __init__(self, master) -> None:
        self.master = master
        self.label_usuario_logado = tk.Label(self.master, text = 'Not logged in', fg='#ff0000')
        self.label_usuario_logado.grid(row = 0, column = 1)


    def update_login_status(self, nome_usuario):
        self.label_usuario_logado['text'] = f'Logged in as : \n{nome_usuario}'
        self.label_usuario_logado['fg'] = '#0000ff'


class Menu:
    def __init__(self, parent):
        self.master = parent.master
        self.menubar = tk.Menu(self.master)

        # FILE MENU
        self.filemenu = tk.Menu(self.menubar, tearoff=0)

        self.filemenu.add_command(label='Back', command=self.display_about)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit', command=self.master.quit)

        self.menubar.add_cascade(label='File', menu=self.filemenu)

        # HELP MENU
        self.helpmenu = tk.Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='About', command=self.display_about)

        self.menubar.add_cascade(label='Help', menu=self.helpmenu)


    def display_about(self):
        '''Opens About Window(tk.Toplevel).'''
        self.about_window = tk.Toplevel(self.master)
        self.about_window.geometry("%dx%d%+d%+d" % (200,200,0,0))
        self.app = About(self.about_window)


class StatusBar():
    def __init__(self, master):
        self.master = master
        self.label_status = tk.Label(self.master, anchor="w", text='Status: ', font=("Arial", 12), bg='#002299', fg='#ffffff',)
        
        ''' Dummy button to test update_label_status() function '''
        # self.button_update_label_status = tk.Button(self.master, text = 'Update Status', width = 25, command = partial(self.update_label_status, text='Status: Atualizei'))
        # self.button_update_label_status.pack()

        self.label_status.place(relx=.5, rely=1.0, relwidth=1.0, anchor='s')


    def update_label_status(self, text='Did you forgot to pass the status message?'):
        '''### Descrição
        Changes Status_Bar text on UI.

        ### Param
        @text : str -- Text to display.
        '''
        self.label_status['text'] = text
