from .gGUI import GameGUI





if __name__ == "__main__":
    ui = GameGUI()
    while True:
        if not ui.run():
            break