from game import Game


def main():
    app = Game()
    for event in app.run():
        print(event)


if __name__ == "__main__":
    main()
