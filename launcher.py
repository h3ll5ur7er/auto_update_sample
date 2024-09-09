
def run():
    from business_logic import main
    main()

def check_update():
    from updater import update_all
    update_all()

if __name__ == '__main__':
    check_update()
    run()