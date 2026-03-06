from game import Game


def main():
    app = Game()
    last = None
    for event in app.run():
        if last and last.type == event.type:
            print(f"\033[2K\r{event}", end="")
        else:
            print(f"\n{event}", end="")
        last = event


if __name__ == "__main__":
    main()
