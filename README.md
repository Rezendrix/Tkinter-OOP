### How to structure a Tkinter App using OOP, MVC and a Event Handler

_This is a Work In Progress._

This code probably violates some principles too, but as a learning implementation, I´ll welcome any comments and suggestions to improve it.

---

Trying to figure this out myself, all I could find is faulty in a way or another. But maybe I´ve got to something. 

As all MVC let´s create three classes to represent the Model, View and Controller. In our case, we´ll call it: Model, GUI_Manager and Controller.

The Controller Class is a composite that has a GUI_Manager instance and a Model Instance.

Controller: 
1. self.view = GUI_Manager()
2. self.model = Model()

---
There are a few rules we´ll follow to structure this Tkinter App:
1. **GUI_Manager** should not be aware of **Controller** nor **Model Classes**.
2. There must be an interface that connects **GUI_Manager** and **Controller** so that the events can be passed from one to another.
3. **Controller** shouldn´t be responsible for using **Tkinter.bind()** to bind events and functions because that scatters tkinter code all over the place.
4. To avoid that, let´s create an **Event Handler Class** whose purpose is to bind the **GUI events** to the **Controller.update()** method as in an **Observer Pattern**.
5. **Controller.update()** will consist of a **Dispatch Table** that binds each **GUI event** to the methods of the **Model Instance** or the **GUI Instance**, creating a circular flow of information.

**How to do it**
1. Call **Event_Handler.attach()** to attach the **Controller Instance** to the **Event_handler.observers[]** list.
2. **Inject Event_handler Instance** into the **GUI_manager Instance** to make this last one the **Observable/Subject** of the **Observer Patter**.
3. It will work like this: The **GUI** calls the **Event_Handler.notify()** that will notify the **Controller** about state changes inside **GUI_Manager** and call its **Controller.update()** method.

### Event Handler

1. Create an **Event Handler Class** to work as an Interface for the **GUI** to access the **Controller** without the need to know about it.
2. Create an **Event_Handler instance**.
3. Add the **Controller Instance** to the observers list inside **Event_Handler instance** calling the **Event_Handler.attach()** method and passing the **Controller Instance** as argument.
4. **Inject** the **Event_Handler.notify()** method from the **Event_Handler instance** onto the **GUI_Manager instance** as an argument in the moment of this one´s instantiation.
5. Call **GUI_Manager.notify()** to notify the **Controller** about events on the **GUI**, so **Controller.update()** method can call the appropriate method of the **Model Class**.

---

### Search History:

Searching for the best way to structure a Tkinter App, I found a lot of examples, but none of them made me happy.

**Best way to structure tkinter app:**
https://stackoverflow.com/questions/17466561/best-way-to-structure-a-tkinter-application

1. From this I got that **creating a Class** for each part of your GUI looks like a good call. 
2. But how do you bind the GUI Events to the Model methods?

---

**How to implement mvc pattern in tkinter:**
https://stackoverflow.com/questions/7638139/how-to-implement-the-mvc-pattern-in-tkinter
1. https://gist.github.com/ajfigueroa/c2af555630d1db3efb5178ece728b017
2. https://sukhbinder.wordpress.com/2014/12/25/an-example-of-model-view-controller-design-pattern-with-tkinter-python/

From this stackoverflow question, I followed those links but IMO: Those are good examples of ‘what not to do’.

---
**In Resume:**
The author of the post: Sukhbinder puts GUI responsibilities inside the Control Class and a user called Tony C points that in his comment. 
Indeed, that that violates SRP – Single Responsibility Principle.

### The Problem of using tkinter binds.

To use bind, the bind code would need to be inserted inside the **Controller Class** to bind the **GUI events** to the **Model methods**, since **Controller** is the only one who knows about both, but **bind()** is an internal tkinter command and should not be used outside the **GUI_Manager Class** because that would lead to mixed codes and responsibilities, and responsibility separation and encapsulation is the whole purpose of OOP.

Also, bind is often called inside the **Controller __init__ method**, but there can be widgets that are instantiated **after** the initiation of the **Controller**, when a user clicks a button, for example, but we cannot bind a button that doesn´t yet exists on the **Controller instantiation** moment. 

Take a **tk.Toplevel()** for example: The user clicks a button and a new Toplevel window is instantiated. This toplevel doesn´t knows about the **Model Class** so you can´t use **tkinter.bind()** also the **Controller** is already instantiated and you can´t call __init__ again. What would you do then? 

Use bind to bind the creation of this new Toplevel to run another binding function to bind all this new Toplevel button/widgets to each of the needed Models functions? If you think this sole sentence looks a mess, imagine this implementation code...

The best approach I could think about is to Inject the **Event_Handler.notify()** function to the **GUI_manager** widgets.
If you pass the event_handler as a parameter to the new Toplevel created, you don´t need to worry about it at all, just call notify from within the Toplevel and that´s it. The event handler will take care of the whole notify process.

### Model Injection inside View

Then, Tony C presents his idea of a MVC pattern, where the Model is injected into the View, and Sukhbinder comments that it also violates the SRP because that way, “if the model changes, the view will need to change” too. 

Indeed, that creates tight coupling and violates de SRP. “A class should have only and only one reason to change’.

but I´m not totally sure about that in this context. It seems kind of impossible to create new functionality in a program Model without doing anything to adjust the GUI, unless the new functions are inserted inside older Model functions. 

Let´s say you have an app that displays the user´s friends list, if you create a function for the user add new friends you need to include a field on the interface for the name input and a ‘submit’ button. It´s useless to add a ‘add_friend()’ method to the Model and do nothing on the GUI so the user can actually use the new method, so…
