class Game:
    # has a collision occured?
    def isCollision(self,x1,y1,x2,y2,bsize):
        # if x1 >= x2 and x1 <= x2 + bsize:
        #     if y1 >= y2 and y1 <= y2 + bsize:
        #         return True
        if x1 == x2 and y1==y2:
            return True
        return False