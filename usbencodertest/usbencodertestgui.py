#
## Copyright (c) 2018, Bradley A. Minch
## All rights reserved.
##
## Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are met: 
## 
##     1. Redistributions of source code must retain the above copyright 
##        notice, this list of conditions and the following disclaimer. 
##     2. Redistributions in binary form must reproduce the above copyright 
##        notice, this list of conditions and the following disclaimer in the 
##        documentation and/or other materials provided with the distribution. 
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
## AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
## IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
## ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
## LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
## SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
## INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
## CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
## ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
## POSSIBILITY OF SUCH DAMAGE.
#

import Tkinter as tk
import interface_functions

class usbencodertestgui:

    def __init__(self):
        self.dev = interface_functions.user_functions()
        if self.dev.joystick.dev >= 0:
            self.update_job = None
            self.root = tk.Tk()
            self.root.title('MP2 GUI')
            self.root.protocol('WM_DELETE_WINDOW', self.shut_down)
            fm = tk.Frame(self.root)
            tk.Button(fm, text = 'Virtual Spring', command = lambda: self.dev.change_mode(1)).pack(side = tk.LEFT)
            tk.Button(fm, text = 'Virtual Damper', command = lambda: self.dev.change_mode(2)).pack(side = tk.LEFT)
            tk.Button(fm, text = 'Virtual Texture: Stick', command = lambda: self.dev.change_mode(3)).pack(side = tk.LEFT)
            tk.Button(fm, text = 'Virtual Texture: Slip', command = lambda: self.dev.change_mode(4)).pack(side = tk.LEFT)
            tk.Button(fm, text = 'Virtual Wall', command = lambda: self.dev.change_mode(5)).pack(side = tk.LEFT)
            tk.Button(fm, text = 'RESET ANGLE', command = lambda: self.dev.reset_angle()).pack(side = tk.LEFT)
            dutyslider = tk.Scale(self.root, from_ = -800, to = 0, orient = tk.HORIZONTAL, showvalue = tk.TRUE, command = self.set_lwall_callback)
            dutyslider.set(-800)
            dutyslider.pack(side = tk.TOP)
            dutyslider2 = tk.Scale(self.root, from_ = 0, to = 800, orient = tk.HORIZONTAL, showvalue = tk.TRUE, command = self.set_rwall_callback)
            dutyslider2.set(800)
            dutyslider2.pack(side = tk.TOP)
            fm.pack(side = tk.TOP)
            self.angle_status = tk.Label(self.root, text = 'Angle is currently ?')
            self.angle_status.pack(side = tk.TOP)
            self.lwall_status = tk.Label(self.root, text = 'Left Wall is currently ?')
            self.lwall_status.pack(side = tk.TOP)
            self.rwall_status = tk.Label(self.root, text = 'Right Wall is currently ?')
            self.rwall_status.pack(side = tk.TOP)
            self.mode_status = tk.Label(self.root, text = 'Mode is currently ?')
            self.mode_status.pack(side = tk.TOP)
            self.update_status()
            self.dev.mode = -1

    def set_lwall_callback(self, value):
        self.dev.set_wall_loc_left(int(value))

    def set_rwall_callback(self, value):
        self.dev.set_wall_loc_right(int(value))

    def update_status(self):
        self.angle_status.configure(text = 'Angle is currently {!s}'.format(self.dev.angle))
        self.lwall_status.configure(text = 'Left Wall is currently {!s}'.format(self.dev.wall_loc_left))
        self.rwall_status.configure(text = 'Right Wall is currently {!s}'.format(self.dev.wall_loc_right))
        self.mode_status.configure(text = 'Mode is currently {!s}'.format(self.dev.mode))
        self.dev.run_cycle(self.dev.mode)
        self.update_job = self.root.after(50, self.update_status)

    def shut_down(self):
        self.root.after_cancel(self.update_job)
        self.root.destroy()
        self.dev.joystick.close()

if __name__=='__main__':
    gui = usbencodertestgui()
    gui.root.mainloop()

