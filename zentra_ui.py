import customtkinter

class ZentraUI:
    def __init__(self, root):
        self.root = root
        self.is_running = True
        
        self.root.overrideredirect(True)
        self.root.config(bg="#212121") 
        self.root.wm_attributes("-transparentcolor", "#212121")
        self.root.geometry("+50+50")
        
        self.main_frame = customtkinter.CTkFrame(
            self.root,
            corner_radius=15,
            fg_color="#2B2B2B"
        )
        self.main_frame.pack(padx=10, pady=10, expand=True, fill="both")
        
        self.char_label = customtkinter.CTkLabel(
            self.main_frame, text="( o.o )", 
            font=customtkinter.CTkFont(family="Consolas", size=24, weight="bold"),
            text_color="#00ff99"
        )
        self.char_label.pack(pady=(10, 5), padx=20)
        
        self.status_label = customtkinter.CTkLabel(
            self.main_frame, text="", 
            font=customtkinter.CTkFont(family="Segoe UI", size=13),
            wraplength=300, justify="left",
            text_color="white"
        )
        self.status_label.pack(pady=(5, 15), padx=20)

        self.animation_frames = ["( Z.z )", "( o.o )", "( >.< )", "( ^.^ )"]
        self.frame_index = 0
        self.animate()

    def animate(self):
        if self.is_running:
            self.char_label.configure(text=self.animation_frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.animation_frames)
            self.root.after(700, self.animate)

    def stop(self):
        self.is_running = False
        
    def update_status(self, text):
        self.status_label.configure(text=text)