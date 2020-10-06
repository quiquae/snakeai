# TO DO: make it all into 1 snake where you can pick whether manual or nonmanual, 
# recording a game? option to pick which ones watcch/stats since doesnt make sense to watch all of them- record stats better!
#making video of the snake game- save images of each screen?? record it playing every 50 games? https://stackoverflow.com/questions/6087484/how-to-capture-pygame-screen
# DISPLAY IT EVERY 50?
# MAKE IT HARDER?
# train it on a GPU- trains much quicker!
 # make a better state-- pass in a grid that goes several squares by the head? for each square indicate whether there's adanger there or not


from app import App
import argparse
#---
 
if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument('--enable-display',dest='display',action='store_true')
    parser.add_argument("--speed", type=int, default=50)
    parser.add_argument("--state-size",dest='state_size',type=int, default=5)
    args = parser.parse_args()
    print(args)
    theApp = App(args.display, args.state_size)
    theApp.on_execute(args.speed)