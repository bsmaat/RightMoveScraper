from rightmoveparser import  RightMoveParser

def start():
    rightmove = RightMoveParser()
    rightmove.search()

    # print the results for sanity's sake
    if rightmove.results.empty == False:
        #for item in rightmove.results   :
        #    print(item.to_string())
        print(rightmove.results.values)
    rightmove.results.to_csv("houses.csv")
    # rightmove.save("houses.csv")
    print(rightmove.results.shape)

    return None


if __name__ == '__main__':
    start()