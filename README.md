### How to structure a Tkinter App using OOP, MVC and a Event Handler

_This is a Work In Progress._

This code probably violates some principles too, but as a learning implementation, I´ll welcome any comments and suggestions to improve it.

Searching for this topic I found a lot of examples, but none of them made me happy.

**Best way to structure tkinter app**
https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application
From this I got that creating a Class for each part of your GUI looks a good call.

https://stackoverflow.com/questions/7638139/how-to-implement-the-mvc-pattern-in-tkinter
https://gist.github.com/ajfigueroa/c2af555630d1db3efb5178ece728b017
https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/
From this stackoverflow question, I followed those links, and found out that:
Those examples are good examples of ‘what not to do’.

**In Resume:**
Sukhbinder puts GUI responsibilities inside the Control Class and Tony C points it in his comment. Indeed, that that violates SRP – Single Responsibility Principle.
Then, Tony C presents his idea of a MVC pattern, where the Model is injected in the View, and Sukhbinder comments that it also violates the SRP because that way, “if the model changes, the view will need to change” too. That creates tight coupling and violates de SRP. “A class should have only and only one reason to change’.

I´m also trying to figure this out myself but searching the web, all I could find is faulty in a way or another.
I have a program that has the classes: GUI_Manager; Model and Controller.
Controller class is a composite that has a GUI_manager instance and a Model Instance.

Controller: Self.view = GUI_Manager()
 		  Self.model = Model()

1. GUI_Manager should not be aware of Controller nor Model Classes;
2. There must be an interface that connects GUI_Manager and Controller so that the events can be passed from one to another.
3. Controller shouldn´t be responsible for using Tkinter.bind to bind events and functions because that scatters tkinter code all over the place.
4. To avoid that, create an Event Handler whose purpose is to bind the GUI events to the Controller.update() function as in an Observer pattern.
5. Call Event_Handler.attach() to attach the Controller Instance to the Event_handler.observers[] list
6. Inject Event_handler Instance into the GUI_manager Instance to make the last one the Observable.
7. It will work like this: The GUI calls the Event_Handler.notify() that will notify the Controller about state changes inside GUI_Manager and call its Controller.update() method;
8. Controller.update() consists of a 'dispatch table ' that binds each event to the methods of the Model Instance or the GUI Instance, creating a circular flow of information


### The Problem of using tkinter binds.

To use bind, the bind code would need to be inserted inside the Controller Class to bind the GUI events to the Model functions, since Controller is the only one who knows about both, but bind is an internal tkinter command and should not be used outside the GUI_Manager Class because that would lead to mixed codes and responsibilities, and responsibility separation and encapsulation is the whole purpose of OOP.

Also, bind is often called inside the Controller __init__ function, but there can be widgets that are instantiated after that, when a user clicks a button, for example, but we cannot bind a button that doesn´t yet exists on the Controller instantiation moment. 

Take a Toplevel for example, user clicks a button and a new Toplevel window is instantiated. This toplevel doesn´t knows about the Model class so you can´t use tkinter.bind also the Controller is already instantiated and you can´t call __init__ again. What would you do then? Use bind to bind the creation of this new Toplevel to run another binding function to bind all of this new Toplevel button/widgets to each of the needed Models functions? If you think this sole sentence looks a mess, imagine this implementation code...

The best approach I could think about is to Inject the Event_Handler.notify() function to the GUI_manager widgets.
If you pass the event_handler as a parameter to the new Toplevel created, you don´t need to worry about it at all, just call notify from within the Toplevel and that´s it. The event handler will take care of the whole notify process.

### Event Handler

1. Create a Event Handler class to work as an Interface for the GUI to access the Controller without the need to know about it.
2. Create a Event_Handler instance.
3. Add the Controller Instance to the observers list inside Event_Handler instance calling the Event_Handler.attach() method and passing the Controller Instance as argument.
4. Inject the Event_Handler.notify() method from the Event_Handler instance onto the GUI_Manager as an argument in the moment of this one´s instantiation.
5. Call GUI_Manager.notify() to notify the Controller about events on the GUI, so Controller.update() method can call the appropriate method of the Model Class.
