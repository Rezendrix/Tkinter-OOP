class Model:
  '''Tkinter OOP/MVC/Event Handler App Model '''
    def check_login(self, ra, tipo_historico):
        print('Model received ra and history type.')
        print(ra, tipo_historico)

    def log_in(self, username, password):
        if username and password:
            print(f'Model Logged the user in! {username} - {password}')

    def do_something(self):
        print('Model did something. Ohhhh!')

    def pos_generated_bind(self):
        print('This function was binded to a button in a class that did not exist on the moment of the Controller was created. Thus, event handler is more flexible than bind.')
