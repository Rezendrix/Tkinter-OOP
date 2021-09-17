### How to structure a Tkinter App using OOP, MVC and a Event Handler

_This is a Work In Progress._ 

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

I´m also trying to figure this out myself but searching the web all I could find is faulty in a way or another.
I have a program that has the classes: GUI_Manager; Model; Controller.
Controller class is a composite that has a GUI_manager instance and a Model Instance.

Controller: Self.view = GUI_Manager()
 		  Self.model = Model()

1. GUI_Manager should not be aware of Controller nor Model Classes;
2. There must be an interface that connects GUI_Manager and Controller so that the events can be passed from one to another.
3. Controller shouldn´t be responsible for doing the events/functions bindings.
4. So, create an Event Handler whose purpose is to bind the GUI events to the Controller.update() function as in an Observer pattern. The GUI calls the Event_handler that notifies the Controller about state changes inside GUI_Manager and calls its update method; So, the Controller is attach as Observer and Event_handler is injected into the GUI_manager Instance making it the Observable.


### The Problem of using tkinter binds.

To use bind, the bind code would need to be inserted inside the Controller Class to bind the GUI events to the Model functions, since Controller is the only one who knows about both, but bind is an internal tkinter command and should not be used outside the GUI_Manager class because that would lead to mixed codes and responsibilities, and responsibility separation and encapsulation is the whole purpose of OOP.

Also, bind is often called inside the Controller __init__ function, but there can be widgets that are instantiated after that, when a user clicks a button, for example, but we cannot bind a button that doesn´t yet exists on the Controller instantiation moment. 

Take a Toplevel for example, user clicks a button and a new Toplevel window is instantiated. This toplevel doesn´t knows about the Model class so you can´t use tkinter.bind and the Controller is already instantiated, and you can´t call init again too. What would you do then? Use bind to bind the creation of this new Toplevel to run another binding function to bind all of this new Toplevel button/widgets to each of the needed Models functions?

The best approach I could think about is to pass the event_handler.notify() function around the GUI_manager widgets. 
If you pass the event_handler as a parameter to the new Toplevel created, you don´t need to worry about it at all, just call notify from within the Toplevel and that´s it.

### Event Handler

1. Create a Event Handler class to work as an Interface for the GUI have acess to the Controller without the need to know about it.
2. Create a Event_Handler instance.
3. Add Controller to the observers list inside Event_Handler instance.
4. Inject the Event_Handler.notify() method from the instance onto the GUI_Manager in the moment of this one´s instantiation.
5. Call GUI_Manager.notify() to notify the Controller about events on the GUI, so Controller can call the appropriate method of the Model Class.
