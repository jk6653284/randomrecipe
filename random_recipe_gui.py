"""
GUI for random recipe
"""

# imports
from functools import partial
import tkinter as tk
import webbrowser

# import random selector
from random_recipe_reco import get_random_recipes

# if interacted, open webbrowser in new url
def open_web(url):
    webbrowser.open(url,new=1)

# if interacted, retrieve new random recipes
def display_random_recipes():
    global frm_recipes
    # reset elements in previous frm recipes
    for child in frm_recipes.winfo_children():
        child.destroy()

    recipes = get_random_recipes()

    for recipe in recipes:
        button = tk.Button(master=frm_recipes,
                           text=f"<{recipe[0]}>\n{recipe[1]}",
                           command=partial(open_web,recipe[2])
                           )
        button.pack()


# create window
window = tk.Tk()
window.title("RRR - Random Recipe Recommendation")

# frame to contain random recipes
frm_recipes = tk.Frame(master=window)
frm_recipes.grid(row=1,column=0)

# create button to generate random recipes,
# which will also refresh everytime
btn_reco = tk.Button(text="Click to generate random recipe!",
                     master=window,
                     command=display_random_recipes)
btn_reco.grid(row=0,column=0)

# mainloop
window.mainloop()