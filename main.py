#!/usr/bin/env python
# -*- coding: utf-8 -*
from gi.repository import Gtk, GdkPixbuf
from config import Config
# import RPi.GPIO as GPIO

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="GPIO MALYNA")
        config = Config()
        conf = config.getConfig()
        config.configureGPIO(conf)
        self.prepareUI(conf)

    def prepareUI(self, conf):
        table = Gtk.Table(13,2,True)
        pinNum = 0

        for pin in conf:
            mainBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            if "direction" in pin:
                if pin["direction"] == "IN":
                    button = Gtk.Button("Get value")
                    button.connect('button-press-event', self.getValue, pin["id"])
                    label = Gtk.Label(pin["label"])
                    box.pack_start(label, False, False, 10)
                    box.pack_start(button, False, False, 10)
                    box.set_border_width(1)
                elif pin["direction"] == "OUT":
                    switch = Gtk.Switch()
                    switch.connect('button-press-event', self.switched, pin["id"])
                    switch.set_active(int(pin["state"]))
                    label = Gtk.Label(pin["label"])
                    box.pack_start(label, False, False, 10)
                    box.pack_start(switch, False, False, 10)
            else:
                label = Gtk.Label(pin["label"])
                box.pack_start(label, False, False, 10)

            f = Gtk.Frame()
            f.set_label(str(pin["id"]))
            f.add(box)
            f.set_border_width(2)
            table.attach(f, self.getColumn(pinNum), self.getColumn(pinNum)+1, self.getRow(pinNum), self.getRow(pinNum)+1)
            pinNum = pinNum + 1
        
        mainBox.pack_start(table, False, False, 10)
        info = Gtk.Button("INFO")
        info.connect('button-press-event', self.showInfo)
        mainBox.pack_end(info, False, False, 10)

        self.add(mainBox)

    def getColumn(self, number):
        if (number+1)%2==0:
            return 1
        else:
            return 0

    def getRow(self, number):
        return int(number/2)

    def switched(self, widget, event, data):
        state = widget.get_active()
        if(state == False):
	  GPIO.output(int(data), GPIO.LOW)
	else:
	  GPIO.output(int(data), GPIO.HIGH)
        

    def getValue(self, widget, event, data):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "GPIO pin "+str(data)+" state")
        dialog.format_secondary_text(
            GPIO.input(data))
        dialog.run()

        dialog.destroy()

    def showInfo(self, widget, event):
        about = Gtk.AboutDialog()
        about.set_program_name("GPIO MALYNA")
        about.set_version("1.0")
        about.set_copyright("(c) Michał Szczesny, Jakub Cegiełka")
        # about.set_logo(GdkPixbuf.Pixbuf.new_from_file("raspberry_pi.png"))
        # about.connect("delete-event", Gtk.main_quit)
        about.run()
        about.destroy()


window = MainWindow()
window.connect("delete-event", Gtk.main_quit)
window.show_all()
Gtk.main()