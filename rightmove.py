from rightmoveparser import  RightMoveParser

def start():
    rightmove = RightMoveParser();
    page = rightmove.search();
    if rightmove.results:
        for item in rightmove.results:
            print("id: " + item.id +
                  ", desc: " + item.desc +
                  ", address: " + item.address +
                  ", price: " + item.price +
                  ", date: " + item.date +
                  ", agent: " + item.agent)
    return page


if __name__ == '__main__':
    start()