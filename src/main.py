import os
import constants
import tkinter as tk
import threading
from tkinter import messagebox

from StockX import StockX


class Root(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('StockX Auto-bidder')
        # self.sx_loop_thread = None

        self.should_quit = True

        self.initialize_credentials_form()
        self.initialize_url_input()
        self.initialize_headless_cbox()
        self.initialize_restrict_cbox()
        self.initialize_restrict_input()
        self.initialize_status()
        self.initialize_buttons()

        self.protocol("WM_DELETE_WINDOW", self.safe_destroy)

    # def __del__(self):
    #     print('Deleting')
    #     # del self.sx_loop_thread
    #     del self.sx

    def can_quit_now(self):
        self.should_quit = True

    def safe_destroy(self):
        if hasattr(self, "sx"):
            self.sx.force_quit = True
            self.after(100, self.safe_destroy)
        elif not self.should_quit:
            self.after(100, self.safe_destroy)
        else:
            self.destroy()

    def initialize_credentials_form(self):
        self.email_lbl = tk.Label(self, text="Enter email:")
        self.pwd_lbl = tk.Label(self, text="Enter password:")

        self.email_input = tk.Entry(self, width=30)
        self.pwd_input = tk.Entry(self, show='*', width=30)

        self.email_lbl.pack()
        self.email_input.pack()
        self.email_input.focus_set()
        self.pwd_lbl.pack()
        self.pwd_input.pack()

    def cleanup(self):
        self.status.set('Done! Waiting for start...')
        self.sx.cleanup()
        del self.sx

    def initialize_url_input(self):
        self.url_label = tk.Label(self, text="Enter url:")
        self.url_label.pack()
        # self.url_label.grid(row=0, padx=10, pady=10)

        self.url_input = tk.Entry(self, width=30)
        self.url_input.pack()
        # self.url_input.grid(row=0, column=1, padx=10, pady=10)

    def initialize_headless_cbox(self):
        self.headless_bool = tk.BooleanVar()
        self.headless_bool.set(False)
        self.headless_cbox = tk.Checkbutton(
            self, text="Headless browser", variable=self.headless_bool)
        self.headless_cbox.pack()

    def initialize_restrict_cbox(self):
        self.restrict_str = tk.StringVar()
        self.restrict_str.set('disabled')
        self.restrict_cbox = tk.Checkbutton(
            self,
            text="Restrict number of bids",
            variable=self.restrict_str,
            onvalue='normal',
            offvalue='disabled',
            command=self.restrict_cbox_callback)
        # self.restrict_cbox.grid(row=1, padx=10, pady=10)
        self.restrict_cbox.pack()

    def initialize_restrict_input(self):
        # self.restrict_num_val = tk.IntVar(self)
        vcmd = self.register(self.validate_restrict_num)
        self.restric_num_input = tk.Entry(
            self,
            width=3,
            validate='all',
            validatecommand=(vcmd, '%P'),
            state='disabled')
        # self.restric_num_input.grid(row=1, column=1, padx=10, pady=10)
        self.restric_num_input.pack()

    def initialize_buttons(self):
        self.start_btn = tk.Button(
            self, text="Start", command=self.start_btn_callback, padx=10)
        # self.start_btn.grid(row=2, column=2, padx=10, pady=10)
        self.start_btn.pack()

        # self.quit_btn = tk.Button(
        #     self, text="Quit", command=self.quit_btn_callback, padx=10)
        # # self.quit_btn.grid(row=2, column=3, padx=10, pady=10)
        # self.quit_btn.pack()

    def initialize_status(self):
        self.status_lbl = tk.Label(self, text="Status:")
        self.status_lbl.pack()

        self.status = tk.StringVar()
        self.status.set('Waiting to start...')
        self.status_entry = tk.Entry(
            self, textvariable=self.status, state='disabled')
        self.status_entry.pack()

        self.success_bids_lbl = tk.Label(self, text="Successful bids:")
        self.success_bids_lbl.pack()

        self.success_bids = tk.IntVar()
        self.success_bids.set(0)
        self.success_bids_entry = tk.Entry(
            self, textvariable=self.success_bids, state='disabled')
        self.success_bids_entry.pack()

    def is_url_valid(self, P):
        return P.startswith(constants.STOCKX_BASE_URL) and len(P) > len(
            constants.STOCKX_BASE_URL)

    def validate_restrict_num(self, P):
        return P.isdigit() or P == ""

    def restrict_cbox_callback(self):
        self.restric_num_input.config(state=self.restrict_str.get())

    # def quit_btn_callback(self):
    #     self.destroy()

    def start_btn_callback(self):
        if hasattr(self, "sx"):
            try:
                self.sx.cleanup()
            except:
                pass
            del self.sx

        email = self.email_input.get().strip()
        pwd = self.pwd_input.get()
        url = self.url_input.get().strip()

        if email == '':
            messagebox.showerror('Error', 'Please enter your StockX email!')
            return
        if pwd == '':
            messagebox.showerror('Error', 'Please enter your StockX password!')
            return
        if not self.is_url_valid(url):
            messagebox.showerror('Error', 'Invalid url format!')
            return

        should_restrict = self.restrict_str.get() == 'normal'
        restrict_num = self.restric_num_input.get().strip()
        if should_restrict and restrict_num == '':
            messagebox.showerror(
                'Error',
                'Please enter restrict number or check the Restrict checkbox!')
            return

        if not should_restrict and restrict_num == '':
            restrict_num = 0
        else:
            restrict_num = int(restrict_num)

        headless_bool = bool(self.headless_bool.get())

        self.sx = StockX(self, email, pwd, url, should_restrict, restrict_num,
                         headless_bool)
        self.should_quit = False
        self.sx.start()


if __name__ == '__main__':
    if not os.path.isfile(constants.CSV_NAME):
        with open(constants.CSV_NAME, 'w') as f:
            f.write('product_url, brand, sub_category, bid\n')

    root = Root()
    root.mainloop()